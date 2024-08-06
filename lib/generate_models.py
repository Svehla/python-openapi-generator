import re
from typing import Dict, Any, Optional, List, Set, Union, Tuple
from enum import Enum
from pydantic import BaseModel, RootModel

def generate_models(openapi_spec: Dict[str, Any]) -> str:
    models = []
    enums = []
    generated_class_names: Set[str] = set()
    model_dependencies: Dict[str, Set[str]] = {}
    
    model_mapping = {}
    component_schemas = openapi_spec.get('components', {}).get('schemas', {}) or openapi_spec.get('definitions', {})

    # Process components first
    for schema_name, schema in component_schemas.items():
        model_code, model_name = generate_model(
            schema,
            schema_name,
            generated_class_names,
            enums,
            models,
            component_schemas,
            model_dependencies
        )
        if model_code:
            models.append((model_name, model_code))

    for path, methods in openapi_spec.get('paths', {}).items():
        path_key = path.replace('/', '_').replace('{', '').replace('}', '')
        path_key = re.sub(r'\W|^(?=\d)', '_', path_key)  # Replace invalid characters
        
        model_mapping[path] = {}
        
        for method, details in methods.items():
            method_name = method.upper()
            method_classes = {}

            parameters_classes = {}

            if 'parameters' in details:
                for param in details['parameters']:
                    param_in = param['in']
                    param_name = param['name']
                    if param_in == 'body':
                        param_schema = param.get('schema')
                        if param_schema:
                            if '$ref' in param_schema:
                                param_schema = resolve_ref(param_schema['$ref'], component_schemas)
                            model_code, model_name = generate_model(
                                param_schema,
                                f"{path_key}_{method_name}_BodyParam",
                                generated_class_names,
                                enums,
                                models,
                                component_schemas,
                                model_dependencies,
                                base_class="BaseModel"
                            )
                            if model_code:
                                models.append((model_name, model_code))
                                parameters_classes[param_name] = model_name
                    else:
                        param_schema = param.get('schema')
                        if param_schema:
                            if '$ref' in param_schema:
                                param_schema = resolve_ref(param_schema['$ref'], component_schemas)
                            required = param.get('required', False)
                            type_hint = map_type(param_schema.get('type'))
                            parameters_classes[param_name] = (type_hint, required)
                    
                if parameters_classes:
                    param_class_name = f"{path_key}_{method_name}_Params"
                    param_class_code = generate_parameter_class(param_class_name, parameters_classes, base_class="BaseModel")
                    models.append((param_class_name, param_class_code))
                    method_classes["parameters"] = param_class_name

            if 'requestBody' in details:
                schema = details['requestBody']['content']['application/json']['schema']
                if '$ref' in schema:
                    schema = resolve_ref(schema['$ref'], component_schemas)
                model_code, model_name = generate_model(
                    schema,
                    f"{path_key}_{method_name}_RequestBody",
                    generated_class_names,
                    enums,
                    models,
                    component_schemas,
                    model_dependencies,
                    base_class="BaseModel"
                )
                if model_code:
                    models.append((model_name, model_code))
                    method_classes["requestBody"] = model_name

            responses = {}
            if 'responses' in details:
                response_classes = {}
                for status, response in details['responses'].items():
                    if 'content' in response and 'application/json' in response['content']:
                        schema = response['content']['application/json']['schema']
                        if '$ref' in schema:
                            schema = resolve_ref(schema['$ref'], component_schemas)
                        model_code, model_name = generate_model(
                            schema,
                            f"{path_key}_{method_name}_Response_Status{status}",
                            generated_class_names,
                            enums,
                            models,
                            component_schemas,
                            model_dependencies
                        )
                        if model_code:
                            models.append((model_name, model_code))
                            response_classes[status] = model_name
                        else:
                            response_classes[status] = 'Any'
                method_classes["responses"] = response_classes

            model_mapping[path][method_name] = method_classes

    sorted_models = topological_sort(models, model_dependencies)

    output = []

    output.append("from pydantic import BaseModel, RootModel\n")
    output.append("from typing import Optional, List, Dict, Any, Union\n")
    if enums:
        output.append("from enum import Enum\n\n")
    else:
        output.append("\n")
    output.append("\n\n".join(enums))
    output.append("\n\n")
    output.append("\n\n".join([model_code for _, model_code in sorted_models]))
    
    output.append("\n\nmodel_mapping = {\n")
    for key, method_classes in model_mapping.items():
        output.append(f'    "{key}": {{\n')
        for method, classes in method_classes.items():
            output.append(f'        "{method}": {{\n')
            for class_type, class_name in classes.items():
                if isinstance(class_name, dict):
                    output.append(f'            "{class_type}": {{\n')
                    for status, response_class in class_name.items():
                        output.append(f'                "{status}": {response_class},\n')
                    output.append(f'            }},\n')
                else:
                    output.append(f'            "{class_type}": {class_name},\n')
            output.append(f'        }},\n')
        output.append(f'    }},\n')
    output.append("}\n")

    return "".join(output)

def resolve_ref(ref: str, component_schemas: Dict[str, Any]) -> Dict[str, Any]:
    ref_name = ref.split('/')[-1]
    return component_schemas.get(ref_name, {})

def generate_model(schema: Dict[str, Any], base_name: str, generated_class_names: Set[str], enums: List[str], models: List[Tuple[str, str]], component_schemas: Dict[str, Any], model_dependencies: Dict[str, Set[str]], base_class: Optional[str] = "BaseModel") -> (str, str):
    if '$ref' in schema:
        schema = resolve_ref(schema['$ref'], component_schemas)

    properties = schema.get('properties', {})
    required = schema.get('required', [])
    
    model_name = base_name
    count = 1
    while model_name in generated_class_names:
        model_name = f"{base_name}_{count}"
        count += 1
    
    generated_class_names.add(model_name)
    model_dependencies[model_name] = set()

    class_inheritance = f'({base_class})' if base_class else ''
    model_code = f'class {model_name}{class_inheritance}:\n'
    lines = []

    if not properties and 'oneOf' not in schema and 'items' not in schema:
        lines.append('    pass\n')
    elif 'items' in schema and 'oneOf' in schema['items']:
        one_of_models = []
        for idx, sub_schema in enumerate(schema['items']['oneOf']):
            sub_model_code, sub_model_name = generate_model(sub_schema, f"{model_name}_OneOf_{idx}", generated_class_names, enums, models, component_schemas, model_dependencies)
            if sub_model_code:
                models.append((sub_model_name, sub_model_code))
                one_of_models.append(sub_model_name)
                model_dependencies[model_name].add(sub_model_name)
        type_hint = f'Union[{", ".join(one_of_models)}]'
        model_code = f'class {model_name}(RootModel[List[{type_hint}]]):\n'
        lines.append('    pass\n')
    else:
        for prop, details in properties.items():
            if '$ref' in details:
                ref_name = details['$ref'].split('/')[-1]
                type_hint = ref_name
                model_dependencies[model_name].add(ref_name)
            elif 'type' not in details and 'oneOf' not in details:
                continue
            elif 'enum' in details:
                enum_name = f"{model_name}_{prop.capitalize()}"
                enum_code = generate_enum(enum_name, details['enum'])
                enums.append(enum_code)
                type_hint = enum_name
            elif details.get('type') == 'object':
                nested_model_code, nested_model_name = generate_model(details, f"{model_name}_{prop.capitalize()}", generated_class_names, enums, models, component_schemas, model_dependencies)
                if nested_model_code:
                    models.append((nested_model_name, nested_model_code))
                    type_hint = nested_model_name
                    model_dependencies[model_name].add(nested_model_name)
                else:
                    type_hint = 'Dict[str, Any]'
            elif details.get('type') == 'array':
                item_details = details.get('items', {})
                if item_details.get('type') == 'object':
                    nested_model_code, nested_model_name = generate_model(item_details, f"{model_name}_{prop.capitalize()}Item", generated_class_names, enums, models, component_schemas, model_dependencies)
                    if nested_model_code:
                        models.append((nested_model_name, nested_model_code))
                        type_hint = f'List[{nested_model_name}]'
                        model_dependencies[model_name].add(nested_model_name)
                    else:
                        type_hint = 'List[Dict[str, Any]]'
                else:
                    type_hint = f'List[{map_type(item_details.get("type", "Any"))}]'
            elif 'oneOf' in details:
                one_of_models = []
                for idx, sub_schema in enumerate(details['oneOf']):
                    sub_model_code, sub_model_name = generate_model(sub_schema, f"{model_name}_{prop.capitalize()}_OneOf_{idx}", generated_class_names, enums, models, component_schemas, model_dependencies)
                    if sub_model_code:
                        models.append((sub_model_name, sub_model_code))
                        one_of_models.append(sub_model_name)
                        model_dependencies[model_name].add(sub_model_name)
                type_hint = f'Union[{", ".join(one_of_models)}]'
            else:
                type_hint = map_type(details['type'])
            
            nullable = details.get('nullable', False)
            if nullable:
                type_hint = f'Optional[{type_hint}]'
            if prop not in required:
                lines.append(f'    {prop}: {type_hint} = None\n')
            else:
                lines.append(f'    {prop}: {type_hint}\n')
    
    # If no lines were added, add 'pass'
    if not lines:
        lines.append('    pass\n')

    model_code += "".join(lines)
    
    return model_code, model_name

def generate_enum(enum_name: str, values: List[str]) -> str:
    enum_code = f'class {enum_name}(Enum):\n'
    for value in values:
        enum_value = re.sub(r'\W|^(?=\d)', '_', value).upper()
        enum_code += f'    {enum_value} = "{value}"\n'
    return enum_code

def generate_parameter_class(class_name: str, parameters: Dict[str, Union[str, bool]], base_class: Optional[str] = "BaseModel") -> str:
    class_inheritance = f'({base_class})' if base_class else ''
    parameter_class_code = f'class {class_name}{class_inheritance}:\n'
    if not parameters:
        parameter_class_code += '    pass\n'
    for param, type_or_class in parameters.items():
        if isinstance(type_or_class, tuple):
            type_hint, required = type_or_class
            if required:
                parameter_class_code += f'    {param}: {type_hint}\n'
            else:
                parameter_class_code += f'    {param}: Optional[{type_hint}] = None\n'
        else:
            parameter_class_code += f'    {param}: {type_or_class}\n'
    return parameter_class_code

def map_type(openapi_type: str) -> str:
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'boolean': 'bool',
        'array': 'List',
        'object': 'Dict',
    }
    return type_mapping.get(openapi_type, 'Any')

def topological_sort(models: List[Tuple[str, str]], dependencies: Dict[str, Set[str]]) -> List[Tuple[str, str]]:
    sorted_models = []
    visited = set()
    temp = set()

    def visit(model):
        if model in temp:
            raise ValueError("Circular dependency detected")
        if model not in visited:
            temp.add(model)
            for dep in dependencies.get(model, []):
                visit(dep)
            temp.remove(model)
            visited.add(model)
            sorted_models.append(model)

    for model, _ in models:
        if model not in visited:
            visit(model)
    
    sorted_model_dict = {model: code for model, code in models}
    return [(model, sorted_model_dict[model]) for model in sorted_models]


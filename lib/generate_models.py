import re
from typing import Dict, Any, Optional, List, Set, Union, Tuple, Type, Literal
from typing_extensions import TypedDict

def sanitize_class_name(name: str) -> str:
    name = re.sub(r'\W|^(?=\d)', '_', name)
    if name.startswith('__'):
        name = '_' + name.lstrip('_')
    return name

def generate_models(openapi_spec: Dict[str, Any]) -> str:
    models = []
    generated_class_names: Set[str] = set()
    model_dependencies: Dict[str, Set[str]] = {}

    model_mapping = {}
    component_schemas = openapi_spec.get('components', {}).get('schemas', {}) or openapi_spec.get('definitions', {})

    for schema_name, schema in component_schemas.items():
        model_code, model_name = generate_model(
            schema,
            schema_name,
            generated_class_names,
            models,
            component_schemas,
            model_dependencies
        )
        if model_code:
            models.append((model_name, model_code))

    for path, methods in openapi_spec.get('paths', {}).items():
        path_key = sanitize_class_name(path.replace('/', '_').replace('{', '').replace('}', ''))
        
        method_classes = {}

        for method, details in methods.items():
            method_name = method.upper()
            method_key = sanitize_class_name(f"{path_key}_{method_name}")

            query_parameters_class = None
            path_parameters_class = None
            request_body_class = None
            response_classes = {}

            if 'parameters' in details:
                query_param_fields = {}
                path_param_fields = {}

                for param in details['parameters']:
                    param_in = param['in']
                    param_name = param['name']
                    param_schema = param.get('schema')
                    if param_schema:
                        if '$ref' in param_schema:
                            param_schema = resolve_ref(param_schema['$ref'], component_schemas)
                        required = param.get('required', False)
                        type_hint = map_type(param_schema.get('type')) # type: ignore
                        
                        if param_in == 'query':
                            query_param_fields[param_name] = (type_hint, required)
                        elif param_in == 'path':
                            path_param_fields[param_name] = (type_hint, required)
                
                if query_param_fields:
                    query_param_class_name = sanitize_class_name(f"{method_key}_QueryParams")
                    query_param_class_code = generate_parameter_class(query_param_class_name, query_param_fields, base_class="TypedDict")
                    models.append((query_param_class_name, query_param_class_code))
                    query_parameters_class = query_param_class_name

                if path_param_fields:
                    path_param_class_name = sanitize_class_name(f"{method_key}_PathParams")
                    path_param_class_code = generate_parameter_class(path_param_class_name, path_param_fields, base_class="TypedDict")
                    models.append((path_param_class_name, path_param_class_code))
                    path_parameters_class = path_param_class_name

            if 'requestBody' in details:
                schema = details['requestBody']['content']['application/json']['schema']
                if '$ref' in schema:
                    schema = resolve_ref(schema['$ref'], component_schemas)
                model_code, model_name = generate_model(
                    schema,
                    sanitize_class_name(f"{method_key}_RequestBody"),
                    generated_class_names,
                    models,
                    component_schemas,
                    model_dependencies,
                    base_class="TypedDict"
                )
                if model_code:
                    models.append((model_name, model_code))
                    request_body_class = model_name

            if 'responses' in details:
                for status, response in details['responses'].items():
                    if 'content' in response and 'application/json' in response['content']:
                        schema = response['content']['application/json']['schema']
                        if '$ref' in schema:
                            schema = resolve_ref(schema['$ref'], component_schemas)
                        if 'oneOf' in schema:
                            one_of_models = []
                            for idx, sub_schema in enumerate(schema['oneOf']):
                                sub_model_code, sub_model_name = generate_model(
                                    sub_schema,
                                    sanitize_class_name(f"{method_key}_Response_{status}_OneOf_{idx}"),
                                    generated_class_names,
                                    models,
                                    component_schemas,
                                    model_dependencies
                                )
                                if sub_model_code:
                                    models.append((sub_model_name, sub_model_code))
                                    one_of_models.append(sub_model_name)
                                    model_dependencies[model_name].add(sub_model_name)
                            type_hint = 'Union[\n    {}\n]'.format(",\n    ".join(one_of_models))
                            response_class_name = sanitize_class_name(f"{method_key}_Response_{status}")
                            response_class_code = generate_union_response_class(response_class_name, type_hint)
                            models.append((response_class_name, response_class_code))
                            response_classes[status] = response_class_name
                        else:
                            model_code, model_name = generate_model(
                                schema,
                                sanitize_class_name(f"{method_key}_Response_Status{status}"),
                                generated_class_names,
                                models,
                                component_schemas,
                                model_dependencies
                            )
                            if model_code:
                                models.append((model_name, model_code))
                                response_class_name = sanitize_class_name(f"{method_key}_Response_{status}")
                                response_class_code = generate_typed_dict_response_class(response_class_name, model_name)
                                models.append((response_class_name, response_class_code))
                                response_classes[status] = response_class_name

            method_class_name = sanitize_class_name(f"{method_key}_Method")
            method_class_code = generate_method_class(method_class_name, query_parameters_class, path_parameters_class, request_body_class, response_classes, path, method_name)
            models.append((method_class_name, method_class_code))
            method_classes[method_name] = method_class_name
        
        path_class_name = sanitize_class_name(f"{path_key}_API")
        path_class_code = generate_path_class(path_class_name, method_classes)
        models.append((path_class_name, path_class_code))
        model_mapping[path_key] = (path_class_name, path)  # store path for comment generation

    sorted_models = topological_sort(models, model_dependencies)

    output = []

    output.append("from typing import Optional, List, Dict, Any, Union, Type, Literal\n")
    output.append("from typing_extensions import TypedDict\n\n")
    output.append("\n\n".join([model_code for _, model_code in sorted_models]))
    
    output.append("\n\nclass ModelMapping:\n")
    for key, (class_name, path) in model_mapping.items():
        output.append(f'\n')
        output.append(f'    # {path}\n')
        output.append(f'    {key} = {class_name}\n')

    return "".join(output)

def resolve_ref(ref: str, component_schemas: Dict[str, Any]) -> Dict[str, Any]:
    ref_name = ref.split('/')[-1]
    return component_schemas.get(ref_name, {})

def generate_model(schema: Dict[str, Any], base_name: str, generated_class_names: Set[str], models: List[Tuple[str, str]], component_schemas: Dict[str, Any], model_dependencies: Dict[str, Set[str]], base_class: Optional[str] = "TypedDict") -> (str, str):
    if '$ref' in schema:
        schema = resolve_ref(schema['$ref'], component_schemas)

    properties = schema.get('properties', {})
    required = schema.get('required', [])
    
    model_name = sanitize_class_name(base_name)
    count = 1
    while model_name in generated_class_names:
        model_name = sanitize_class_name(f"{base_name}_{count}")
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
            sub_model_code, sub_model_name = generate_model(sub_schema, sanitize_class_name(f"{model_name}_OneOf_{idx}"), generated_class_names, models, component_schemas, model_dependencies)
            if sub_model_code:
                models.append((sub_model_name, sub_model_code))
                one_of_models.append(sub_model_name)
                model_dependencies[model_name].add(sub_model_name)
        type_hint = 'Union[\n    {}\n]'.format(",\n    ".join(one_of_models))
        model_code = f'class {model_name}(List[{type_hint}]):\n'
        lines.append('    pass\n')
    elif 'oneOf' in schema:
        one_of_models = []
        for idx, sub_schema in enumerate(schema['oneOf']):
            sub_model_code, sub_model_name = generate_model(sub_schema, sanitize_class_name(f"{model_name}_OneOf_{idx}"), generated_class_names, models, component_schemas, model_dependencies)
            if sub_model_code:
                models.append((sub_model_name, sub_model_code))
                one_of_models.append(sub_model_name)
                model_dependencies[model_name].add(sub_model_name)
        type_hint = 'Union[\n    {}\n]'.format(",\n    ".join(one_of_models))
        model_code = f'class {model_name}(TypedDict):\n'
        lines.append(f'    pass\n')
    else:
        for prop, details in properties.items():
            if '$ref' in details:
                ref_name = details['$ref'].split('/')[-1]
                type_hint = ref_name
                model_dependencies[model_name].add(ref_name)
            elif 'type' not in details and 'oneOf' not in details:
                continue
            elif 'enum' in details:
                literal_values = ", ".join(f'"{value}"' for value in details['enum'])
                type_hint = f'Literal[{literal_values}]'
            elif details.get('type') == 'object':
                nested_model_code, nested_model_name = generate_model(details, sanitize_class_name(f"{model_name}_{prop.capitalize()}"), generated_class_names, models, component_schemas, model_dependencies)
                if nested_model_code:
                    models.append((nested_model_name, nested_model_code))
                    type_hint = nested_model_name
                    model_dependencies[model_name].add(nested_model_name)
                else:
                    type_hint = 'Dict[str, Any]'
            elif details.get('type') == 'array':
                item_details = details.get('items', {})
                if item_details.get('type') == 'object':
                    nested_model_code, nested_model_name = generate_model(item_details, sanitize_class_name(f"{model_name}_{prop.capitalize()}Item"), generated_class_names, models, component_schemas, model_dependencies)
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
                    sub_model_code, sub_model_name = generate_model(sub_schema, sanitize_class_name(f"{model_name}_{prop.capitalize()}_OneOf_{idx}"), generated_class_names, models, component_schemas, model_dependencies)
                    if sub_model_code:
                        models.append((sub_model_name, sub_model_code))
                        one_of_models.append(sub_model_name)
                        model_dependencies[model_name].add(sub_model_name)
                type_hint = 'Union[\n    {}\n]'.format(",\n    ".join(one_of_models))
            else:
                type_hint = map_type(details['type'])
            
            nullable = details.get('nullable', False)
            if nullable:
                type_hint = f'Optional[{type_hint}]'
            if prop not in required:
                lines.append(f'    {prop}: Optional[{type_hint}]\n')
            else:
                lines.append(f'    {prop}: {type_hint}\n')
    
    if not lines:
        lines.append('    pass\n')

    model_code += "".join(lines)
    
    return model_code, model_name

def generate_union_response_class(class_name: str, union_type: str) -> str:
    return f'class {class_name}(TypedDict):\n    data: {union_type}\n'

def generate_typed_dict_response_class(class_name: str, model_name: str) -> str:
    return f'class {class_name}(TypedDict):\n    data: {model_name}\n'

def generate_parameter_class(class_name: str, parameters: Dict[str, Tuple[str, bool]], base_class: Optional[str] = "TypedDict") -> str:
    class_inheritance = f'({base_class})' if base_class else ''
    parameter_class_code = f'class {class_name}{class_inheritance}:\n'
    if not parameters:
        parameter_class_code += '    pass\n'
    for param, (type_hint, required) in parameters.items():
        if required:
            parameter_class_code += f'    {param}: {type_hint}\n'
        else:
            parameter_class_code += f'    {param}: Optional[{type_hint}]\n'
    return parameter_class_code

def generate_method_class(class_name: str, query_parameters: Optional[str], path_parameters: Optional[str], request_body: Optional[str], responses: Dict[str, Union[str, Type]], url: str, method: str) -> str:
    method_class_code = f'class {class_name}:\n'
    lines = []
    if query_parameters:
        lines.append(f'    query = {query_parameters}\n')
    if path_parameters:
        lines.append(f'    path = {path_parameters}\n')
    if request_body:
        lines.append(f'    request_body = {request_body}\n')
    if responses:
        for status, response_type in responses.items():
            lines.append(f'    response_{status} = {response_type}\n')
    lines.append(f'    URL: Literal["{url}"] = "{url}"\n')
    lines.append(f'    METHOD: Literal["{method}"] = "{method}"\n')
    if not lines:
        lines.append('    pass\n')
    method_class_code += "".join(lines)
    return method_class_code

def generate_path_class(class_name: str, methods: Dict[str, str]) -> str:
    path_class_code = f'class {class_name}:\n'
    lines = []
    for method, method_class in methods.items():
        lines.append(f'    {method} = {method_class}\n')
    if not lines:
        lines.append('    pass\n')
    path_class_code += "".join(lines)
    return path_class_code

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

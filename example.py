import json
from lib.generate_models import generate_models
import os  # Import the os module to handle directory operations

print('--- start generating openapi ---')

with open('example_openapi.json', 'r') as file:
    openapi_spec = json.load(file)
    generated_code = generate_models(openapi_spec)

    pretty_generated_code = generated_code # json.dumps(generated_code, indent=2)
    
    output_dir = '__generated_api__'
    os.makedirs(output_dir, exist_ok=True)


    # Save the pretty printed generated code to a file
    output_file_path = os.path.join(output_dir, 'api_types.py')
    with open(output_file_path, 'w') as output_file:
        output_file.write(pretty_generated_code)


print('DONE')

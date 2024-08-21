import json
import os
from lib.generate_models import generate_models

print('--- start generating openapi ---')

# Define the root directory where your test folders are located
root_dir = 'tests'

# Iterate over each folder within the root directory
for folder_name in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder_name)
    
    # Check if the path is a directory
    if os.path.isdir(folder_path):
        openapi_file_path = os.path.join(folder_path, 'openapi.json')
        
        # Check if the openapi.json file exists in the directory
        if os.path.exists(openapi_file_path):
            with open(openapi_file_path, 'r') as file:
                openapi_spec = json.load(file)
                generated_code = generate_models(openapi_spec)

                # The generated code is already pretty formatted
                pretty_generated_code = generated_code
                
                # Save the pretty printed generated code to a file in the same directory
                output_file_path = os.path.join(folder_path, '__generated_api_types.py')
                with open(output_file_path, 'w') as output_file:
                    output_file.write(pretty_generated_code)

            print(f'Generated types for {folder_name}')
        else:
            print(f'No openapi.json found in {folder_name}')

print('DONE')

"""
This file runs the diagram validator to check all examples on the original dataset and check if diagrams are valid or not. It creates a new dataset with that info
"""
import sys
import os
import json

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by using os.path.dirname on the current directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from diagram_validator import validate_diagram

# Define the filenames
input_filename = '../../data/mermaid_dataset_public.json'
output_filename = 'mermaid_dataset_with_validity.json'

# Open and read the JSON file
with open(input_filename, 'r', encoding='utf-8') as file:
    # Load JSON content from the file
    full_data = json.load(file)

# Create a new list that will hold objects with the validity of the diagrams
data_with_validity = []

# Counter to keep track of progress
total_entries = len(full_data)
count = 0

# Iterate through each entry in the dataset
for obj in full_data:
    # Extract the diagram field from the current object
    diagram = obj.get('mermaid', None)

    # Validate the diagram and add the 'is_diagram_valid' key to the object
    # Set it to True or False based on the diagram's validity
    obj['is_diagram_valid'] = validate_diagram(diagram) if diagram else False

    # Append the updated object to the new list
    data_with_validity.append(obj)

    # Increment counter and print progress
    count += 1
    print(f'Processed {count} of {total_entries} entries', end='\r')

# Write the updated dataset to a new file
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(data_with_validity, file, indent=4)

print(f'Dataset with diagram validity created and saved to {output_filename}')
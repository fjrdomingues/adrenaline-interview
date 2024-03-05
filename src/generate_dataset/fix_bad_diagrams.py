import sys
import os
import json

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from diagram_validator import validate_diagram
from mermaid_fixer import fix_mermaid_syntax
from mermaid_md_extractor import extract_mermaid_code

# Define input and output filenames.
input_filename = 'mermaid_dataset_with_validity.json'
fixed_output_filename = 'mermaid_dataset_with_fixed_diagrams.json'

# Load the data with validity added.
with open(input_filename, 'r', encoding='utf-8') as file:
    data_with_validity = json.load(file)

# Variable to hold the data after attempting repairs.
data_with_repairs = []

# Counter to keep track of progress
total_entries = len(data_with_validity)
count = 0

# Iterate through each entry in the dataset.
for obj in data_with_validity:
    # Check if the diagram is valid.
    is_valid = obj.get('is_diagram_valid', False)
    diagram = obj.get('mermaid', None)

    # If the diagram is invalid, try to fix it.
    if not is_valid and diagram:

        # Extract Mermaid
        cleaned_diagram = extract_mermaid_code(diagram)

        # Attempt to fix the diagram.
        fixed_diagram = fix_mermaid_syntax(cleaned_diagram)

        # Validate the fixed diagram.
        is_now_valid = validate_diagram(fixed_diagram, False)

        # Update the object if the diagram was fixed.
        if is_now_valid:
            obj['diagram_fixed'] = is_now_valid

        # Always include the (potentially fixed) diagram.
        obj['new_diagram'] = fixed_diagram or ''

    # Append the updated object to the new list.
    data_with_repairs.append(obj)

    count += 1
    print(f'Processed {count} of {total_entries} entries', end='\r')

# Write the updated dataset with repairs to a new file.
with open(fixed_output_filename, 'w', encoding='utf-8') as file:
    json.dump(data_with_repairs, file, indent=4)

print(f'Dataset with repairs saved to {fixed_output_filename}')

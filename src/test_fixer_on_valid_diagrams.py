"""
This script takes an enhanced dataset with valid diagrams, applies the fixer to them, and checks if the output remains valid.
It aims to ensure that the fixer does not introduce any issues to already valid diagrams.
"""

import os
import json
from diagram_validator import validate_diagram
from mermaid_fixer import fix_mermaid_syntax

def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_to_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def test_fixer_on_valid_diagrams(input_filename, output_filename):
    # Load the input dataset
    enhanced_data = load_json_file(input_filename)
    
    total_entries = len(enhanced_data)
    count = 0
    unchanged_count = 0
    fixer_issues_count = 0
    
    for obj in enhanced_data:
        is_valid = obj.get('is_diagram_valid')
        diagram = obj.get('new_diagram')
        
        if is_valid:
            # Apply the fixer to the valid diagram
            fixed_diagram = fix_mermaid_syntax(diagram)
            
            # Check if the fixed diagram is still valid
            is_still_valid = validate_diagram(fixed_diagram)
            
            if is_still_valid and diagram == fixed_diagram:
                unchanged_count += 1
            elif not is_still_valid:
                fixer_issues_count += 1
                print(f"Fixer introduced an issue in diagram {count + 1}")
                
            # Update the object with new information
            obj['is_fixed_diagram_still_valid'] = is_still_valid
            
        count += 1
        print(f'Checked {count} of {total_entries} diagrams', end='\r')

    # Save the results to the output file
    save_to_json_file(enhanced_data, output_filename)
    
    # Print summary statistics
    print(f'\nCompleted checks on valid diagrams.')
    print(f'{unchanged_count} diagrams remain unchanged after applying the fixer. ')
    print(f'{fixer_issues_count} diagrams had issues introduced by the fixer.')
    print(f'Results saved to {output_filename}')

# Define the input and output filenames
input_filename = 'generate_dataset/mermaid_dataset_enhanced.json'
output_filename = 'mermaid_dataset_post_fixer_check.json'

# Perform the diagram fixer check
test_fixer_on_valid_diagrams(input_filename, output_filename)

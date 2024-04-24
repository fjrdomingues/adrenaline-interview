"""
This script tests using a static fixer for fixing subgraph names. We want to check how relevant this would be.
"""

import json
import re
from modules.diagram_validator import validate_diagram
from modules.mermaid_md_extractor import extract_mermaid_code


input_filename = './rectifier_model/mermaid_dataset_enhanced.json'
output_filename = './fixed_mermaid_results.jsonl'

def load_json_file(filename):
    """ Load JSON data from a file """
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_to_json_file(data, filename):
    """ Save data to a JSONL file, each item on a new line """
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

count_matches = 0
def fix_mermaid_syntax(diagram):
    global count_matches
    """ Fix Mermaid syntax, including renaming subgraphs and removing '&#34;' """
    # Replace spaces with underscores in subgraph identifiers
    fixed_diagram = re.sub(
        r'subgraph "([^"]+)"',
        lambda match: f'subgraph {match.group(1).replace(" ", "_")}', 
        diagram
    )
    fixed_diagram = re.sub(
        r'subgraph ([^\s\{]+(?: [^\s\{]+)+)',
        lambda match: f'subgraph {match.group(1).replace(" ", "_")}',
        fixed_diagram
    )
    # Remove all instances of '&#34;' on lines that contain 'subgraph'
    # fixed_diagram = re.sub(
    #     r'(subgraph[^\n]*)',
    #     lambda match: match.group(1).replace("&#34;", ""),
    #     fixed_diagram
    # )

    if diagram != fixed_diagram:
        count_matches += 1
    print(count_matches)
    return fixed_diagram

def process_diagrams(diagrams, output_filename):
    """ Process diagrams: fix, validate, and save results """
    results = []
    successful_count = 0

    for index, diagram in enumerate(diagrams):
        diagram = extract_mermaid_code(diagram['mermaid'])
        fixed_diagram = fix_mermaid_syntax(diagram)
        is_valid, error_message = validate_diagram(fixed_diagram)

        result = {
            'original': diagram,
            'fixed': fixed_diagram,
            'valid': is_valid,
            'error_message': error_message if not is_valid else 'No errors'
        }
        results.append(result)

        if is_valid:
            successful_count += 1
        
        # Print result for current diagram and success rate so far
        print(f"Diagram {index + 1}: {'Valid' if is_valid else 'Invalid'} - {error_message if not is_valid else 'No errors'}")
        print(f"Success rate: {successful_count / (index + 1) * 100:.2f}%")

    save_to_json_file(results, output_filename)
    print(f"Processed {len(results)} diagrams. Results are saved to {output_filename}")

def get_unfixable_diagrams(filename):
    """ Retrieve diagrams that cannot be fixed """
    dataset = load_json_file(filename)
    return [data for data in dataset if not data.get('diagram_fixed', True)]


unfixable_diagrams = get_unfixable_diagrams(input_filename)
print(f"Found {len(unfixable_diagrams)} unfixable diagrams")
process_diagrams(unfixable_diagrams, output_filename)

# diagram=\
# """
# ```mermaid
# graph TD
#  subgraph &#34;Semaphores&#34;
#    A(Semaphore Variable) -->|wait #40;P#41;| B(Process 1 waiting on semaphore)
#    A -->|wait #40;P#41;| C(Process 2 waiting on semaphore)
#    A -->|signal #40;V#41;| D(Shared Resource controlled by semaphore)
#    B --> D
#    C --> D
#  end


#  subgraph &#34;Mutex Locks&#34;
#    E(Mutex Lock) -->|Lock operation| F(Process 1 waiting to acquire mutex)
#    E -->|Lock operation| G(Process 2 waiting to acquire mutex)
#    E -->|Unlock operation| H(Critical section protected by mutex)
#    F --> H
#    G --> H
#  end


#  I[Complexity and Comparison] --> J{Semaphores offer versatility}
#  I --> K{Mutex locks provide straightforward exclusive access}
#  ```
# """
# print(fix_mermaid_syntax(diagram))
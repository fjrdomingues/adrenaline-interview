"""
This script generates a dataset for identifying Mermaid diagrams that cannot be fixed.
"""

# Import json for file handling
import json

# Functions to handle JSON files
def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_to_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

# Set file paths
input_dataset_filename = './mermaid_dataset_enhanced.json'
testing_filename = 'testing_unfixable.jsonl'

# Load dataset
dataset = load_json_file(input_dataset_filename)

# Select unfixable diagrams
unfixable_diagrams = [data for data in dataset if data.get('diagram_fixed') is False]

# System message for unfixable diagrams
system_message = \
"""You are provided with a mermaidJS diagram that is syntactically incorrect. 
Correct the diagram syntax without altering its intended structure and content. Ensure the syntax is valid for mermaidJS. 
Escape all necessary characters to comply with mermaid syntax.
If the diagram contains styling you must remove it.
"""

# Format dataset
def format_for_openai(dataset):
    formatted_data = []
    for datum in dataset:
        incorrect_diagram = datum['mermaid']
        unfixed_diagram = datum['new_diagram']
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": incorrect_diagram},
            {"role": "assistant", "content": unfixed_diagram}
        ]
        formatted_data.append({"messages": messages})
    return formatted_data

# Format and save testing dataset
formatted_data = format_for_openai(unfixable_diagrams)
save_to_json_file(formatted_data, testing_filename)

# Notification of creation
print(f'Testing dataset for unfixable diagrams created, containing {len(formatted_data)} entries.')
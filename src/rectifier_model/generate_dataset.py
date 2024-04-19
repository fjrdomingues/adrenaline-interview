"""
This script generates a dataset specifically designed for fine-tuning a model to fix invalid Mermaid diagrams, tailored for OpenAI's format.
"""

# Required libraries
import json
from sklearn.model_selection import train_test_split

# Functions to load and save JSON
def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_to_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

# File locations
input_dataset_filename = './mermaid_dataset_enhanced.json'
training_filename = 'training_dataset.jsonl'
testing_filename = 'testing_dataset.jsonl'

# Load the enhanced dataset with invalid diagrams flagged and fixed diagrams included
dataset = load_json_file(input_dataset_filename)

# Filter for entries with diagrams that needed fixing and fixed successfully
fixable_diagrams = [data for data in dataset if data.get('diagram_fixed')]

# Define the system message
system_message = \
"""You are provided with a mermaidJS diagram that is syntactically incorrect. 
Correct the diagram syntax without altering its intended structure and content. Ensure the syntax is valid for mermaidJS."""

# Formatting function for OpenAI dataset
def format_for_openai(dataset):
    formatted_data = []
    for datum in dataset:
        question = datum['question']
        answer = datum['answer']
        incorrect_diagram = datum['mermaid']
        fixed_diagram = datum['new_diagram']
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": incorrect_diagram},
            {"role": "assistant", "content": fixed_diagram}
        ]
        formatted_data.append({"messages": messages})
    return formatted_data

# Format the dataset
formatted_dataset = format_for_openai(fixable_diagrams)

# Splitting the dataset
train_data, test_data = train_test_split(formatted_dataset, test_size=0.2, random_state=42)

# Save formatted datasets
save_to_json_file(train_data, training_filename)
save_to_json_file(test_data, testing_filename)

# Notification of success
print(f'Training and testing datasets have been created: {len(train_data)} training entries and {len(test_data)} testing entries saved.')

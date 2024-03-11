"""
This script validates diagrams in the original dataset and attempts to fix them if necessary.
It creates a new dataset with the validity information and the fixed diagrams. This will be used to teach the model how to handle use-cases where it usually fails.
"""
#%%
import sys
import os
import json
from sklearn.model_selection import train_test_split

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the 'modules' directory
modules_dir = os.path.join(current_dir, '..', 'modules')

# Normalize the path (resolve "..")
modules_dir = os.path.normpath(modules_dir)

if modules_dir not in sys.path:
    sys.path.append(modules_dir)

# Import the necessary modules
from diagram_validator import validate_diagram
from mermaid_fixer import fix_mermaid_syntax
from mermaid_md_extractor import extract_mermaid_code

def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_to_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Define the filenames
original_dataset_filename = '../../data/mermaid_dataset_public.json'
output_filename = 'mermaid_dataset_enhanced.json'
training_filename = 'mermaid_dataset_training.json'
testing_filename = 'mermaid_dataset_testing.json'

# Load the original dataset
full_data = load_json_file(original_dataset_filename)

enhanced_data = []

total_entries = len(full_data)
count = 0
fixed_count = 0
# %%

## Loop to enhance dataset. This is process takes ~30 minutes because mermaid CLI is slow to validate diagrams
for obj in full_data:
    # Validate the original diagram and store the result.
    diagram = obj.get('mermaid', None)

    # Extract from Markdown
    cleaned_diagram = extract_mermaid_code(diagram) if diagram else None

    # Test if diagram is valid
    is_valid = validate_diagram(cleaned_diagram) if diagram else False
    obj['is_diagram_valid'] = is_valid

    fixed_diagram = ""

    if not is_valid and cleaned_diagram:
        # Attempt to fix the diagram
        print("Diagram is not valid. Attempting to fix...")
        fixed_diagram = fix_mermaid_syntax(cleaned_diagram)
        # Re-validate the fixed diagram
        is_now_valid = validate_diagram(fixed_diagram)
        # Update the object if the diagram has been fixed
        if is_now_valid:
            print("Diagram Fixed")
            obj['diagram_fixed'] = True
            fixed_count += 1
        else:
            obj['diagram_fixed'] = False
            print("Diagram not fixed")
    # Include the cleaned/fixed diagram if diagrams were processed
    if cleaned_diagram:
        obj['new_diagram'] = fixed_diagram or cleaned_diagram
    # Exclude the "source_chunks" key from the object, if present.
    obj.pop('source_chunks', None)
    
    # Append the updated object to the enhanced data list
    enhanced_data.append(obj)

    count += 1
    print(f'Processed {count} of {total_entries} entries', end='\r')

# Save the enhanced dataset to a file
save_to_json_file(enhanced_data, output_filename)

print(f'\nDataset enhanced with validity checks and repairs saved to {output_filename}')
print(f'Number of diagrams fixed: {fixed_count}')

"""
Now with the enhanced dataset, we'll try to run a fine-tuning using the invalid diagrams that were fixed with success. 
For the testing data, we'll also add a few valid examples (diagram that didn't need fixing) to validate that the model is not overfitting on the diagrams with special chars
"""

#%%
# Load the enhanced dataset
enhanced_data = load_json_file(output_filename)

# Filter the fixed diagrams
fixed_diagrams = [item for item in enhanced_data if item.get('diagram_fixed', False)]
# Filter the enhanced data for items with originally valid diagrams (assuming 'original_diagram_valid')
valid_diagrams = [item for item in enhanced_data if item.get('is_diagram_valid', False)]

# Define the format function to create JSON Lines entries
def format_data_for_training(data, system_message):
    formatted_data = []
    for entry in data:
        # Only proceed if there is a question, answer, and diagram key in the entry
        if 'question' in entry and 'answer' in entry and 'new_diagram' in entry:
            question = entry['question']
            answer = entry['answer']
            diagram = entry['new_diagram']
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": f'# Question\n{question}\n\n# Answer\n{answer}\n\n# Your output'},
                {"role": "assistant", "content": diagram}
            ]
            
            formatted_data.append({"messages": messages})
    return formatted_data

# Create correct format for openAI training
system_message = \
"""Your task is to build a mermaidJS diagram to help users visualize an answer provided to question they did.
Your output will be parsed and validated so you must reply with VALID mermaidJS code only. Don't add anything else to your reply.

Prefer diagrams with simple syntax
Avoid styling on the diagram
Escape characters when needed
You MUST produce valid mermaidJS syntax!"""

# Format the enhanced dataset
formatted_enhanced_data = format_data_for_training(fixed_diagrams, system_message)

# Split the data into training and testing sets
train_data, test_data = train_test_split(formatted_enhanced_data, test_size=0.2, random_state=42)

# Function to write dataset to a file in JSON Lines format
def write_dataset_file(dataset, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for jsonl_item in dataset:
            # Write the JSON Lines item to file. Each item has to be followed by a newline "\n"
            file.write(json.dumps(jsonl_item, ensure_ascii=False) + '\n')

# Write the training dataset file
write_dataset_file(train_data, 'training_dataset.jsonl')
print(f'{len(train_data)} entries saved to the training dataset: training_dataset.jsonl')

# Extract the last 100 valid diagram samples, or as many as available if there are fewer than 100, to include other examples on the training dataset.
# This is useful to ensure that the training didn't hurt the model on examples that were working before.
num_additional_samples = min(100, len(valid_diagrams))
additional_samples = valid_diagrams[-num_additional_samples:]

# Format these additional samples for training
formatted_additional_samples = format_data_for_training(additional_samples, system_message)
# Add these formatted samples to the test_data
test_data.extend(formatted_additional_samples)

# Write the testing dataset file
write_dataset_file(test_data, 'testing_dataset.jsonl')
print(f'{len(test_data)} entries saved to the testing dataset: testing_dataset.jsonl')

# %%
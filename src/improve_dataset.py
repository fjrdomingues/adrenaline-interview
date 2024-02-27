"""
We are using this file to populate the training dataset with failed diagram generations from our fine-tuned model. We'll then fix them manually. This should provide good examples for the model to learn and improve syntax
"""

import json

# Hardcoded system message
system_message = \
'''Your task is to build a mermaidJS diagram to help users visualize an answer provided to question they did. You'll be provided the "Question", the "Answer", the "DiagramType" and the "DiagramTypeDocs"
Your output will be parsed and validate so you must reply with VALID mermaidJS code only and in the following format:
```mermaid
{ diagram }
```

Prefer diagrams with simple syntax
Avoid styling on the diagram
Escape characters when needed
Make sure that you don't use any forbidden mermaid characters
Make sure to below the instructions and examples in the syntax documentation
You MUST produce valid mermaidJS syntax!
'''

# Filenames
evaluation_filename = '../data/evaluation_results.json'
dataset_filename = '../data/new_dataset_full.jsonl'

# Read the evaluation results
with open(evaluation_filename, 'r', encoding='utf-8') as file:
    evaluation_results = json.load(file)

# Process each entry
with open(dataset_filename, 'a', encoding='utf-8') as file:  # 'a' mode to append to the file
    for entry in evaluation_results:
        fine_tuned_results = entry['fine-tuned-gpt-3.5']
        if not fine_tuned_results['valid_syntax']:
            question = entry['question']
            answer = entry['answer']
            diagram = fine_tuned_results['diagram']
            # Ensure there is a diagram and it is not empty
            if diagram:
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"# Question - Question from the user\n{question}\n# Answer - Answer given to the user\n{answer}\n# Your output"},
                    {"role": "assistant", "content": diagram}
                ]
                # Create a dictionary for the JSON Lines item
                jsonl_item = {"messages": messages}
                # Write the JSON Lines item to file, followed by a newline
                file.write(json.dumps(jsonl_item, ensure_ascii=False) + '\n')

print('New fine-tuning dataset has been updated.')

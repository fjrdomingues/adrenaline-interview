"""
Put any code that evaluates the model in here. If you're evaluating the validity of the MermaidJS
syntax, you may want to replace this file with a NodeJS file so you can use the Mermaid library.

Besides checking valid syntax, if you choose to also evaluate the quality of the generated diagrams,
you have a lot of liberty with how you approach that.
"""

import json
import random
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
print("Current Working Directory:", os.getcwd())


# Define the number of samples to evaluate
NUM_SAMPLES = 100  # number of random samples to evaluate on

# Specify the models to compare
first_model_name = "gpt-4-0125-preview"
second_model_name = "ft:gpt-3.5-turbo-0613:rubrick-ai::8wWjQ3wc"

# Define the filenames
input_filename = '../data/mermaid_dataset_public.json'
evaluation_filename = '../data/evaluation_results.json'
mermaid_js_path = 'validate_mermaid.js'

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

# Function to ask a model to build a MermaidJS diagram
def build_diagram(model_name, question, answer):
    system = \
'''Your task is to build a mermaidJS diagram to help users visualize an answer provided to question they did. You'll be provided the "Question" and the "Answer" that was given to the user.
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

    prompt = \
f'''# Question - Question from the user
{question}

# Answer - Answer given to the user
{answer}

# Your output'''
    response = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
          {"role": "system", "content": system},
          {"role": "user", "content": prompt}
        ]
    )
    # print(prompt)
    diagram = response.choices[0].message.content
    print(diagram)
    return diagram

# Function to validate a MermaidJS diagram
def validate_diagram(markdown_code):
    try:
        # Extract the Mermaid code block from Markdown (assuming it's well formed)
        match = re.search(r'```mermaid([^`]*)```', markdown_code, re.DOTALL)
        if not match:
            print("No valid Mermaid diagram code block found.")
            return False
        
        diagram_code = match.group(1).strip()  # Extracted Mermaid code

        # The NODE package doesn't work properly. It rejects some valid diagrams! CLI is performing better
        process = subprocess.run(
            ['mmdc', '--input', '-'],
            input=diagram_code, 
            text=True, 
            capture_output=True, 
            check=True,
            timeout=30
        )

        print("STDOUT:", process.stdout.strip())
        return process.stdout.strip() == 'Generating single mermaid chart'
    except subprocess.CalledProcessError as e:
        print("CalledProcessError:", e)
        return False
    except subprocess.TimeoutExpired as e:
        print("TimeoutExpired:", e)
        return False

# Load the dataset
with open(input_filename, 'r', encoding='utf-8') as file:
    full_data = json.load(file)

# Randomly select samples from the dataset
sample_data = random.sample(full_data, NUM_SAMPLES)

# Lists to hold evaluation results
evaluation_results = []

# Counters for success rates
first_model_success = 0
second_model_success = 0

# Evaluate each model on the selected samples
for i, sample in enumerate(sample_data):
    question = sample['question']
    answer = sample['answer']
    
    # Get diagrams from both models
    first_model_diagram = build_diagram(first_model_name, question, answer)
    second_model_diagram = build_diagram(second_model_name, question, answer)
    
    # Validate diagrams
    first_model_valid = validate_diagram(first_model_diagram)
    second_model_valid = validate_diagram(second_model_diagram)
    
    # Update success counters
    if first_model_valid:
        first_model_success += 1
    if second_model_valid:
        second_model_success += 1
    
    # Store the results
    result = {
        "sample_index": i,
        "question": question,
        "answer": answer,
        "gpt-4-turbo": {
            "name": first_model_name,
            "diagram": first_model_diagram,
            "valid_syntax": first_model_valid
        },
        "fine-tuned-gpt-3.5": {
            "name": second_model_name,
            "diagram": second_model_diagram,
            "valid_syntax": second_model_valid
        }
    }
    print(i)
    print("Model: ", first_model_name, "success: ", first_model_success)
    print("Model: ", second_model_name, "success: ", second_model_success)
    evaluation_results.append(result)

# Save the evaluation results to a file
with open(evaluation_filename, 'w', encoding='utf-8') as file:
    json.dump(evaluation_results, file, indent=4)

# Calculate and print success rates
first_model_rate = (first_model_success / NUM_SAMPLES) * 100
second_model_rate = (second_model_success / NUM_SAMPLES) * 100

print("Evaluation completed")
print(f"First model ({first_model_name}) success rate: {first_model_rate}%")
print(f"Second model ({second_model_name}) success rate: {second_model_rate}%")

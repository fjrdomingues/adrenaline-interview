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
import time
import sys
from datetime import datetime

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the 'modules' directory
modules_dir = os.path.join(current_dir, 'modules')

# Normalize the path (resolve "..")
modules_dir = os.path.normpath(modules_dir)

if modules_dir not in sys.path:
    sys.path.append(modules_dir)

from diagram_validator import validate_diagram

# Define the number of samples to evaluate
NUM_SAMPLES = 100  # number of random samples to evaluate on

# Specify the models to compare
first_model_name = "gpt-4-0125-preview"
second_model_name = "ft:gpt-3.5-turbo-0125:rubrick-ai::91izT8QS"

# Define the filenames
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
input_filename = 'generate_dataset/testing_dataset.jsonl'
evaluation_filename = f'../data/evaluation_results_{timestamp}.json'  # unique filename with timestamp

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

# Function to ask a model to build a MermaidJS diagram
def build_diagram(model_name, system, prompt):
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
    # print(diagram)
    return diagram

# Load the dataset
full_data = []
with open(input_filename, 'r', encoding='utf-8') as file:
    for line in file:
        # Parse each line (which is a JSON object) and append to the list
        full_data.append(json.loads(line))

# Use the entire testing dataset
NUM_SAMPLES = len(full_data)
# Randomly select samples from the dataset
sample_data = random.sample(full_data, NUM_SAMPLES)

# Lists to hold evaluation results
evaluation_results = []

# Counters for success rates
first_model_success = 0
second_model_success = 0
first_model_time_taken = 0
second_model_time_taken = 0

# Evaluate each model on the selected samples both models and compare them
# for i, sample in enumerate(sample_data):
#     question = sample['question']
#     answer = sample['answer']
    
#     # Get diagrams from both models and measure time to reply
#     start_time = time.time()
#     first_model_diagram = build_diagram(first_model_name, question, answer)
#     end_time = time.time()
#     first_model_elapsed = end_time - start_time

#     start_time = time.time()
#     second_model_diagram = build_diagram(second_model_name, question, answer)
#     end_time = time.time()
#     second_model_elapsed = end_time - start_time
    
#     # Validate diagrams
#     first_model_valid = validate_diagram(first_model_diagram)
#     second_model_valid = validate_diagram(second_model_diagram)
    
#     # Update success counters
#     if first_model_valid:
#         first_model_success += 1
#     if second_model_valid:
#         second_model_success += 1

#     first_model_time_taken += first_model_elapsed
#     second_model_time_taken += second_model_elapsed
    
#     # Store the results
#     result = {
#         "sample_index": i,
#         "question": question,
#         "answer": answer,
#         "gpt-4-turbo": {
#             "name": first_model_name,
#             "diagram": first_model_diagram,
#             "valid_syntax": first_model_valid,
#             "response_time": first_model_elapsed,
#         },
#         "fine-tuned-gpt-3.5": {
#             "name": second_model_name,
#             "diagram": second_model_diagram,
#             "valid_syntax": second_model_valid,
#             "response_time": second_model_elapsed,
#         }
#     }
#     print(i)
#     print("Model: ", first_model_name, "success: ", first_model_success, "time taken: ", first_model_elapsed)
#     print("Model: ", second_model_name, "success: ", second_model_success, "time taken: ", second_model_elapsed)
#     evaluation_results.append(result)

# Function to evaluate only 1 of the models
for i, sample in enumerate(sample_data):
    system = sample["messages"][0]["content"]
    prompt = sample["messages"][1]["content"]
    
    start_time = time.time()
    second_model_diagram = build_diagram(second_model_name, system, prompt)
    end_time = time.time()
    second_model_elapsed = end_time - start_time
    
    # Validate diagrams
    second_model_valid = validate_diagram(second_model_diagram)
    
    # Update success counters
    if second_model_valid:
        second_model_success += 1

    second_model_time_taken += second_model_elapsed
    
    # Store the results
    result = {
        "sample_index": i,
        "system": system,
        "prompt": prompt,
        "fine-tuned-gpt-3.5": {
            "name": second_model_name,
            "diagram": second_model_diagram,
            "valid_syntax": second_model_valid,
            "response_time": second_model_elapsed,
        }
    }
    print(i)
    print("Model: ", second_model_name, "success: ", second_model_success, "time taken: ", second_model_elapsed)
    evaluation_results.append(result)

# Save the evaluation results to a file
with open(evaluation_filename, 'w', encoding='utf-8') as file:
    json.dump(evaluation_results, file, indent=4)

# Calculate and print success rates
# first_model_rate = (first_model_success / NUM_SAMPLES) * 100
second_model_rate = (second_model_success / NUM_SAMPLES) * 100

print("Evaluation completed")
# print(f"First model ({first_model_name}) success rate: {first_model_rate}%")
print(f"Second model ({second_model_name}) success rate: {second_model_rate}%")

"""
Put any code you use for generating training or evaluation datasets in here. Please also include
the dataset itself in the `src/` directory once you make your submission.
"""

# This script filters the provided dataset to extract the user questions that are programming related

import os
import json
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import threading
from sklearn.model_selection import train_test_split
from concurrent.futures import ThreadPoolExecutor, as_completed
from diagram_types_docs import flowchart as flowchart_docs, sequenceDiagram as sequenceDiagram_docs, classDiagram as classDiagram_docs, stateDiagram as stateDiagram_docs

openai_model = "gpt-4-0125-preview"

diagram_docs = {
    "flowchart": flowchart_docs,
    "sequenceDiagram": sequenceDiagram_docs,
    "classDiagram": classDiagram_docs,
    "stateDiagram": stateDiagram_docs,
}

# Load environment variables from .env file
load_dotenv()

# Define the filenames
input_filename = '../data/mermaid_dataset_public.json'
output_filename = '../data/mermaid_dataset_public_filtered.json'
dataset_filename = '../data/dataset_full.jsonl'

# Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI()

### Functions to call GPT

# Function to ask GPT if a question is programming-related
def is_programming_question(question):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": 'Decide if the question provided is related with the topic of programming. Reply in the following JSON format: {"isProgramming": true|false}'},
      {"role": "user", "content": question}
    ]
  )
  parsed_content = json.loads(response.choices[0].message.content)
  # print (parsed_content)
  return parsed_content["isProgramming"]

# Function to ask GPT what is the best diagram type for the question/answer pair. Limiting the model to use a list of diagram types (we can later add more types if needed)
def get_diagram_type(question, answer):
  system = \
'''Based on the "Question" and "Answer" you'll decide what is the appropriate MermaidJS diagram type to use. You must select 1 of the following types:
"flowchart" - Flowcharts are composed of nodes (geometric shapes) and edges (arrows or lines). The Mermaid code defines how nodes and edges are made and accommodates different arrow types, multi-directional arrows, and any linking to and from subgraphs
"sequenceDiagram" - A Sequence diagram is an interaction diagram that shows how processes operate with one another and in what order
"classDiagram" - The class diagram is the main building block of object-oriented modeling. It is used for general conceptual modeling of the structure of the application, and for detailed modeling to translate the models into programming code. Class diagrams can also be used for data modeling. The classes in a class diagram represent both the main elements, interactions in the application, and the classes to be programmed
"stateDiagram" - A state diagram is a type of diagram used in computer science and related fields to describe the behavior of systems. State diagrams require that the system described is composed of a finite number of states; sometimes, this is indeed the case, while at other times this is a reasonable abstraction

Reply in the following JSON format: {"diagramType": "flowchart|sequenceDiagram|classDiagram|stateDiagram", "thoughts": "explain your reasoning to choose this diagram type"}
'''

  prompt = \
f'''# Question
{question}

# Answer
{answer}
'''

  # print(system)
  # print(answer)

  response = client.chat.completions.create(
    model=openai_model,
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  parsed_content = json.loads(response.choices[0].message.content)
  # print (parsed_content)
  return parsed_content

def build_diagram(question, answer, diagram_type, diagram_type_reason, documentation):
  system = \
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

  prompt = \
f'''# Question - Question from the user
{question}

# Answer - Answer given to the user
{answer}

# DiagramType - Diagram type that you must use and why it was chosen
Diagram Type: {diagram_type}
Reasoning: {diagram_type_reason}

# DiagramTypeDocs - Syntax documentation to build the diagram
{documentation}

# Your output'''

  # Writing on a file to check if prompt is format correctly
  with open('prompt.md', 'w') as file:
    file.write(system)
    file.write("\n")
    file.write(prompt)

  response = client.chat.completions.create(
    model=openai_model,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  res = response.choices[0].message.content
  # print (res)
  return {"diagram": res, "system": system, "prompt": prompt}


def validate_diagram_with_mermaid(diagram_code):
  try:
      # Run the Node.js validation script
      process = subprocess.run(
          ['node', 'validate_mermaid.js'], 
          input=diagram_code, 
          text=True, 
          capture_output=True, 
          check=True
      )
      
      if process.stdout.strip() == 'Syntax is correct.':
          return True
      else:
          # print("Error:", process.stderr.strip())
          return False
  except subprocess.CalledProcessError as e:
      # Handle errors in case the Node.js script failed to run
      print(f'Node.js script failed: {e.stderr}')
      return False

def convert_to_training_format(system_content, user_content, assistant_content):
  return {
      "messages": [
          {"role": "system", "content": system_content},
          {"role": "user", "content": user_content},
          {"role": "assistant", "content": assistant_content}
      ]
  }

# Open and read the JSON file
with open(input_filename, 'r', encoding='utf-8') as file:
    # Load JSON content from the file
    full_data = json.load(file)
    
    data = full_data
    # Limit the numbers of objs for testing purposes (for testing)
    # data = full_data[:10]

# Initialize a list to store the updated objects
filtered_data = []

# Get the total number of data points
total_questions = len(data)

failed_diagram_count = 0
failed_diagram_count_lock = threading.Lock()

### Main Loop

def process_question(obj):
  global failed_diagram_count 

  # Get the question text from the object
  question = obj.get("question", "")
  answer = obj.get("answer", "")
  
  # Query GPT to check if it's a programming-related question (API call)
  is_programming = is_programming_question(question)

  print("Is Programming:", is_programming)
  # If it's not a programming-related question, skip the rest of the loop
  if not is_programming:
      return None

  # Query GPT to get the diagram type (API call)
  diagram_type_info = get_diagram_type(question, answer)
  diagram_type = diagram_type_info["diagramType"]
  diagram_type_reason = diagram_type_info["thoughts"]
  print("Diagram Type:", diagram_type)
  # print("Diagram Type Reason:", diagram_type_reason)

  # Get the corresponding documentation for the determined diagram type
  documentation = diagram_docs.get(diagram_type, "")
  
  # Add the gpt responses to the object
  obj['is_programming'] = is_programming
  obj['diagram_type'] = diagram_type

  # A loop to ensure a valid diagram is generated
  MAX_ATTEMPTS = 5  # set a maximum number of attempts to prevent infinite loops
  attempts = 0
  while attempts < MAX_ATTEMPTS:
      # Query GPT to build the diagram based on diagram type, diagram type documentation, question and answer (API call)
      final_diagram_res = build_diagram(question, answer, diagram_type, diagram_type_reason, documentation) 

      # print("Diagram:", final_diagram_res['diagram'])
      
      valid = validate_diagram_with_mermaid(final_diagram_res['diagram'])
      if valid:
          print('Valid Mermaid diagram')
          obj['system'] = final_diagram_res['system']
          obj['prompt'] = final_diagram_res['prompt']
          obj['diagram'] = final_diagram_res['diagram']
          return obj
      else:
          print('Invalid Mermaid diagram. Attempting to regenerate...')
          attempts += 1
          with failed_diagram_count_lock:  # Use the lock to protect this section
            failed_diagram_count += 1
  
  # If failed to generate diagram
  print(f"Failed to generate a valid diagram after {MAX_ATTEMPTS} attempts.")
  print(f'Failed diagram generations so far: {failed_diagram_count}')
  return None


# How many jobs to run in parallel
workers = 10
processed_count = 0

# Initialize the ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=workers) as executor:
    # Submit the tasks to the executor
    future_to_obj = {executor.submit(process_question, obj): obj for obj in data}
    
    # Process the results as they complete
    for future in as_completed(future_to_obj):
        # Get the result from the future
        result = future.result()
        processed_count += 1
        print(f'Progress: {processed_count}/{total_questions} questions processed.')
        if result is not None:
          filtered_data.append(result)

# Write everything to a file that can be used for inspecting the entire data
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4)

# Write the dataset file that will be used for fine-tuning an OpenAI model
with open(dataset_filename, 'w', encoding='utf-8') as file:
    for entry in filtered_data:
        # Only proceed if there is a diagram field and it is not empty
        if entry.get('diagram'):
            messages = [
                {"role": "system", "content": entry['system']},  # The system message used
                {"role": "user", "content": entry['prompt']},  # The prompt used
                {"role": "assistant", "content": entry['diagram']}  # The diagram generated
            ]
            # Create a dictionary for the JSON Lines item
            jsonl_item = {"messages": messages}
            # Write the JSON Lines item to file. Each item has to be followed by a newline "\n"
            file.write(json.dumps(jsonl_item, ensure_ascii=False) + '\n')

print(f'Total failed diagram generations: {failed_diagram_count}')
print(f'Dataset created and saved to {dataset_filename}')

# Split the dataset
with open(dataset_filename, 'r', encoding='utf-8') as file:
  data = [json.loads(line) for line in file]

# Split the data into training and testing datasets
# Using a 80-20 split for training and testing
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Define filenames for the training and testing dataset
train_filename = '../data/training_dataset.jsonl'
test_filename = '../data/testing_dataset.jsonl'

# Write the training dataset to a file
with open(train_filename, 'w', encoding='utf-8') as file:
  for entry in train_data:
    file.write(json.dumps(entry, ensure_ascii=False) + '\n')

# Write the testing dataset to a file
with open(test_filename, 'w', encoding='utf-8') as file:
  for entry in test_data:
    file.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f'Training dataset created and saved to {train_filename}')
print(f'Testing dataset created and saved to {test_filename}')
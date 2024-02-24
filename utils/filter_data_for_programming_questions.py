# This script filters the provided dataset to extract the user questions that are programming related

import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the filenames
input_filename = '../data/mermaid_dataset_public.json'
output_filename = '../data/mermaid_dataset_public_programming_filtered.json'

# Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI()

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

# Function to ask GPT what is the best diagram type for the question/answer pair. Limiting the model to use a list of diagram types
def get_diagram_type(question, answer):
  system = '''Based on the #Question and #Answer you'll decide what is the appropriate MermaidJS diagram type to use. You must select 1 of the following types:
  "flowchart" - Flowcharts are composed of nodes (geometric shapes) and edges (arrows or lines). The Mermaid code defines how nodes and edges are made and accommodates different arrow types, multi-directional arrows, and any linking to and from subgraphs
  "sequenceDiagram" - A Sequence diagram is an interaction diagram that shows how processes operate with one another and in what order
  "classDiagram" - The class diagram is the main building block of object-oriented modeling. It is used for general conceptual modeling of the structure of the application, and for detailed modeling to translate the models into programming code. Class diagrams can also be used for data modeling. The classes in a class diagram represent both the main elements, interactions in the application, and the classes to be programmed
  "stateDiagram" - A state diagram is a type of diagram used in computer science and related fields to describe the behavior of systems. State diagrams require that the system described is composed of a finite number of states; sometimes, this is indeed the case, while at other times this is a reasonable abstraction
  "erDiagram" - An entity-relationship model (or ER model) describes interrelated things of interest in a specific domain of knowledge. A basic ER model is composed of entity types (which classify the things of interest) and specifies relationships that can exist between entities (instances of those entity types)

  Reply in the following JSON format: {"diagramType": "flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram"}
  '''
  prompt = f'''#Question
  {question}

  #Answer
  {answer}
  
  '''
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  parsed_content = json.loads(response.choices[0].message.content)
  # print (parsed_content)
  return parsed_content["diagramType"]

# Open and read the JSON file
with open(input_filename, 'r', encoding='utf-8') as file:
    # Load JSON content from the file
    full_data = json.load(file)
    
    # Limit the numbers of objs for testing purposes
    data = full_data[:10] if len(full_data) > 50 else full_data

# Initialize a list to store the updated objects
filtered_data = []

# Get the total number of data points
total_questions = len(data)

# Iterate over each question in the data
for index, obj in enumerate(data):
    # Get the question text from the object
    question = obj.get("question", "")
    answer = obj.get("answer", "")
    
    # Query GPT to check if it's a programming-related question
    is_programming = is_programming_question(question)

    # Query GPT to get the diagram type
    diagram_type = get_diagram_type(question, answer)
    
    # Add the OpenAI response to the object
    obj['is_programming'] = is_programming
    obj['diagram_type'] = diagram_type
    
    # Update the filtered data list with the modified object
    filtered_data.append(obj)

    # Print the current progress
    print(f'Progress: {index+1}/{total_questions} questions processed.')

# Write the updated objects to a new file
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4)

print(f'Dataset filtered and saved to {output_filename}')

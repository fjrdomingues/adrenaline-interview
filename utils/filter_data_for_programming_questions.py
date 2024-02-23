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

# Function to ask GPT-3.5-turbo if a question is programming-related
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

# Open and read the JSON file
with open(input_filename, 'r', encoding='utf-8') as file:
    # Load JSON content from the file
    data = json.load(file)

# Initialize a list to store the updated objects
filtered_data = []

# Get the total number of data points
total_questions = len(data)

# Iterate over each question in the data
for index, obj in enumerate(data):
    # Get the question text from the object
    question = obj.get("question", "")
    
    # Query GPT-3.5-turbo to check if it's a programming-related question
    is_programming = is_programming_question(question)
    
    # Add the OpenAI response to the object
    obj['is_programming'] = is_programming
    
    # Update the filtered data list with the modified object
    filtered_data.append(obj)

    # Print the current progress
    print(f'Progress: {index+1}/{total_questions} questions processed.')

# Write the updated objects to a new file
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4)

print(f'Dataset filtered and saved to {output_filename}')

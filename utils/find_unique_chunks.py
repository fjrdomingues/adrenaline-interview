# To help visualizing the dataset provided

import json

# Define the filename
filename = '../data/mermaid_dataset_public.json'

# Initialize an empty set to keep track of unique source chunk types
unique_source_chunk_types = set()

# Open and read the JSON file
with open(filename, 'r', encoding='utf-8') as file:
    # Load JSON content from the file
    data = json.load(file)

    # Count the total number of objects in the dataset
    total_objects = len(data)
    
    # Iterate over each object in the JSON array
    for obj in data[:500]:  # Limiting to the first 100 objects
        # Check if 'source_chunks' key exists in the object
        if 'source_chunks' in obj:
            # Iterate over each source chunk
            for chunk in obj['source_chunks']:
                # Add the type of the source chunk to the unique types set
                unique_source_chunk_types.add(chunk['type'])

# Output the unique source chunk types found in the file
print(f'Unique source chunk types: {unique_source_chunk_types}')

# Output the total number of objects in the dataset
print(f'Total number of objects (questions) in the dataset: {total_objects}')

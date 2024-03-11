"""
To understand how the dataset looks at the moment
"""

import json

# Path to the JSON file
file_path = 'mermaid_dataset_enhanced.json'

# Read the json file
with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize counters
total_items = 0
initially_valid_diagrams = 0  # Counter for diagrams valid from the start
fixed_diagrams = 0            # Counter for diagrams fixed later
invalid_diagrams = 0          # Counter for diagrams still invalid

# Iterate over the items to count initially valid and fixed diagrams
for item in data:
    total_items += 1
    if item.get('is_diagram_valid'):
        initially_valid_diagrams += 1
    elif item.get('diagram_fixed'):
        fixed_diagrams += 1
    else:
        invalid_diagrams += 1

# Assume that all initially valid and fixed diagrams are valid now
valid_diagrams = initially_valid_diagrams + fixed_diagrams
# Calculate percentages
valid_diagrams_percentage = (valid_diagrams / total_items) * 100 if total_items > 0 else 0
invalid_diagrams_percentage = (invalid_diagrams / total_items) * 100 if total_items > 0 else 0
fixed_diagrams_percentage = (fixed_diagrams / (invalid_diagrams + fixed_diagrams)) * 100 if total_items > 0 else 0

# Print stats
print(f'Number of items: {total_items}')
print(f'Number of initially valid diagrams: {initially_valid_diagrams}')
print(f'Number of diagrams fixed: {fixed_diagrams}')
print(f'Number of invalid diagrams: {invalid_diagrams}')
print(f'Percentage of valid diagrams (initially valid + fixed): {valid_diagrams_percentage:.2f}%')
# print(f'Percentage of invalid diagrams: {invalid_diagrams_percentage:.2f}%')
print(f'Percentage of diagrams that we could fix: {fixed_diagrams_percentage:.2f}%')

# This script is used to valid the diagram on the training set before beginning training. Making sure that we don't feed garbage

import re
import subprocess
import jsonlines

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

def main():
    # Open the JSON lines file and process each entry
    with jsonlines.open('../data/new_dataset_full.jsonl') as reader:
        line_number = 0  # Initialize line number counter
        for obj in reader:
            line_number += 1  # Increment line number with each new object from the reader
            # Extract messages from the entry
            messages = obj['messages']
            
            # Loop through messages to find the "assistant" message containing the diagram
            for message in messages:
                if message['role'] == 'assistant':
                    diagram_content = message['content']
                    if validate_diagram(diagram_content):
                        print(f"Diagram is valid. (Line {line_number})")
                    else:
                        print(f"Diagram is invalid or could not be processed. (Line {line_number})")
                    break  # Stop after processing the "assistant" message


if __name__ == '__main__':
    main()
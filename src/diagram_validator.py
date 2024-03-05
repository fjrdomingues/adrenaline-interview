import subprocess
import re

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
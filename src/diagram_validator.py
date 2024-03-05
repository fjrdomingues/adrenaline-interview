import subprocess
import re

# Function to validate a MermaidJS diagram
def validate_diagram(code, is_markdown=True):
    try:
        diagram_code = ""
        if is_markdown:
            # Extract the Mermaid code block from Markdown (assuming it's well-formed)
            match = re.search(r'```mermaid([^`]*)```', code, re.DOTALL)
            if not match:
                print("No valid Mermaid diagram code block found.")
                return False
            diagram_code = match.group(1).strip()  # Extracted Mermaid code
        else:
            # Use the entire code as the Mermaid diagram code
            diagram_code = code.strip()
        
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

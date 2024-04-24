import subprocess
import re
import requests
import time


# Function to validate a MermaidJS diagram
def validate_diagram_cli(code, is_markdown=True):
    try:
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

# Function to validate a MermaidJS diagram using API
def validate_diagram(diagram_definition):
    url = 'http://192.168.1.75:8080/validate'
    payload = {"definition": diagram_definition}

    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        # print(result)
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        # print(f"Elapsed time: {elapsed_time:.2f} seconds")  # Print the elapsed time
        return result.get('is_valid'), result.get('error_message')
    except requests.exceptions.RequestException as e:
        print("RequestException:", e)
        elapsed_time = time.time() - start_time  # Calculate elapsed time on error
        # print(f"Elapsed time on failure: {elapsed_time:.2f} seconds")
        return False, str(e)

if __name__ == "__main__":
    example_diagram_code =  """
graph TD
A(#34;Ethical Considerations#34;) -->|shape business practices| B(#34;Compliance and Regulations#34;)
A -->|maintaining trust| C(#34;Corporate Social Responsibility #40;CSR#41;#34;)
A -->|transparency in dealings| D(#34;Transparency and Accountability#34;)
A -->|negative consequences for stakeholders| E(#34;Impact on Stakeholders#34;)
B -->|avoid legal issues| D
C -->|promoting ethical labor practices| E
D -->|commitment to integrity| C
E -->|protecting interests of stakeholders| A
"""
    valid = validate_diagram(example_diagram_code)
    print("Is the diagram valid?", valid)
import subprocess
import re

# Function to validate a MermaidJS diagram
def validate_diagram(code, is_markdown=True):
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

if __name__ == "__main__":
    example_diagram_code = """
graph TD
  Flask(Flask: Python microframework) --> Routes
  Flask --> Decorators["Decorators &#40;@app.route&#40;&#41;&#41;"]
  Flask --> ViewFunctions[View Functions]
  Flask --> HTMLTemplates[HTML Templates]

  Routes --> |"Define URLs"| Decorators
  Decorators --> |"Map to"| ViewFunctions
  ViewFunctions --> |"Execute & Render"| HTMLTemplates
  
  HTMLTemplates --> |"Dynamic content"| RenderTemplate["render_template"]
  ViewFunctions --> RenderTemplate
  
  Flask --> VirtualEnvironment[Virtual Environment]
  VirtualEnvironment --> |"Isolates dependencies"| ProjectStructure[Project Structure]

  ProjectStructure --> |"Organizes"| Code[Python code]
  ProjectStructure --> |"Separates"| Resources["Resources &#40;HTML, etc.&#41;"]    """
    valid = validate_diagram(example_diagram_code)
    print("Is the diagram valid?", valid)
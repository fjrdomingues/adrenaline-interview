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
    example_diagram_code = "graph TD\n  A[AP_INVOICE_PAYMENTS_ALL Table] --> B[Payment Status Fields]\n  A --> C[Payment Date and Time Fields]\n  A --> D[Discount Information Fields]\n  A --> E[Payment Currency and Conversion Fields]\n  A --> F[Remit-To Address Fields]\n  B --> B1[Processed Status]\n  B --> B2[Pending Status]\n  B --> B3[Completed Status]\n  C --> C1[Payment Date]\n  C --> C2[Payment Time]\n  D --> D1[Discount Taken]\n  D --> D2[Lost Discounts]\n  E --> E1[Payment Currency]\n  E --> E2[Conversion Rates]\n  F --> F1[Remit-To Address ID]"
    valid = validate_diagram(example_diagram_code)
    print("Is the diagram valid?", valid)
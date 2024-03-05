import re
import html

def fix_mermaid_syntax(diagram_text):
    # Regular expression pattern to match parentheses within square brackets
    pattern = re.compile(r'\[([^]]*?\([^]]*?\)[^]]*?)\]')

    # Function to replace parentheses within square brackets
    def replace_parentheses(match):
        inner_text = match.group(1)
        fixed_text = html.escape(inner_text)
        fixed_text = (fixed_text.replace('(', '#40;')
                                .replace(')', '#41;'))
        return f'[{fixed_text}]'

    # Apply the replacement function to the diagram text
    fixed_diagram = re.sub(pattern, replace_parentheses, diagram_text)

    return fixed_diagram

if __name__ == "__main__":
  # Playground
  original_diagram = """
  flowchart TD
    A[Start] --> B{Input values}
    B --> C["1" N ( number of strips already placed)]
    B --> D[L (width of the wall)]
    B --> E[W (width of the wallpaper roll)]
    B --> F[Array of xi (coordinates of left ends of placed strips)]

    G[Variables used in the solution] --> H[count (to keep track of the number of wallpaper strips needed)]
    G --> I[prev (to keep track of the previous coordinate)]

    J[Calculation steps] --> K[Calculation of gap between coordinates]
    K --> L[Calculation of strips needed to cover the gap POWER * ^1]
    L --> M[Updating count and prev]
    
    M --> N[End]
  """

  fixed_diagram = fix_mermaid_syntax(original_diagram)
  print(fixed_diagram)

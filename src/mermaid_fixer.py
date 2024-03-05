import re
import html

def fix_mermaid_syntax(diagram_text):
    # Regular expression pattern to match the first instance of curly braces, parentheses, or square brackets
    pattern = re.compile(r'(\{[^{}]*\}|\([^()]*\)|\[[^\[\]]*\])')

    # Function to replace matched characters within curly braces, parentheses, or square brackets
    def replace_matched(match):
      match_text = match.group(0)
      # FIX: Keep the enclosing characters as they are and only replace the inner content
      start_char = match_text[0]
      end_char = match_text[-1]
      inner_text = match_text[1:-1]  # Extract the inner part
      
      # Escape the inner text by HTML entities to use in Mermaid
      fixed_inner_text = (html.escape(inner_text, quote=False)
                          .replace('{', '&#123;')
                          .replace('}', '&#125;')
                          .replace('(', '&#40;')
                          .replace(')', '&#41;')
                          .replace('[', '&#91;')
                          .replace(']', '&#93;'))
      # Reconstruct the original enclosing characters with the fixed inner content
      return f'{start_char}{fixed_inner_text}{end_char}'

    # Split the diagram into lines
    lines = diagram_text.strip().split('\n')

    # Process each line separately
    fixed_lines = []
    for line in lines:
        # Apply the pattern and replacement function to each line
        fixed_line = pattern.sub(replace_matched, line)
        fixed_lines.append(fixed_line)
    
    # Rejoin the lines into the full diagram text
    fixed_diagram = '\n'.join(fixed_lines)

    return fixed_diagram


if __name__ == "__main__":
  # Playground
  original_diagram = """
  flowchart TD
    A[Start] --> B{Input values}
    B --> C{"1" N ( number of strips already placed)}
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

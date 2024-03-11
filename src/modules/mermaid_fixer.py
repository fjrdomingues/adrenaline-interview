"""
This is a script that can fix some mermaid diagrams that were generated. In our original dataset it was able to fix 48% of the diagrams with bad syntax.
"""


import re
import html

def escape_brackets(s):
    pairs = {'{': '}', '[': ']', '(': ')', '|': '|'}
    opening = pairs.keys()
    closing = pairs.values()
    stack = []
    escaped_string = ""

    for char in s:
        if char in opening:
            if stack and (stack[-1] != '|' or char != '|'):
                # It's an inner bracket, escape it
                escaped_string += {
                    '{': '#123;',
                    '[': '#91;',
                    '(': '#40;',
                    '|': '#124;',
                    '"': '#34;',
                    "'": '#39;'
                }.get(char, char)
            else:
                escaped_string += char
            if char == '|' and stack and stack[-1] == '|':
                stack.pop()  # Pipe character behaves as both opening and closing
            else:
                stack.append(char)
        elif char in closing:
            if char == '|':
                # Handle pipe characters which serve as both opening and closing brackets
                if stack and stack[-1] == '|':
                    stack.pop()
                else:
                    stack.append(char)
                escaped_string += char
            else:
                if stack:
                    stack.pop()
                if stack:
                    # It's an inner bracket, escape it
                    escaped_string += {
                        '}': '#125;',
                        ']': '#93;',
                        ')': '#41;',
                        '"': '#34;',
                        "'": '#39;'
                    }[char]
                else:
                    escaped_string += char
        else:
            # Escape quotes that are not used as brackets
            if char in ['"', "'"]:
                escaped_string += {
                    '"': '#34;',
                    "'": '#39;'
                }[char]
            else:
                escaped_string += char

    return escaped_string


def fix_mermaid_syntax(input_string):
    # Split the string into lines
    lines = input_string.strip().split('\n')

    # Escape the brackets in each line
    processed_lines = [escape_brackets(line) for line in lines]

    # Join the lines back into a single string and return
    return '\n'.join(processed_lines)

if __name__ == "__main__":
  # Playground
  original_diagram = """
graph TD
  A[Start] --> B[Define Functions]
  B --> C[add#40;x, y#41;]
  B --> D[subtract#40;x, y#41;]
  B --> E[multiply#40;x, y#41;]
  B --> F[divide#40;x, y#41;]
  F --> G[Check if y is 0]
  G -->|Yes| H[Return "Cannot divide by zero!"]
  G -->|No| I[Return x / y]
  A --> J[Test the Calculator]
  J --> K[Set num1 = 10]
  J --> L[Set num2 = 5]
  J --> M[Print Results]
  M --> N[add#40;num1, num2#41;]
  M --> O[subtract#40;num1, num2#41;]
  M --> P[multiply#40;num1, num2#41;]
  M --> N[Use #34;signOut()#34;]
 """

  fixed_diagram = fix_mermaid_syntax(original_diagram)
  print(fixed_diagram)

"""
Extract a diagram from a markdown string
"""

import re

def extract_mermaid_code(markdown_text):
    """
    Extracts the Mermaid code from a block of Markdown text, with a second attempt for badly formatted blocks.
    
    Parameters:
    markdown_text (str): The Markdown text that potentially contains Mermaid or badly formatted Mermaid code blocks.

    Returns:
    str: The extracted Mermaid code, or an empty string if no Mermaid code is found.
    """
    # Regular expression to match correctly formatted Mermaid code blocks in Markdown
    mermaid_block_pattern = re.compile(r'```mermaid([^`]*)```', re.DOTALL)
    
    # Regular expression to match incorrectly formatted Mermaid code blocks with \`\`\`
    badly_formatted_pattern = re.compile(r'\\\`\\\`\\\`mermaid([^`]*)\\\`\\\`\\\`', re.DOTALL)
    
    # First attempt: Search for well-formatted Mermaid code blocks in the Markdown text
    match = mermaid_block_pattern.search(markdown_text)
    
    # If a well-formatted Mermaid code block is found, return the code inside it
    if match:
        return match.group(1).strip()
    
    # Second attempt: Search for badly formatted Mermaid code blocks in the Markdown text
    match = badly_formatted_pattern.search(markdown_text)
    
    # If a badly formatted Mermaid code block is found, return the code inside it
    if match:
        return match.group(1).strip()
    
    # If neither is found, return an empty string
    return ""

# This allows the module to be used as a script for quick tests
if __name__ == "__main__":
    # Sample test with a Markdown containing a Mermaid diagram
    sample_markdown = "```mermaid\ngraph TD\n    A[\u041a\u043e\u0434 JavaScript \u0434\u043b\u044f \u0432\u0435\u0431-\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b] --> B{\u0421\u0438\u043d\u0442\u0430\u043a\u0441\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043e\u0448\u0438\u0431\u043a\u0438}\n    B -->|\u041d\u0435\u0442| C[\u041a\u043e\u0434 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0438\u0440\u043e\u0432\u0430\u043d \u0441 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0430\u043c\u0438 \u0441\u043e\u0431\u044b\u0442\u0438\u0439 \u0438 \u0444\u0443\u043d\u043a\u0446\u0438\u044f\u043c\u0438]\n    C --> D[\u041b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0435\u0439]\n    D --> E[\u0412\u0445\u043e\u0434 \u0432 \u0441\u0438\u0441\u0442\u0435\u043c\u0443, \u0437\u0430\u043a\u0430\u0437\u044b, \u043f\u043e\u0438\u0441\u043a, \u043e\u0446\u0435\u043d\u043a\u0438, \u043e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c, \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0430, \u043a\u043e\u0440\u0437\u0438\u043d\u0430, \u043e\u043f\u043b\u0430\u0442\u0430, \u0444\u043e\u0440\u043c\u044b]\n\n    A --> F{\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0439}\n    F -->|\u041d\u0435\u0442 \u044f\u0432\u043d\u043e\u0439 \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438| G[\u0421\u043b\u0435\u0434\u0443\u0435\u0442 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e\u043c\u0443 \u043f\u043e\u0434\u0445\u043e\u0434\u0443]\n    G --> H[\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0432\u0437\u0430\u0438\u043c\u043e\u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f\u043c\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f]\n\n    A --> I{\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043e\u0448\u0438\u0431\u043e\u043a}\n    I -->|\u041d\u0435\u0442 \u044f\u0432\u043d\u044b\u0445 \u043c\u0435\u0445\u0430\u043d\u0438\u0437\u043c\u043e\u0432| J[\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u044e\u0442\u0441\u044f alert() \u0434\u043b\u044f \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439 \u043e\u0431 \u043e\u0448\u0438\u0431\u043a\u0430\u0445]\n    J --> K[\u0424\u043e\u043a\u0443\u0441 \u043d\u0430 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0438 \u0432\u0437\u0430\u0438\u043c\u043e\u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f\u043c\u0438 \u0438 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0438 \u0441\u043e\u0434\u0435\u0440\u0436\u0438\u043c\u043e\u0433\u043e]\n\n    E -.-> H\n    H -.-> K\n```"
    print(extract_mermaid_code(sample_markdown))

import re

def extract_mermaid_code(markdown_text):
    """
    Extracts the Mermaid code from a block of Markdown text.
    
    Parameters:
    markdown_text (str): The Markdown text that potentially contains Mermaid code blocks.

    Returns:
    str: The extracted Mermaid code, or an empty string if no Mermaid code is found.
    """
    # Regular expression to match Mermaid code blocks in Markdown
    mermaid_block_pattern = re.compile(r'```mermaid([^`]*)```', re.DOTALL)
    
    # Search for Mermaid code blocks in the Markdown text
    match = mermaid_block_pattern.search(markdown_text)

    # If a Mermaid code block is found, return the code inside it
    if match:
        return match.group(1).strip()
    
    return ""

# This allows the module to be used as a script for quick tests
if __name__ == "__main__":
    # Sample test with a Markdown containing a Mermaid diagram
    sample_markdown = """
    Here is an example Mermaid diagram in Markdown:

    ```mermaid
    graph TD;
        A-->B;
        A-->C;
        B-->D;
        C-->D;
    ```

    The above should be extracted.
    """
    print(extract_mermaid_code(sample_markdown))

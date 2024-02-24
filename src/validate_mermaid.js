import mermaid from "mermaid";

const removeMarkdownWrapper = (string) => {
  // Remove Markdown Mermaid wrapper ```mermaid\n and the closing ```
  return string.replace(/^```mermaid\n?/, '').replace(/\n?```$/, '');
};

const checkMermaidSyntax = async (string) => {
  try {
    // Remove Markdown wrapper if present before parsing
    const mermaidString = removeMarkdownWrapper(string);
    await mermaid.parse(mermaidString);
    process.stdout.write('Syntax is correct.\n');
  } catch (error) {
    process.stderr.write(`Syntax error in Mermaid diagram: ${error.message}\n`);
  }
};

// Read the entire input from stdin
let data = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', (chunk) => {
  data += chunk;
});
process.stdin.on('end', () => {
  // When all data is received, validate the syntax.
  checkMermaidSyntax(data.trim());
});

process.stdin.resume();

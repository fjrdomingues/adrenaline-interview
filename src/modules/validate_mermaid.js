import mermaid from "mermaid";

const checkMermaidSyntax = async (string) => {
  console.log(string)
  try {
    await mermaid.parse(string);
    process.stdout.write('Syntax is correct.\n');
    process.exitCode = 0; // Explicitly set exit code to 0 on success
  } catch (error) {
    process.stderr.write(`Syntax error in Mermaid diagram: ${error.message}\n`);
    process.exitCode = 1; // Set a non-zero exit code on error
    // Optionally, you could call process.exit(1) here to immediately terminate the process
  }
};

// Read the entire input from stdin
let data = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', (chunk) => {
  data += chunk;
});
process.stdin.on('end', () => {
  checkMermaidSyntax(data.trim()).then(() => {
    // The process will exit with the code set above once the promise resolves
    process.exit(); // This will cause the process to exit with the code set in checkMermaidSyntax
  });
});

process.stdin.resume();

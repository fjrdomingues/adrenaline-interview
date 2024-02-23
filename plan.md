# Goals of this project
- Get 100% correct syntax on generated diagrams
- Improve quality of diagrams

# Plan
- Generate dataset for training
  - Use dataset that was provided and filter questions that are programming related (using GPT)
  - Ask GPT to choose the appropriate diagram type for the each answer
  - Ask GPT to generate the diagram based on the diagram type and its documentation
  - Evaluate output for valid syntax, if incorrect, repeat
  - (for later) Further refine the answer to improve quality
- Use generated dataset for fine-tuning a model
  - Include in prompt:
    - Diagram type
    - answer context
    - Diagram type documentation
- Evaluate performance of fine-tuned model:
  - Check for syntax validity
  - Ask GPT-4 to evaluate
- Try and compare different approaches
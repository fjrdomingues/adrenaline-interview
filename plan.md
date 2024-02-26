# Goals of this project
- Get 100% correct syntax on generated diagrams
- Improve quality of diagrams

# Plan
- Generate dataset for training
  - ✅ Use dataset that was provided and filter questions that are programming related (using GPT)
  - ✅ Ask GPT to choose the appropriate diagram type for the each answer
  - ✅ Ask GPT to generate the diagram based on the diagram type and its documentation
  - ✅ Evaluate output for valid syntax, if incorrect, repeat
  - 🕚 (for later) Further refine the answer to improve quality and syntax
    - feed the validation error back to gpt to fix
    - provide better documentation or more examples of valid syntax
    - instruct the model to simplify the syntax
    - Ask GPT to evaluate the diagram
    - Ask GPT to generate a description of a diagram and have a model just creating the syntax❗
- Generate dataset for fine-tuning an openAI model
  - Include in prompt:
    - Diagram type
    - question and answer context
    - Diagram type documentation (should we include the docs or not? - probably not) (ok to have the docs if in inference we don't need to send the docs)
- Evaluate performance of fine-tuned model:
  - Check for syntax validity (how many failed attempts with GPT-4 vs with fine-tuned model?)
  - Ask GPT-4 to evaluate a subset
  - Choose random scenarios and documentation a subjective comparison between results of both models

- Try and compare different approaches
  - Fine-tune an OSS model like mistral or other models that are good with code
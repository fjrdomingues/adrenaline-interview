# Generating system diagrams with LLMs

At Adrenaline, we're building tools for understanding large codebases. One of the best ways to learn a new codebase is to visualize it. Engineers do this all the time when they explain concepts on whiteboards or propose code changes using design documents. With LLMs, these visualizations can be generated on-the-spot and catered to a specific prompt. Adrenaline achieves this functionality right now in production by prompting GPT-4 to generate a diagram in MermaidJS syntax, given a query and some relevant code chunks.

But this approach has two problems: 

1. GPT-4 frequently generates invalid MermaidJS syntax
2. Diagrams can be low-quality in a variety of ways, such as being too abstract or too detailed, leaving out important information, or even using the wrong diagram type (e.g. a sequential vs. flow diagram)

Edit this repository with your own approach at solving these two problems. You have a lot of liberty here. For example, to improve the syntax accuracy you may want to fine-tune either an OpenAI model or an open-source one. To improve quality, you may want to generate a training set using multiple LLM calls to construct diagrams.

The main objective here is to beat GPT-4 in both syntax accuracy and diagram quality.

### To make a submission:

1. Fork the repository
2. Make a PR with your changes _in your repository_
3. Email _your_ repository to jonathan@useadrenaline.com

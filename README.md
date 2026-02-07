# Iterative Synthesis Loop (ISL)

An intelligent code and documentation generation system that combines Large Language Models (LLMs) with prompt engineering workflows. ISL enables iterative refinement of software through structured prompts, LLM-powered synthesis, and version control.

## Overview

Iterative Synthesis Loop automates the generation of code and documentation by:
- **Templating**: Create markdown prompt templates with code file inclusions
- **LLM Integration**: Call OpenAI or compatible LLM APIs to generate/refine code
- **Iterative Workflow**: Organize projects with separate folders for raw and final outputs
- **Version Control**: Track all iterations with built-in Git integration
- **Web UI**: Manage projects through an intuitive web interface

## Features

- 🤖 **LLM-Powered Code Generation**: Use prompts to generate Python code, documentation, UML diagrams, and more
- 📝 **Smart Markdown Templating**: Include code files in prompts with `<insert>` tags for dynamic prompt composition
- 🔄 **Iterative Refinement**: Organize workflows with separate raw and final output folders
- 📦 **Project Management**: Create, open, and manage multiple projects
- 🌳 **Version Control**: Built-in Git integration for tracking iterations across all project folders
- 🌐 **Web Interface**: Manage projects and compilation from a browser-based UI
- ⚙️ **Configuration-Driven**: Use JSON configuration for API and loop settings

## Quick Start

### Prerequisites

- Python 3.8+
- FastAPI
- An OpenAI API key (or compatible LLM endpoint)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd iterative-synthesis-loop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Create a .env file in the project root
echo "API_KEY=your_openai_api_key_here" > .env
```

4. Start the server:
```bash
python server.py
```

5. Open your browser and navigate to `http://localhost:8000`

## Project Structure

```
project-root/
├── .api.json                 # API configuration (URL, headers, model settings)
├── .isl.json                 # ISL loop configuration
├── prompt-raw/               # Raw prompts (input)
│   ├── .api.json            # API config override
│   ├── .loop.json           # Loop config override
│   ├── .template-prompt.md  # Main prompt template
│   └── raw-prompt.md        # Reference for raw prompts
├── prompt-final/             # Refined prompts (output)
│   ├── .api.json
│   ├── .loop.json
│   ├── class-diagram.uml    # Generated UML diagrams
│   ├── package-diagram.uml
│   ├── usecase-diagram.uml
│   └── readme.md            # Generated documentation
├── code-raw/                 # Raw code (input)
│   ├── .api.json
│   ├── .loop.json
│   └── main.py              # Code files to reference in prompts
└── code-final/               # Refined code (output)
```

## Usage

### 1. Via Web UI

- **Open Project**: File → Open Project (select a folder)
- **Create Project**: File → New Project (creates folder structure with template)
- **Compile**: Compile → Compile (runs `isl.py` on selected folders)
- **Version Control**: Windows → Git (view and manage versions)
- **Terminal**: Windows → Terminal (open integrated terminal)

### 2. Via CLI

Run ISL on a specific folder:

```bash
python isl.py path/to/prompt-raw
```

With custom configuration:

```bash
python isl.py path/to/prompt-raw \
  -a path/to/.api.json \
  -l path/to/.loop.json
```

### 3. Markdown Template Syntax

Include code files in prompts using the `<insert>` tag:

```markdown
# Code Generation Prompt

Analyze the following code:

<insert src="input_handler.py"></insert>

Please refactor this code for better performance.
```

The template processor will replace the `<insert>` tag with the file contents before sending to the LLM.

## Configuration Files

### .api.json

```json
{
  "url": "https://api.openai.com/v1/chat/completions",
  "method": "POST",
  "timeout": 30,
  "api_key_env": "API_KEY",
  "headers": {
    "Content-Type": "application/json"
  },
  "payload": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2048
  },
  "system": "You are an expert software engineer..."
}
```

### .loop.json

```json
{
  "out_path": "."
}
```

## File Structure

| File | Purpose |
|------|---------|
| `server.py` | FastAPI web server with REST API for file/project management |
| `isl.py` | CLI tool that executes the synthesis loop on a project folder |
| `api.py` | LLM API client handling requests to OpenAI or compatible endpoints |
| `md.py` | Markdown template processor for `<insert>` tag substitution |
| `index.html` | Web UI for the application |
| `requirements.txt` | Python dependencies |

## Workflow Example

Here's a typical workflow for generating code:

1. **Create a project structure** with separate folders for raw and final outputs
2. **Write a raw prompt** in `prompt-raw/.template-prompt.md` using markdown syntax
3. **Include code files** using `<insert src="file.py"></insert>` tags
4. **Configure API settings** in `.api.json` with model preferences
5. **Run compilation** to send the prompt to the LLM
6. **Review generated code** in the output folder
7. **Commit to Git** to version the iteration
8. **Refine and iterate** by adjusting prompts and rerunning

## Example: Freefall Simulator

The `example/` folder contains a complete freefall physics simulator:

```
example/
├── code-raw/
│   ├── main.py
│   ├── input_handler.py
│   ├── freefall_simulator.py
│   └── output_formatter.py
├── prompt-raw/
│   ├── .api.json
│   ├── .template-prompt.md
│   └── description.md
└── prompt-final/
    ├── class-diagram.uml
    ├── package-diagram.uml
    ├── usecase-diagram.uml
    └── readme.md
```

To run the freefall example:

```bash
cd example
python code-raw/main.py
```

## API Endpoints

The FastAPI server provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the web UI |
| `/system_pick_folder` | GET | Open native folder picker |
| `/list_files` | POST | List files in a directory |
| `/read_file` | POST | Read file contents |
| `/write_file` | POST | Write or update a file |
| `/create_project` | POST | Create a new project structure |
| `/list_projects` | GET | List all projects |
| `/compile` | POST | Run ISL on a folder |

## Environment Variables

```bash
# Required: LLM API key
API_KEY=sk-...

# Optional: Custom API endpoint
API_URL=https://api.openai.com/v1/chat/completions
```

## Version Control

ISL integrates with Git for tracking iterations:

- Each folder (prompt-raw, prompt-final, code-raw, code-final) can be a separate Git repository
- Use the UI to view commit history across all folders
- Automatically initialize Git repos when creating new projects

## Requirements

```
fastapi
pydantic
python-dotenv
requests
```

## Contributing

Contributions are welcome! Please follow these guidelines:
- Test your changes with the example project
- Update documentation for new features
- Submit pull requests with clear descriptions

## License

[Specify your license here]

## Support

For issues and feature requests, please [specify how to report them].

## Acknowledgments

This project demonstrates the power of combining LLMs with structured prompt engineering for automated software development and documentation generation.

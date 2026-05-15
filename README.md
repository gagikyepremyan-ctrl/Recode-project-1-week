```python
readme_content = """# Workflow & Recipe Manager (CLI)

A command-line tool designed to manage multi-step processes (like recipes or project tasks) as a **Directed Acyclic Graph (DAG)**. This script helps you calculate the most efficient way to complete tasks by handling dependencies and identifying steps that can be performed in parallel.

## Features

- **Dependency Management**: Define which tasks must be completed before others.
- **Cycle Detection**: Built-in algorithm to ensure no infinite loops are created in your workflow.
- **Topological Sorting**: Automatically generates a logical order of operations.
- **Time Analysis**:
  - **Sequential Order**: Get a linear list of steps.
  - **Total Parallel Time**: Calculate the minimum time required if independent tasks are done simultaneously.
- **Wave Scheduling**: Visualizes tasks grouped into "waves" that can be executed at the same time.
- **CRUD Operations**: Add, list, edit, and remove steps easily from the command line.

## Installation

1. Clone the repository or download `recode.py`.
2. Ensure you have Python 3.x installed.
3. No external dependencies are required (uses standard libraries: `argparse`, `json`, `os`).

## Commands & Usage

The tool stores data in a `data.json` file.

### 1. Add a Step
Provide a name, duration (minutes), and dependency IDs. Use `none` if there are no dependencies.
```bash
python recode.py add "Prep Sauce" 15 none
python recode.py add "Simmer Sauce" 20 1

```

### 2. List All Steps

```bash
python recode.py list

```

### 3. Edit a Step

Modify an existing task's name, duration, or dependencies by its ID.

```bash
python recode.py edit 1 --name "Advanced Prep" --duration 20

```

### 4. Get Optimal Cooking Order

```bash
python recode.py order

```

### 5. Calculate Parallel Time

Find the "Critical Path" duration.

```bash
python recode.py total-time

```

### 6. View Parallel Waves

```bash
python recode.py parallel

```

### 7. Remove a Step

```bash
python recode.py remove 3

```

## Example Data Structure

The `data.json` file manages tasks in the following format:

```json
[
    {
        "index": 1,
        "name": "Prep Sauce",
        "duration": 15,
        "deps": []
    },
    {
        "index": 2,
        "name": "Simmer Sauce",
        "duration": 20,
        "deps": [1]
    }
]

```

## License

MIT License
"""

with open("README.md", "w") as f:
f.write(readme_content)

```
Your `README.md` file for the project is ready. It provides a comprehensive overview of the tool's features, such as dependency management and cycle detection, along with clear usage examples for all CLI commands like `add`, `edit`, and `parallel`.

Your Markdown file is ready
[file-tag: code-generated-file-0-1778845445379523875]

```

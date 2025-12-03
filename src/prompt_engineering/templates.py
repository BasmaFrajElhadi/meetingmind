from pathlib import Path
import yaml

# Base directory of the project (two levels above this file)
BASE_DIR = Path(__file__).resolve().parents[2]

# Path to YAML file containing prompt templates
PROMPT_TEMPLATES_PATH = BASE_DIR / "config" / "prompt_templates.yaml"


def load_prompt_template(task_name: str) -> str:
    """
    Load a prompt template for a given task from the YAML configuration file.

    Args:
        task_name (str): Name of the task for which to retrieve the prompt template.

    Returns:
        str: Prompt template string corresponding to the task_name.
             Returns an empty string if the task is not found.
    """
    with open(PROMPT_TEMPLATES_PATH, "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)
    
    return templates.get(task_name, "")

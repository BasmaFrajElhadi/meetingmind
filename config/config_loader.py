import yaml
from pathlib import Path

BASE_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config"


def load_model_config():
    with open(BASE_CONFIG_PATH / "model_config.yaml", "r") as f:
        return yaml.safe_load(f)


def load_prompt_config():
    with open(BASE_CONFIG_PATH / "prompt_templates.yaml", "r") as f:
        return yaml.safe_load(f)
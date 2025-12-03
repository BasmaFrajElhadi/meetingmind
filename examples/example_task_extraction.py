import sys
import os

# --- Project path setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.analysis.task_extractor import TaskExtractor

sample_text = """
Sarah will finish the UI by Friday. Ahmed will deploy the backend by next Monday.
"""

task_extractor = TaskExtractor()
tasks = task_extractor.extract_tasks(sample_text)

print("\n--- Tasks ---\n")
print(tasks)

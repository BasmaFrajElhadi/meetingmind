import sys
import os

# --- Project path setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.analysis.summarizer import MeetingSummarizer

sample_text = """
Today we discussed the roadmap for Q4 and assigned tasks to the design team.
"""

summarizer = MeetingSummarizer()
summary = summarizer.summarize(sample_text)

print("\n--- SUMMARY ---\n")
print(summary)

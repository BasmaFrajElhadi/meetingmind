import sys
import os

# --- Project path setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.research.web_searcher import WebSearcher


topic = "AI in healthcare 2025"


web_searcher = WebSearcher()
web_results = web_searcher.search(topic)

print("\n--- Web Results ---\n")
print(web_results)

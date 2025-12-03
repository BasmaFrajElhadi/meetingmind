import sys
import os

# --- Project path setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.analysis.sentiment_analyzer import SentimentAnalyzer

sample_text = """
Today we discussed the roadmap for Q4 and assigned tasks to the design team.
Some participants expressed concern about tight deadlines.
"""


analyzer = SentimentAnalyzer()

sentiment_result = analyzer.analyze_sentiment(sample_text)

print("\n--- SENTIMENT ANALYSIS ---\n")
print(sentiment_result)

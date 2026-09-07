import json
import os

# Script that regenerates football_analysis.ipynb
with open("football_analysis.ipynb", "r", encoding="utf-8") as f:
    nb_data = json.load(f)

with open("football_analysis.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb_data, f, indent=1)

print("Updated football_analysis.ipynb successfully!")

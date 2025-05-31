#!/bin/zsh
cd "/Users/davidhu/Documents/python code/DI Capital website"
source .venv/bin/activate
python generate.py
git add docs/index.html
git commit -m "Update fund data: $(date '+%Y-%m-%d')"
git push origin main
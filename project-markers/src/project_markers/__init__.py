import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'project-markers.json'), encoding='utf-8') as file:
    project_markers = json.load(file)

sys.modules[__name__] = project_markers

import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'project_markers.json')) as file:
    project_markers = json.load(file)

sys.modules[__name__] = project_markers

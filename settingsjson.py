import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'example title'},
    {'type': 'options',
     'title': 'HSK Level',
     'desc': 'Choose the difficulty (HSK1 to HSK6)',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6']}])
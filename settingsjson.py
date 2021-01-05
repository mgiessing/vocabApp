import json

settings_json = json.dumps([
    {'type': 'options',
     'title': 'Select HSK level',
     'desc': 'Choose for an difficulty option',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6']
    }])
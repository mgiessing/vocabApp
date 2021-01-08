import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'example title'},
    {'type': 'options',
     'title': 'HSK Level',
     'desc': 'Choose the difficulty (HSK1 to HSK6)',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6']},
     {'type': 'options',
     'title': 'Quiz words',
     'desc': 'Amount of words asked in a quiz',
     'section': 'example',
     'key': 'wordsexample',
     'options': ['10', '20', '30', '40', '50']}
])
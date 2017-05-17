#Use this to add fields to JSON file


import json

with open('client_settings.json', 'w') as f:
    settings_dict = {'log_folder': 'log', 'countdown_time': 70, 'ip': '192.168.1.33', 'port': 5000}
    json.dump(settings_dict, f)
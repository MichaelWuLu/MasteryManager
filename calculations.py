import json
import os


def calculate_total_mastery_level():
    if not os.path.exists('temp/mastery.json'):
        return 0
    with open('temp/mastery.json', 'r') as json_file:
        data = json.load(json_file)
        cumulative = 0
        for dict in data:
            lvl = dict['championLevel']
            cumulative = cumulative + lvl
        return cumulative

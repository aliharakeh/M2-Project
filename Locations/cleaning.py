import os
import json
import re

LOCAL_DIR = os.path.dirname(__file__)

with open(f'{LOCAL_DIR}\\cities.json', 'r', encoding='utf-8') as cities_file:
    Cities = json.loads(cities_file.read())

with open(f'{LOCAL_DIR}\\cities_details.json', 'r', encoding='utf-8') as cities_file:
    Cities_Details = json.loads(cities_file.read())

PROBLEM_CHARS = r'[^\w\s]'

res = {}
for k, v in Cities.items():
    res[k] = {}
    for k1, v1 in v.items():
        res[k][k1] = []
        for c in v1:
            res[k][k1].append(re.sub(PROBLEM_CHARS, '', c).replace('  ', ' '))

with open('cities_v2.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(res, indent=2, ensure_ascii=False))

res = {}
for k, v in Cities_Details.items():
    new_key = re.sub(PROBLEM_CHARS, '', k)
    res[new_key] = {}
    for k1, v1 in v.items():
        if k1 == 'name':
            res[new_key][k1] = re.sub(PROBLEM_CHARS, '', v1).replace('  ', ' ')

        elif k1 == 'latin' or k1 == 'non-latin':
            if v1:
                res[new_key][k1] = []
                for v2 in v1:
                    res[new_key][k1].append(re.sub(PROBLEM_CHARS, '', v2).replace('  ', ' '))
            else:
                res[new_key][k1] = None

        else:
            res[new_key][k1] = v1

with open('cities_details_v2.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(res, indent=2, ensure_ascii=False))

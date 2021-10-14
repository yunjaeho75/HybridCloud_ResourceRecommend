import json
import csv

csvpath = './src/data/test-ml.csv'
jsonpath = './src/data/test-ml.json'

csvfile = open(csvpath, 'r')
jsonfile = open(jsonpath, 'w')

reader = csv.reader(csvfile)

import itertools
jsonarr = list(itertools.chain(*reader))
jsonarr = list(map(int, jsonarr))

data = dict()
data['label'] = 'cpu'
data['sequance'] = jsonarr
#json.dump(data, jsonfile, indent=4)
json.dump(data, jsonfile)

print(f'{csvpath} ---> {jsonpath}')
print('completed.')
import common
import json

s = common.generate_system()
json.dump(s, open("tmp.json", 'w'), indent=4, sort_keys=True)

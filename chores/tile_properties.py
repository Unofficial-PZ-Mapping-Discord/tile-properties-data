import json, yaml
from pathlib import Path


JAVA_INPUT = Path("pz-java-parser/out/tile_properties.json")
DATA_INPUT = Path("data/tile_properties.yaml")
OUTPUT = Path("out/tile_properties.json")


# load properties from java parser
with open(JAVA_INPUT) as f:
    data = json.load(f)


# load dataset
with open(DATA_INPUT) as f:
    property = yaml.safe_load(f)['objects']

# check provided data is not providing for a non-existing tile property
for name in data.keys():
    if name not in property:
        property[name] = data[name]
    else:
        property[name]['field'] = data[name]['field']

# copy #desc to description
for prop in property.values():
    if "#desc" in prop:
        ref = prop["#desc"]
        if ref not in data:
            print(f"Warning: description reference '{ref}' not found for property '{prop['field']}'")
            continue
        prop["description"] = property[ref]["description"]

# output
with open(OUTPUT, "w") as f:
    json.dump(property, f, indent=4)


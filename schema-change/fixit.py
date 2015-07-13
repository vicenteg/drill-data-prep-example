#!python

import json
import types

for filename in ("data/vince.json", "data/nikki.json"):
	# Read the file into memory.
	with file(filename) as infile:
		data = json.loads(infile.read())

	# Open and truncate the input file.
	with file(filename, "w") as outfile:
		# enumerate returns an incrementing integer with each iteration.
		# convenient way to keep track of the index into the list
		# we need to modify.
		for i,f in enumerate(data["favorite_foods"]):
			# Check if the value pointed to by "flavors" is of type
			# ListType.
		    if type(f["flavors"]) != types.ListType:
		    	# If it's not, then overwrite the value as a list.
				data["favorite_foods"][i]["flavors"] = [ f["flavors"] ]
		outfile.write(json.dumps(data))

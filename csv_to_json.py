__author__ = 'spousty'

import json

infile = open('US_CONCISE.csv', 'r')
outfile = open('gnis.json', 'w')

headersArray = infile.readline().rstrip().split(',')
i = 1
for line in infile:
    print i
    new_dict = {}
    point_array = []
    splitline = line.rstrip().split(',')
    for x in range(0, len(headersArray)):
        #if header = long put in first spot or if lat in second slot
        if ("LONG" == headersArray[x]):
            point_array.insert(0, float(splitline[x]))
        elif ("LAT" == headersArray[x]):
            point_array.insert(1, float(splitline[x]))
        else:
            new_dict[headersArray[x]] = splitline[x]
    coords = {'type': "Point", 'coordinates': point_array}
    new_dict["pos"] = coords

    #add the geoson to the dict
    json.dump(new_dict, outfile)
    outfile.write("\n")
    i = i + 1

outfile.close()
print "The End"
__author__ = 'spousty'

infile = open('US_CONCISE.csv', 'r')
outfile = open('gnis.json', 'w')

print(infile.readline())
for line in infile:
    splitline = line.rstrip().split(',')
    print splitline


print "The End"
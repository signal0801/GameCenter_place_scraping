
import sys
import csv
from pygeocoder import Geocoder
 
infile = open('in.csv', 'rt')
outfile = open('out.csv', 'wt')
 
try:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    geocoder = Geocoder()
     
    for row in reader:
        if len(row) > 0:
            try:
                result = geocoder.geocode(row[0], language='ja')
                 
                if len(result) > 0:
                    writer.writerow([row[0], result[0].coordinates[0], result[0].coordinates[1]])
            except:
                print(sys.exc_info()[0])
except:
    print(sys.exc_info()[0])
finally:
    infile.close()
    outfile.close()
 
print('geocoding finished!')

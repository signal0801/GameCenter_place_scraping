# -*- coding: utf-8 -*-
import sys
import csv
import sqlite3
from pygeocoder import Geocoder
 
con = sqlite3.connect('shop.db')
outfile = open('shopList.csv','wt')
errorfile =open ('error.csv','wt')
 
try:
    geocoder = Geocoder()
    writer = csv.writer(outfile)
    ewriter = csv.writer(errorfile)
    con = sqlite3.connect("shop.db")
    c = con.execute("select * from shop")
    for row in c:
        if len(row) > 0:
            try:
		if len(row) < 4:
			print(row)
			continue
                result = geocoder.geocode(row[3].encode("utf-8"), language='ja')
                if len(result) > 0:
                    writer.writerow([row[0],row[1].encode("utf-8"),"",row[3].encode("utf-8"), result[0].coordinates[0], result[0].coordinates[1],row[6]])
            except Exception as e:
                ewriter.writerow([str(type(e)),row[1].encode("utf-8"), row[3].encode("utf-8")])

except Exception as e:
    print(sys.exc_info()[0])
    print(str(e))
finally:
    con.close()
    outfile.close()
    errorfile.close()
print('geocoding finished!')

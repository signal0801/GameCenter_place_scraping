# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect("database.db")
c = con.cursor()
c.execute("select * from shop")
for row in c:
   print row[1], row[3]
con.close()

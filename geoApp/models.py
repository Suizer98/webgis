"""


In this project this py used for importing database


"""


from django.db import models

# Create your models here.
import mysql.connector
connection = mysql.connector.connect(host='localhost',
                                     database='mymcd_scraped',
                                     user='root',
                                     password='REAPINGHOOK980921')
df = []
address = []

sql_select_Query = "select * from mcdmalaysiascraped"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()
connection.close()
cursor.close()

# place all markers
for row in records:
    df.append(row)

print(df)
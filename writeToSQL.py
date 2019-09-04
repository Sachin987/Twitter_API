import xlrd
import pymysql

book = xlrd.open_workbook("tweetsImportantInfo.xls") #open the file to extract to information
sheet = book.sheet_by_name("tweetsImportantInfo")    #specify the sheet name

connection = pymysql.connect( host="localhost", user = "root", passwd = "sachin" , db = "mysql")
cursor = connection.cursor()

query = """INSERT INTO twitter (Tweets , length, date_tweet  ,likes, retweets) VALUES (%s, %s, %s, %s, %s)"""
for r in range(1, sheet.nrows):
        Tweets          = sheet.cell(r,0).value
        length          = sheet.cell(r,1).value
        date_tweet      = sheet.cell(r,2).value
        likes           = sheet.cell(r,3).value
        retweets        = sheet.cell(r,4).value
        
        # Assign values from each row
        values = (Tweets , length, date_tweet  ,likes, retweets)
        # Execute sql Query
        cursor.execute(query, values)

# Close the cursor
cursor.close()
# Commit the transaction
conn.commit()
# Close the database connection
conn.close()

print ("Done!")
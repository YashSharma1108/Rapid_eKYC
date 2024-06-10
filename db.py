import pyodbc

server = 'INVL0089'
database = 'eKYC'

connectionString = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';'

def getdbObj():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    return cursor

# cursor.execute("select * from users")

# for row in cursor.fetchall():
#     print(row)
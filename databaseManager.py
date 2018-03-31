import pymysql

class DatabaseManager(object):
	def __init__(self):
		self.db = pymysql.connect("localhost","root","","ars" )
		self.cursor = self.db.cursor()
		self.cursor.execute("SELECT VERSION()")
		data = self.cursor.fetchone()
		print("Database version : %s " % data)
	def getPassword(self,loginId):
		sql = "SELECT password FROM login_credentials WHERE loginId='%s'" %(loginId)
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchone()[0]
		except:
		   print("Error: unable to fetch data")
	def getUserType(self,loginId):
		sql = "SELECT userType FROM login_credentials WHERE loginId='%s'" %(loginId)
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchone()[0]
			
		except:
		   print("Error: unable to fetch data")
	def getResults(self):
		print(self.cursor)
		sql = "SELECT * FROM login_credentials" 
		try:
			
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
			  loginId = row[0]
			  password = row[1]
			  type = row[2]
			  # Now print fetched result
			  print("%s,%s,%c" %(loginId,password,type))
		except:
		   print("Error: unable to fetch data")
if __name__=="__main__":
	dbManager = DatabaseManager()

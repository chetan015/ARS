import pymysql
from user import User

class DatabaseManager(object):
	def __init__(self):
		self.db = pymysql.connect("localhost","root","","ars" )
		self.cursor = self.db.cursor()
		self.cursor.execute("SELECT VERSION()")
		data = self.cursor.fetchone()
		print("Database version : %s " % data)
	def deleteUser(self,loginId):
		sql1 = "DELETE FROM user_details WHERE loginId='%s'" %(loginId)
		sql2 = "DELETE FROM login_credentials WHERE loginId='%s'" %(loginId)
		try:
			self.cursor.execute(sql1)
			self.db.commit()
			self.cursor.execute(sql2)
			self.db.commit()
			return 1;
		except Exception as e:
			print("Exeception occured:{}".format(e))
			db.rollback()
			return 0;
	def addUser(self,user):
		sql1 = "INSERT INTO login_credentials(loginId,password,userType) VALUES('%s','%s','%s')" %(user.loginId,user.password,user.userType)
		sql2 = "INSERT INTO user_details(name,phone,loginId) VALUES('%s','%s','%s')" %(user.name,user.phone,user.loginId)
		
		try:
			self.cursor.execute(sql1)
			self.db.commit()
			self.cursor.execute(sql2)
			self.db.commit()
			return 1;
		except Exception as e:
			print("Exeception occured:{}".format(e))
			db.rollback()
			return 0;
	def searchUserByLoginId(self,loginId):
		sql = "SELECT name,phone,loginId,password,userType FROM login_credentials NATURAL JOIN user_details where loginId='%s'" %(loginId)
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchone()
			name = results[0]
			phone = results[1]
			loginId = results[2]
			password = results[3]
			userType = results[4]
			user = User(name,phone,loginId,password,userType)
			print(user.toString)
			return user
		except Exception as e:
			print("Exception occured:{}".format(e))
			return None
	def updateUser(self,user):
		loginId = user.loginId
		status = self.deleteUser(loginId)
		if status==1:
			status = self.addUser(user)
		return status
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
		sql = "SELECT * FROM user_details" 
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
	
	print(dbManager.getUserType("Shubham"))
	user = User("Chetan Surana","18923123","Cheta","Brun",'e')
	print("Status=%d"%(dbManager.addUser(user)))
	dbManager.getResults()
	print(dbManager.searchUserByLoginId("Cheta").toString())

class User:
	def __init__(self,name,phone,loginId,password,userType):
		self.name = name
		self.phone = phone
		self.password = password
		self.loginId = loginId
		self.userType = userType
	def toString(self):
		return ("%s,%s,%s,%s" %(self.name,self.phone,self.loginId,self.password))

import sys
from PyQt5.QtWidgets import QDialog,QApplication
from design import Ui_arsDialog
from databaseManager import DatabaseManager
from user import User
class Mediator(QDialog):
	def __init__(self):
		super(Mediator, self).__init__()
		# Set up the user interface from Designer
		self.ui = Ui_arsDialog()
		self.ui.setupUi(self)
		self.dbManager = DatabaseManager()
		# Make some local modifications.
		self.ui.loginButton.clicked.connect(self.handleLogin)
		self.ui.adminLogoutButton.clicked.connect(self.handleLogout)
		self.ui.employeeLogoutButton.clicked.connect(self.handleLogout)
		self.ui.managerLogoutButton.clicked.connect(self.handleLogout)
		self.ui.addUserMenuButton.clicked.connect(self.showAddUserView)
		self.ui.searchUserMenuButton.clicked.connect(self.showModifyUserView)
		self.ui.addButton.clicked.connect(self.handleAddUser)
		self.ui.backAddButton.clicked.connect(self.handleBackAddButton)
		self.ui.backModifyButton.clicked.connect(self.handleBackModifyButton)
		self.ui.searchButton.clicked.connect(self.handleSearchUser)
		self.ui.deleteButton.clicked.connect(self.handleDeleteUser)
		self.ui.updateButton.clicked.connect(self.handleUpdateUser)
		self.searchSuccess = False
		self.confirmUpdate = False
	def showAddUserView(self):
		self.ui.addNameLineEdit.setText("")
		self.ui.addPhoneLineEdit.setText("")
		self.ui.addPasswordLineEdit.setText("")
		self.ui.confirmPasswordLineEdit.setText("")
		self.ui.addLoginLineEdit.setText("")
		self.ui.addUserTypeComboBox.setCurrentText("")
		self.ui.viewsStackedWidget.setCurrentIndex(self.ui.viewsStackedWidget.indexOf(self.ui.addUserView))
	def showModifyUserView(self):
		self.ui.searchLoginLineEdit.setText("")
		self.ui.modifyNameLineEdit.setText("")
		self.ui.modifyPhoneLineEdit.setText("")
		self.ui.modifyPasswordLineEdit.setText("")
		self.ui.modifyLoginLineEdit.setText("")
		self.ui.modifyUserTypeComboBox.clear()
		self.searchSuccess = False
		self.confirmUpdate = False
		self.ui.viewsStackedWidget.setCurrentIndex(self.ui.viewsStackedWidget.indexOf(self.ui.modifyUserView))

	def handleBackAddButton(self):
		self.ui.addUserPromptLabel.setText("Enter all the details to add user")
		self.ui.viewsStackedWidget.setCurrentIndex(1)
	def handleBackModifyButton(self):
		self.ui.modifyUserPromptLabel.setText("Enter the LoginId")
		self.ui.viewsStackedWidget.setCurrentIndex(1)
	def handleAddUser(self):
		name = self.ui.addNameLineEdit.text()
		phone = self.ui.addPhoneLineEdit.text()
		ps = self.ui.addPasswordLineEdit.text()
		loginId = self.ui.addLoginLineEdit.text()
		cps = self.ui.confirmPasswordLineEdit.text()
		userType = self.ui.addUserTypeComboBox.currentText()
		if(cps==ps):
			user = User(name,phone,loginId,ps,userType)
			status = self.dbManager.addUser(user)
			if(status==1):
				self.ui.addUserPromptLabel.setText("New User Added!")
				self.showAddUserView()
			else:
				self.ui.addUserPromptLabel.setText("Error adding user details. Try again.")
		else:
			self.ui.addUserPromptLabel.setText("Password and Confirm Password fields do not match. Try again.")
	def handleSearchUser(self):
		loginId = self.ui.searchLoginLineEdit.text()
		user = self.dbManager.searchUserByLoginId(loginId)
		if user==None:
			self.ui.modifyUserPromptLabel.setText("Not found. Try again.")
			self.showModifyUserView()
		else:
			self.searchSuccess = True
			self.ui.modifyUserPromptLabel.setText("User details found.")
			self.ui.modifyNameLineEdit.setText(user.name)
			self.ui.modifyPhoneLineEdit.setText(user.phone)
			self.ui.modifyLoginLineEdit.setText(user.loginId)
			self.ui.modifyPasswordLineEdit.setText(user.password)
			self.ui.modifyUserTypeComboBox.clear()
			self.ui.modifyUserTypeComboBox.addItem(user.userType)

	def handleLogout(self):
		self.ui.viewsStackedWidget.setCurrentIndex(0)
	
	def handleUpdateUser(self):
		if self.searchSuccess==False:
			self.ui.modifyUserPromptLabel.setText("First search for the user. Enter a valid loginId.")
			self.showModifyUserView()
			return;
		if self.confirmUpdate==False:
			self.ui.modifyNameLineEdit.setReadOnly(False)
			self.ui.modifyPhoneLineEdit.setReadOnly(False)
			self.ui.modifyLoginLineEdit.setReadOnly(False)
			self.ui.modifyPasswordLineEdit.setReadOnly(False)
			self.ui.modifyUserTypeComboBox.clear()
			self.ui.modifyUserTypeComboBox.addItem("Employee")
			self.ui.modifyUserTypeComboBox.addItem("Manager")
			self.ui.modifyUserTypeComboBox.addItem("Admin")
			self.ui.modifyUserPromptLabel.setText("Edit the fields below and click Update to confirm Update.")
			self.confirmUpdate = True
		else:
			name = self.ui.modifyNameLineEdit.text()
			phone = self.ui.modifyPhoneLineEdit.text()
			ps = self.ui.modifyPasswordLineEdit.text()
			loginId = self.ui.modifyLoginLineEdit.text()
			userType = self.ui.modifyUserTypeComboBox.currentText()
			self.confirmUpdate = False
			user = User(name,phone,loginId,ps,userType)
			status = self.dbManager.updateUser(user)
			if status == 1:
				self.ui.modifyUserPromptLabel.setText("Update successful. Enter loginId to search another user")
			else:
				self.ui.modifyUserPromptLabel.setText("Update unsuccessful! Try again")
			self.showModifyUserView()

	def handleDeleteUser(self):
			if self.searchSuccess==True:
				if self.confirmUpdate==False:
					loginId = self.ui.searchLoginLineEdit.text()
					status = self.dbManager.deleteUser(loginId)
					if status == 1:
						self.ui.modifyUserPromptLabel.setText("Delete successful. Enter Login Id to search another user")
					else:
						self.ui.modifyUserPromptLabel.setText("Delete unsuccessful. Try Again.")
				else:
					self.ui.modifyUserPromptLabel.setText("Cannot delete in the middle of update operation. Try again. Enter loginId")

			else:
				self.ui.modifyUserPromptLabel.setText("First search for the user. Enter valid loginId")
			self.showModifyUserView()
	def handleLogin(self):
		loginId = self.ui.loginLineEdit.text()
		password = self.ui.passwordLineEdit.text()
		ps = self.dbManager.getPassword(loginId)
		print(ps)
		if ps!=None:
			if password==ps:
				userType = self.dbManager.getUserType(loginId)
				self.ui.loginLineEdit.setText("");
				self.ui.passwordLineEdit.setText("");
				self.ui.loginPromptLabel.setText("Please Enter your Login Id and Password to Login")
				if userType=='Admin':
					self.ui.viewsStackedWidget.setCurrentIndex(1);
				elif userType=='Employee':
					self.ui.viewsStackedWidget.setCurrentIndex(4);
				else:
					self.ui.viewsStackedWidget.setCurrentIndex(5);
			else:
				self.ui.loginPromptLabel.setText("Incorrect Password. Please try again.")
		else:
			self.ui.loginPromptLabel.setText("Invalid Login Id. Please try again.")


		
def main():
	app = QApplication(sys.argv)
	window = Mediator()
	window.show()
	sys.exit(app.exec_())


if __name__=="__main__":
	main()
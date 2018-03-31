import sys
from PyQt5.QtWidgets import QDialog,QApplication
from design import Ui_arsDialog
from databaseManager import DatabaseManager
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
	def handleLogout(self):
		self.ui.viewsStackedWidget.setCurrentIndex(0)
	def handleLogin(self):
		username = self.ui.loginLineEdit.text()
		password = self.ui.passwordLineEdit.text()
		ps = self.dbManager.getPassword(username)
		print(ps)
		if ps!=None:
			if password==ps:
				userType = self.dbManager.getUserType(username)
				self.ui.loginLineEdit.setText("");
				self.ui.passwordLineEdit.setText("");
				self.ui.loginPromptLabel.setText("Please Enter your Username and Password to Login")
				if userType=='a':
					self.ui.viewsStackedWidget.setCurrentIndex(1);
				elif userType=='e':
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
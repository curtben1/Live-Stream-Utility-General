import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import paramiko

class Window(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(100,100,256,128)

        self.loginFrame = QFrame()
        self.usernameBox = QLineEdit()
        self.hostIpInput = QLineEdit()
        self.hostNameInput = QLineEdit()
        self.pwordBox = QLineEdit()

        self.pwordLabel = QLabel("Password")
        self.usernameLabel = QLabel("url")
        self.ipLabel = QLabel("IP")
        self.devveLabel = QLabel("device username")

        self.enterButton = QPushButton("execute")
        self.exitButton = QPushButton("stop video")
        
        self.loginLayout = QVBoxLayout()
        self.pwordBox.setEchoMode(QLineEdit.Password)

        self.loginLayout.addWidget(self.ipLabel)        
        self.loginLayout.addWidget(self.hostIpInput)
        self.loginLayout.addWidget(self.devveLabel)
        self.loginLayout.addWidget(self.hostNameInput)
        self.loginLayout.addWidget(self.usernameLabel)
        self.loginLayout.addWidget(self.usernameBox)
        self.loginLayout.addWidget(self.pwordLabel)
        self.loginLayout.addWidget(self.pwordBox)
        self.loginLayout.addWidget(self.enterButton)
        self.loginLayout.addWidget(self.exitButton)
        self.exitButton.hide()

        self.enterButton.clicked.connect(self.executeSSH)
        self.setWindowTitle(self.tr("remote live streamer"))
        
        self.setLayout(self.loginLayout)

    def executeSSH(self):
        self.thread = Worker(self)
        self.thread.start()
        self.exitButton.show()
        self.exitButton.clicked.connect(self.thread.exit)

class Worker(QThread):
    def __init__(self, window, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False

    def run(self):
        print("0")
        window.url = window.usernameBox.text()
        window.pwordPlain = window.pwordBox.text()
        window.hostName = window.hostNameInput.text()
        window.hostIp = window.hostIpInput.text()
        window.pwordBox.setText("")
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=window.hostIp,username=window.hostName,password=window.pwordPlain)
        command = "cvlc "+ window.url + "--caching=60000"
        stdin,stdout,stderr = ssh_client.exec_command(command)
        print(stdout.readlines())
        print(stderr.readlines())
        print("2")

    def exit(self):
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=window.hostIp,username=window.hostName,password=window.pwordPlain)
        command = "sudo killall vlc"
        stdin,stdout,stderr = ssh_client.exec_command(command)
        window.exitButton.hide()
    


app = QApplication(sys.argv)
window = Window()
window.show()
app.setWindowIcon(QIcon('streaming.ico'))
sys.exit(app.exec_())

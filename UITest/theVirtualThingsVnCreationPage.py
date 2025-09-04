from PyQt5 import QtWidgets, uic
import sys, subprocess

class CreationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CreationWindow, self).__init__()
        uic.loadUi('UI/vnCreationPage.ui', self)

        
        self.cancelButton.clicked.connect(CreationWindow.close)
        self.createButton.clicked.connect(self.createVN)

        self.show()

        
    def createVN(self):
        name = self.nameLineEdit.text()
        disableDNS = self.dnsCheckBox.isChecked()
        internal = self.internalCheckBox.isChecked()
        subnet = self.subnetLineEdit.text()
        gateway = self.gatewayLineEdit.text()

        if name == "":
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("You must provide a name for the VN.")
            dialog.exec_()
            return False

        args = ""
        if disableDNS:
            args += " -d"
        if internal:
            args += " -i"
        if subnet != "":
            args += " -s {}".format(subnet)
        if gateway != "":
            args += " -g {}".format(gateway)

        
        command = "vn-create {} {}".format(args,name)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status != 0:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText(f"An error occured while creating the VN.\n{err}")
            dialog.exec_()
            return False
        else:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Success")
            dialog.setIcon(QtWidgets.QMessageBox.Information)
            dialog.setText("The VN has been created successfully :)")
            dialog.exec_()
            app.quit()



app = QtWidgets.QApplication(sys.argv)
window = CreationWindow()
app.exec_()
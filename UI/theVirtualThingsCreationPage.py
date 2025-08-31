from PyQt5 import QtWidgets, uic
import sys, subprocess

class CreationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CreationWindow, self).__init__()
        uic.loadUi('UI/creationPage.ui', self)

        self.imageComboBox.addItems(self.getImageList())
        self.cancelButton.clicked.connect(CreationWindow.close)
        self.createButton.clicked.connect(self.createVM)

        self.show()

    
    def getImageList(self):
        images = ["debian","archlinux", "fedora"]
        return images

        p = subprocess.Popen("vm-ls-images -n", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        output = output.split(b'\n')
        for line in output:
            if line != b'':
                images.append(line.decode('utf-8'))
        #for line in result.stdout.readlines():
        #    print(line)
        
    def createVM(self):
        name = self.nameLineEdit.text()
        image = self.imageComboBox.currentText()
        gui = self.guiCheckBox.isChecked()
        vnet = self.networkLineEdit.text()
        isolated = self.isolatedCheckBox.isChecked()

        args = ""
        if gui:
            args += " -x"
        if vnet != "":
            args += " -c {}".format(vnet)
        if isolated:
            args += " -i"
        
        command = "vm-create {} -d {} {}".format(args,image,name)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status != 0:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("An error occured while creating the VM.\nPlease check the name is not already used and that the image exists.")
            dialog.exec_()
            return False
        else:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Success")
            dialog.setIcon(QtWidgets.QMessageBox.Information)
            dialog.setText("The VM has been created successfully :)")
            dialog.exec_()
            app.quit()



app = QtWidgets.QApplication(sys.argv)
window = CreationWindow()
app.exec_()
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit
import sys, subprocess

class TransferWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransferWindow, self).__init__()
        uic.loadUi('UI/transferPage.ui', self)
        self.selectedVM = sys.argv[1] if len(sys.argv) > 1 else None
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("No VM specified. Please run this script with a VM name as an argument.")
            dialog.exec_()
            sys.exit(1)
        self.subLabel.setText(f"Host <--> {self.selectedVM}")
        self.hostToVMButton.clicked.connect(self.hostToVM)
        self.vmToHostButton.clicked.connect(self.vmToHost)
        self.mountButton.clicked.connect(self.mountVM)




        self.show()

    def hostToVM(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            print("Selected File:", selected_files[0])

        subprocess.run(f"podman cp {selected_files[0]} {self.selectedVM}:/home", shell=True)
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("theVirtualThings - Info")
        dialog.setIcon(QtWidgets.QMessageBox.Information)
        dialog.setText("Transfer complete!")
        dialog.exec_()
        

    def vmToHost(self):
        text, okPressed = QInputDialog.getText(self, "Enter your file path","Your file:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory to Save File"))
        subprocess.run(f"podman cp {self.selectedVM}:{text} {dir}", shell=True)
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("theVirtualThings - Info")
        dialog.setIcon(QtWidgets.QMessageBox.Information)
        dialog.setText("Transfer complete!")
        dialog.exec_()
        
    def mountVM(self):
        subprocess.run(f"podman unshare bash -c 'mnt=$(podman mount {self.selectedVM}); dolphin $mnt'", shell=True)
        subprocess.run(f" {self.selectedVM}", shell=True)


        

app = QtWidgets.QApplication(sys.argv)
window = TransferWindow()
app.exec_()
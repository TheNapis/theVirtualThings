from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os, subprocess

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('UI/mainWindow.ui', self)
        self.selectedVM = None
        
        self.updateVMList()
        self.createButton.clicked.connect(self.createVMWindow)
        self.listWidget.itemClicked.connect(lambda : self.updateVMInfos(self.listWidget.currentItem().text()))
        self.removeButton.clicked.connect(self.deleteVM)
        self.startButton.clicked.connect(self.startVM)
        self.stopButton.clicked.connect(self.stopVM)
        self.attachButton.clicked.connect(self.attachVM)
        self.networkButton.clicked.connect(self.openNetworkPage)
        self.show()

    def updateVMInfos(self, vmName):
        self.selectedVM = vmName
        vmInfo = os.popen(f"vm-info {self.selectedVM}").read().splitlines()
        self.infosList.clear()
        for line in vmInfo:
            item = QtWidgets.QListWidgetItem()
            item.setText(line)
            self.infosList.addItem(item)

    def updateVMList(self):
        self.listWidget.clear()
        vmList = os.popen("vm-ls -n").read().splitlines()
        vmList = [line.split()[0] for line in vmList if line]
        for line in vmList:
            if "running" in os.popen(f"vm-status {line}").read():
                item = QtWidgets.QListWidgetItem()
                item.setText(line)
                item.setBackground( QColor("#00A516") )
                self.listWidget.addItem(item)
            else:
                item = QtWidgets.QListWidgetItem()
                item.setText(line)
                self.listWidget.addItem(item)
    
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
        
    def createVMWindow(self):
        os.system("python3 UI/theVirtualThingsCreationPage.py")
        self.updateVMList()

    def deleteVM(self):
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select a VM to delete.")
            dialog.exec_()
            return
        
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("theVirtualThings - Delete VM")
        dialog.setIcon(QtWidgets.QMessageBox.Information)
        dialog.setText("Are you sure you want to delete " + self.selectedVM +" ?\nThis action is irreversible.")
        dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dialog.setDefaultButton(QtWidgets.QMessageBox.No)
        ret = dialog.exec_()
        if ret == QtWidgets.QMessageBox.Yes:
            command = f"vm-rm {self.selectedVM} -f"
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            if p_status != 0:
                dialog = QtWidgets.QMessageBox()
                dialog.setWindowTitle("theVirtualThings - Error")
                dialog.setIcon(QtWidgets.QMessageBox.Critical)
                dialog.setText("An error occured while deleting the VM.\nPlease check the VM name.")
                dialog.exec_()
            else:
                dialog = QtWidgets.QMessageBox()
                dialog.setWindowTitle("theVirtualThings - Success")
                dialog.setIcon(QtWidgets.QMessageBox.Information)
                dialog.setText("The VM has been deleted successfully :)")
                dialog.exec_()
        self.selectedVM = None
        self.updateVMList()
        self.infosList.clear()

    def startVM(self):
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select a VM to start.")
            dialog.exec_()
            return
        command = f"vm-start {self.selectedVM}"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status != 0:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("An error occured while starting the VM.\nPlease check the VM name.")
            dialog.exec_()
        else:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Success")
            dialog.setIcon(QtWidgets.QMessageBox.Information)
            dialog.setText("The VM has been started successfully :)")
            dialog.exec_()
        self.updateVMList()
        self.updateVMInfos(vmName=self.selectedVM)

    def stopVM(self):
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select a VM to stop.")
            dialog.exec_()
            return
        command = f"vm-stop {self.selectedVM}"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status != 0:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("An error occured while stopping the VM.\nPlease check the VM name.")
            dialog.exec_()
        else:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Success")
            dialog.setIcon(QtWidgets.QMessageBox.Information)
            dialog.setText("The VM has been stopped successfully :)")
            dialog.exec_()
        self.updateVMList()
        self.infosList.clear()

    def attachVM(self):
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select a VM to attach.")
            dialog.exec_()
            return
        elif "running" not in os.popen(f"vm-status {self.selectedVM}").read():
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("The selected VM is not running.\nPlease start it before attaching.")
            dialog.exec_()
            return
        command = f"konsole -e vm-attach {self.selectedVM}"
        os.system(command)

    def openNetworkPage(self):
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select a VM to manage its network interfaces.")
            dialog.exec_()
            return
        os.system(f"python3 UI/theVirtualThingsNetworkPage.py {self.selectedVM}")



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
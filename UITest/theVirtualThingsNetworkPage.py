from PyQt5 import QtWidgets, uic
import sys, subprocess

class NetworkWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(NetworkWindow, self).__init__()
        uic.loadUi('UI/networkPage.ui', self)
        self.selectedVM = sys.argv[1] if len(sys.argv) > 1 else None
        if self.selectedVM is None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("No VM specified. Please run this script with a VM name as an argument.")
            dialog.exec_()
            sys.exit(1)
        self.connectedLabel.setText(f"Interfaces connected to {self.selectedVM} :")
        self.updateNetworkInfos()
        self.connectButton.clicked.connect(self.connectInterface)
        self.disconnectButton.clicked.connect(self.disconnectInterface)

        self.show()

    
    def updateNetworkInfos(self):
        vmInfo = subprocess.getoutput(f"vm-info {self.selectedVM}").splitlines()
        interfaces = [line for line in vmInfo if "Network Settings" in line]
        self.connectedList.clear()
        self.otherList.clear()
        connected = ()
        for line in interfaces:
            if "map[" in line:
                map_part = line.split("map[", 1)[1].split("]", 1)[0]
                pairs = map_part.split()
                for pair in pairs:
                    name = pair.split(":", 1)[0]
                    connected += (name,)
                    if "pasta" in name:
                        dialog = QtWidgets.QMessageBox()
                        dialog.setWindowTitle("theVirtualThings - Info")
                        dialog.setIcon(QtWidgets.QMessageBox.Critical)
                        dialog.setText("That VM got a pasta interface. Trying to disconnect it may cause issues.")
                        dialog.exec_()
                    item = QtWidgets.QListWidgetItem()
                    item.setText(name)
                    self.connectedList.addItem(item)
        vnList = subprocess.getoutput(f"vn-ls -n").splitlines()
        vnList = [line.split()[0] for line in vnList if line]
        for line in vnList:
            if line in connected:
                continue
            else:
                item = QtWidgets.QListWidgetItem()
                item.setText(line)
                self.otherList.addItem(item)
        
    def connectInterface(self):
        if self.otherList.currentItem() is  None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select an interface.")
            dialog.exec_()
            return
        else:
            interface = self.otherList.currentItem().text()
            subprocess.run(f"vn-connect {interface} {self.selectedVM}", shell=True)
            self.updateNetworkInfos()

    def disconnectInterface(self):
        if self.connectedList.currentItem() is  None:
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("theVirtualThings - Error")
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
            dialog.setText("Please select an interface.")
            dialog.exec_()
            return
        else:
            if "pasta" in self.connectedList.currentItem().text():
                dialog = QtWidgets.QMessageBox()
                dialog.setWindowTitle("theVirtualThings - Warning")
                dialog.setIcon(QtWidgets.QMessageBox.Warning)
                dialog.setText("That VM got a pasta interface. Disconnecting it may cause issues. Are you sure you want to proceed?")
                dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                response = dialog.exec_()
                if response == QtWidgets.QMessageBox.No:
                    return
            interface = self.connectedList.currentItem().text()
            subprocess.run(f"vn-disconnect {interface} {self.selectedVM}", shell=True)
            self.updateNetworkInfos()

app = QtWidgets.QApplication(sys.argv)
window = NetworkWindow()
app.exec_()
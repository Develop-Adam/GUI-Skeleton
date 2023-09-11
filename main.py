#=======================================================================================================#
# Imports                                                                                               #
#=======================================================================================================#
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from sub_routines import ThreadOne as One
from sub_routines import ThreadTwo as Two
from sub_routines import ThreadThree as Three
from sub_routines import ThreadFour as Four
from data_storage import data as d
from data_storage import commands as cmd

#=======================================================================================================#
# Worker Threads                                                                                        #
#=======================================================================================================#
class ThreadOne(QThread):
    return_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.commands_instance = One.ThreadRun()
        self.commands_instance.return_signal.connect(self.emit_signal)

    def run(self):
        self.commands_instance.start()

    def emit_signal(self, status):
        self.return_signal.emit(status)

class ThreadTwo(QThread):
    return_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.commands_instance = Two.ThreadRun()
        self.commands_instance.return_signal.connect(self.emit_signal)

    def run(self):
        self.commands_instance.start()

    def emit_signal(self, status):
        self.return_signal.emit(status)

class ThreadThree(QThread):
    return_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.commands_instance = Three.ThreadRun()
        self.commands_instance.return_signal.connect(self.emit_signal)

    def run(self):
        self.commands_instance.ems()

    def emit_signal(self, status):
        self.return_signal.emit(status)

class ThreadFour(QThread):
    return_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.commands_instance = Four.ThreadRun()
        self.commands_instance.return_signal.connect(self.emit_signal)

    def run(self):
        self.commands_instance.light()

    def emit_signal(self, status):
        self.return_signal.emit(status)

#=======================================================================================================#
# Class for the main window of the application                                                          #
#=======================================================================================================#
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi('Lib/GUI.ui', self)

        # Set the initial value of the progress bar
        self.BatteryLevel.setValue(d.battery_level)
        self.FuelLevel.setValue(d.fuel_level)

        # Instantiate the ThreadOne, ThreadTwo, ThreadThree, and ThreadFour objects
        self.ThreadOne = ThreadOne()
        self.ThreadTwo = ThreadTwo()
        self.ThreadThree = ThreadThree()
        self.ThreadFour = ThreadFour()

        # Connect the signals from the threads to the respective handlers
        self.ThreadOne.return_signal.connect(self.handle_ThreadOne)
        self.ThreadTwo.return_signal.connect(self.handle_ThreadTwo)
        self.ThreadThree.return_signal.connect(self.handle_ThreadThree)
        self.ThreadFour.return_signal.connect(self.handle_ThreadFour)

        # Connect the signals to the slots
        self.pushButton.clicked.connect(self.ThreadOne.start)
        self.pushButton_2.clicked.connect(self.ThreadTwo.start)

        self.show()

#=======================================================================================================#
# Handle the return signals from the threads                                                            #
#=======================================================================================================#
    def handle_ThreadOne(self, status):
        if self is not None:
            if status == True:
                cmd.SERVER_ON = True
                self.pushButton.setText("Stop Server")
            else:
                cmd.SERVER_ON = False
                self.pushButton.setText("Start Server")

    def handle_ThreadTwo(self, status):
        if status is not None:
            self.BatteryLevel.setValue(d.battery_level)
            print(f'Battery Level: {d.battery_level}')

    def handle_ThreadThree(self, value):
        if self is not None:
            pass

    def handle_ThreadFour(self, value):
        if self is not None:
            if value == True:
                if value == True:
                    print("handle_ThreadFour Returned True")
                else:
                    print("handle_ThreadFour Returned False")

#=======================================================================================================#
# Close the threads on close                                                                            #
#=======================================================================================================#
    def closeEvent(self, event: QEvent) -> None:
        # Clean up threads on close
        self.ThreadOne.quit()
        self.ThreadOne.wait()

        self.ThreadTwo.quit()
        self.ThreadTwo.wait()

        self.ThreadThree.quit()
        self.ThreadThree.wait()

        self.ThreadFour.quit()
        self.ThreadFour.wait()

        event.accept()

#=======================================================================================================#
# Main function                                                                                         #
#=======================================================================================================#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = UI()
    mainWin.show()
    sys.exit(app.exec_())

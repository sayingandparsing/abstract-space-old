from .threaded_pipe import ProcessPipe
from PyQt5.QtWidgets import QListWidget, QApplication, QMainWindow, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtCore import QTimer
from PyQt5 import Qt
import sys
from time import time
from typing import Union

ftime = lambda s, t: s.format(time()-t)


class ViewContext(ProcessPipe):
    """docstring for ListDialog"""
    def __init__(self, connection):
        ProcessPipe.__init__(self, connection)
        self.connection = connection
        self.timer = Qt.QTimer()
        self.timer.timeout.connect(self.monitor_pipe)
        #self.view = None

    def run(self):
        self.view_process = QApplication(sys.argv)
        self.load_stylesheet()
        self.view = SpaceView()
        self.timer.start(180)
        sys.exit(self.view_process.exec_())

    def load_stylesheet(self):
        with open('/home/reagan/path_mod/Abstract_Space/style.qss', 'r') as f:
            self.view_process.setStyleSheet(f.read())

    @Qt.pyqtSlot()
    def monitor_pipe(self):
        signifier = self.check_pipe()
        if signifier is not None:
            self.interpret(signifier)
            print('gui sig interpreted')
            if self.terminate is True:
                self.view_process.exit()
        # Callback for idle task must return True, or isn't repeated
        # return True

    def interpret(self, signifier: Union[str, list]):
        if type(signifier) == str:
            if signifier == 'TERMINATE':
                self.terminate = True
        #elif type(signifier) == list:
        else:
            print('recieved list')
            print (signifier)
            self.populate_listbox(signifier)

    def populate_listbox(self, items):
        self.view.remove_populated_list()
        self.view.create_list(items)


    def display(self):
        self.show_all()

    def terminate(self):
        #self.gui_thread.# = None
        pass


class SpaceView(QWidget):
    """docstring for AbstractSpaceDialog"""

    def __init__(self):
        QWidget.__init__(self)
        print('created win')
        self.setObjectName("space_view")
        #self.resize(379, 456)
        print('resized win')
        #self.main.setCentralWidget(self)
        self.vert_layout = QVBoxLayout(self)
        self.setLayout(self.vert_layout)
        #self.lineEdit = QLineEdit(self)
        #self.vert_layout.addWidget(self.lineEdit)
        self.list_view = None
        #self.show()

    def remove_populated_list(self):
        if self.list_view is not None:
            t = time()
            self.vert_layout.removeWidget(self.list_view)
            print(ftime('remove old listbox\t{}',t))

    def create_list(self, items):
        self.list_view = QListWidget()
        self.list_view.addItems(items)
        self.vert_layout.addWidget(self.list_view)
        self.show()

    def accomodate_size(self):
        pass

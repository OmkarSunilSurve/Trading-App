


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

from add import Ui_add_window
from DataBase3 import Ui_Dialog
from chart1 import Ui_Chart
from Opt import Ui_Optimization
from Gains import Ui_Gains
from Short import Ui_SELL
from Neu import GenericAssistant

import tensorflow as tf
import pickle
import sys





def load_model_from_pickle(model_name):
    with open(f"{model_name}.pkl", 'rb') as file:
        model_data = pickle.load(file)

    words = model_data['words']
    classes = model_data['classes']

    model = tf.keras.models.model_from_json(model_data['model'])
    model.set_weights(model_data['model_weights'])

    return words, classes, model

class Ui_First_window(object):
    
    
    def openwindow(self,text):
        self.lineEdit.clear()
        
        def add_portfolio():
            
            self.window = QtWidgets.QDialog()
            self.ui = Ui_add_window()
            self.ui.setupUi(self.window)
            self.window.show()
            
            
        def show_portfolio():
            
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Dialog()
            self.ui.setupUi(self.window)
            self.window.show()
            
        def plot_chart():
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Chart()
            self.ui.setupUi(self.window)
            self.window.show()
            
        def optimize():
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Optimization()
            self.ui.setupUi(self.window)
            self.window.show()
            
        def portfolio_gains():
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Gains()
            self.ui.setupUi(self.window)
            self.window.show()
            
        def remove_portfolio():
            self.window = QtWidgets.QDialog()
            self.ui = Ui_SELL()
            self.ui.setupUi(self.window)
            self.window.show()
        
        def bye():
            First_window.close()
            
        
        mappings = { 'add_portfolio' : add_portfolio, 'show_portfolio' : show_portfolio , 'plot_chart' : plot_chart , 'portfolio_gains':portfolio_gains ,
                    'optimize':optimize , 'remove_portfolio':remove_portfolio , 'bye':bye}
        assistant = GenericAssistant('Intents.json',mappings)
        assistant.words = words
        assistant.classes = classes
        assistant.model = model
        assistant.request(text)
        
    def setupUi(self, First_window):
        First_window.setObjectName("First_window")
        First_window.resize(931, 607)
        First_window.setWindowIcon(QIcon('bull-market.png'))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(First_window.sizePolicy().hasHeightForWidth())
        First_window.setSizePolicy(sizePolicy)
        First_window.setMinimumSize(QtCore.QSize(931, 607))
        First_window.setMaximumSize(QtCore.QSize(931, 607))
        self.label = QtWidgets.QLabel(First_window)
        self.label.setGeometry(QtCore.QRect(50, 40, 831, 131))
        font = QtGui.QFont()
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(First_window)
        self.label_2.setGeometry(QtCore.QRect(90, 190, 751, 111))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(First_window)
        self.lineEdit.setGeometry(QtCore.QRect(192, 341, 541, 71))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(First_window,clicked=lambda: self.openwindow(self.lineEdit.text()))
        self.pushButton.setGeometry(QtCore.QRect(310, 480, 291, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        # self.Close_but = QtWidgets.QPushButton(First_window)
        # self.Close_but.setGeometry(QtCore.QRect(530, 480, 291, 71))
        # font = QtGui.QFont()
        # font.setPointSize(20)
        # self.Close_but.setFont(font)
        # self.Close_but.setObjectName("Close_but")
        # self.Close_but.clicked.connect(First_window.close)

        self.retranslateUi(First_window)
        QtCore.QMetaObject.connectSlotsByName(First_window)

    def retranslateUi(self, First_window):
        _translate = QtCore.QCoreApplication.translate
        First_window.setWindowTitle(_translate("First_window", "Welcome"))
        self.label.setText(_translate("First_window", "Hello There!!!!"))
        self.label_2.setText(_translate("First_window", "How Can I Help You???"))
        self.pushButton.setText(_translate("First_window", "Submit"))
        #self.Close_but.setText(_translate("First_window", "Close"))


if __name__ == "__main__":
    
    
    
    words, classes, model = load_model_from_pickle("Financial_Assistant_new")
    
    
    app = QtWidgets.QApplication(sys.argv)
    First_window = QtWidgets.QDialog()
    ui = Ui_First_window()
    ui.setupUi(First_window)
    First_window.show()
    sys.exit(app.exec_())

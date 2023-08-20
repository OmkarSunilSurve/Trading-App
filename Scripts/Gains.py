


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sqlite3
from PyQt5.QtGui import QIcon
import pandas as pd
import os
import sys
import yfinance as yf
yf.pdr_override()


class Ui_Gains(object):
    
    def press(self):
        db_path = os.path.join(os.path.dirname(sys.argv[0]), "Stock_data.db")
        db = sqlite3.connect(str(db_path))
        
        
        query = '''Select * from Data'''
        df = pd.read_sql(query,db)
        df['Price'] = df['Amount'] / df['Quantity']
        df = df[['Name','Price']]
        stocks = list(df.Name)
        curr_price = []
        for stock in stocks:
            data = yf.Ticker(stock).info
            price = data['currentPrice']
            curr_price.append(price)
        df['Curr_price'] = curr_price
        df['Perf.'] = ((df['Curr_price'] - df['Price'] ) * 100 / df['Price']).round(decimals=2)
        df = df.sort_values('Perf.', ascending=False)
        sum = df['Curr_price'].sum() - df['Price'].sum()
        sum = str(sum.round(decimals=2))
        
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.tableWidget.setItem(i, j, item)
            
        self.Gain_disp.setText(sum)
        
    
    
    
    
    def setupUi(self, Gains):
        Gains.setObjectName("Gains")
        Gains.setEnabled(True)
        Gains.resize(765, 713)
        Gains.setWindowIcon(QIcon('gains.png'))
        Gains.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(220,220,220);")
        self.GAIN_BUT = QtWidgets.QPushButton(Gains , clicked = lambda: self.press())
        self.GAIN_BUT.setGeometry(QtCore.QRect(280, 17, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.GAIN_BUT.setFont(font)
        self.GAIN_BUT.setStyleSheet("color: rgb(60, 255, 73);\n"
"background-color: rgb(125, 153, 126);")
        self.GAIN_BUT.setObjectName("GAIN_BUT")
        self.tableWidget = QtWidgets.QTableWidget(Gains)
        self.tableWidget.setGeometry(QtCore.QRect(40, 100, 691, 471))
        self.tableWidget.setStyleSheet("font: 15pt \"MS Shell Dlg 2\";")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(168)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.Overall_gain = QtWidgets.QLabel(Gains)
        self.Overall_gain.setGeometry(QtCore.QRect(170, 630, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Overall_gain.setFont(font)
        self.Overall_gain.setStyleSheet("color: rgb(0, 0, 128);\n"
"background-color: rgb(125, 153, 126);\n"
"border: 2px solid rgb(100, 25, 173);")
        self.Overall_gain.setAlignment(QtCore.Qt.AlignCenter)
        self.Overall_gain.setObjectName("Overall_gain")
        self.Gain_disp = QtWidgets.QLabel(Gains)
        self.Gain_disp.setGeometry(QtCore.QRect(430, 630, 160, 41))
        self.Gain_disp.setStyleSheet("color: rgb(60, 255, 73);\n"
"background-color: rgb(125, 153, 126);\n"
"border: 2px solid rgb(100, 25, 173);")
        self.Gain_disp.setText("")
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Gain_disp.setFont(font)
        self.Gain_disp.setObjectName("Gain_disp")
        self.label_2 = QtWidgets.QLabel(Gains)
        self.label_2.setGeometry(QtCore.QRect(390, 630, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Gains)
        QtCore.QMetaObject.connectSlotsByName(Gains)

    def retranslateUi(self, Gains):
        _translate = QtCore.QCoreApplication.translate
        Gains.setWindowTitle(_translate("Gains", "Gains"))
        self.GAIN_BUT.setText(_translate("Gains", "CALCULATE"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Gains", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Gains", "Bought_Price"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Gains", "Current_Price"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Gains", "Performance"))
        self.Overall_gain.setText(_translate("Gains", "Over All Gain"))
        self.label_2.setText(_translate("Gains", "-"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Gains = QtWidgets.QDialog()
    ui = Ui_Gains()
    ui.setupUi(Gains)
    Gains.show()
    sys.exit(app.exec_())

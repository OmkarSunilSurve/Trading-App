


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon

import pandas as pd
from datetime import  date
import sys
import os
import sqlite3
from imports import Optimize


class Ui_Optimization(object):
    
    
    
    def Rebal(self):
        
        self.rebal_but.setEnabled(False)
        db_path = os.path.join(os.path.dirname(sys.argv[0]), "Stock_data.db")
        db = sqlite3.connect(str(db_path))
        cursor = db.cursor()
        
        query = '''SELECT * FROM Data'''
        df = pd.read_sql(query,db)
        Tot_Amount = df['Amount'].sum()
        Stocks = list(df.Name)
        
        df1 = pd.DataFrame()
        
        df1['Name'] = df['Name']
        df1['Date'] = [date.today()] * len(df1['Name'])
        df1['Action'] = 'Sell'
        df1['Quantity'] = -df['Quantity']
        df1['Price'] = [df['Amount'][i] / df['Quantity'][i] for i in range(len(df))]
        df1['Amount'] = -df['Amount']
        des_order = ['Date','Name','Action','Quantity','Price','Amount']
        df1 = df1.reindex(columns = des_order)
        df1['Quantity'] = pd.to_numeric(df1['Quantity'])
        df1['Amount'] = pd.to_numeric(df1['Amount'])
        df1.to_sql('Stock',db,if_exists = 'append', index=False)
        
        
        Opt_result , Price = Optimize(Stocks, Tot_Amount)
        Opt_result = Opt_result[0]
        
        df = pd.DataFrame(Opt_result.items(),columns = ['Name','Quantity'])
        
        df['Amount'] = df.apply(lambda row: row['Quantity'] * Price[row['Name']], axis=1)
        df['Amount'] = df['Amount'].round(decimals=2)
        
        df1 = pd.DataFrame()
        
        df1['Name'] = df['Name']
        df1['Date'] = [date.today()] * len(df1['Name'])
        df1['Action'] = 'Buy'
        df1['Quantity'] = df['Quantity']
        df1['Price'] = [Price[stock] for stock in df['Name']]
        df1['Amount'] = df['Amount']
        des_order = ['Date','Name','Action','Quantity','Price','Amount']
        df1 = df1.reindex(columns = des_order)
        df1['Quantity'] = pd.to_numeric(df1['Quantity'])
        df1['Amount'] = pd.to_numeric(df1['Amount'])
        df1.to_sql('Stock', db,if_exists = 'append' , index=False)
        
        cursor.close()
        db.close()
        
        
    
    def Opt(self):
        db_path = os.path.join(os.path.dirname(sys.argv[0]), "Stock_data.db")
        db = sqlite3.connect(str(db_path))
        cursor = db.cursor()
        
        query = '''SELECT Name ,SUM(Quantity) as Quantity ,SUM(Amount) as Amount FROM Stock Group By Name'''
        df = pd.read_sql(query,db)
        Stocks = df['Name'].unique()
        Tot_Amount = df['Amount'].sum()
        result = cursor.execute(query)
        
        self.Curr_Hold.setRowCount(0)
        
        for row_number , row_data in enumerate(result):
            self.Curr_Hold.insertRow(row_number)
            for column_number , data in enumerate(row_data):
                self.Curr_Hold.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        
        
        
        Opt_result , Price = Optimize(Stocks, Tot_Amount)
        Opt_result = Opt_result[0]
        
        df = pd.DataFrame(Opt_result.items(),columns = ['Stock','Quantity'])
        df['Amount'] = df.apply(lambda row: row['Quantity'] * Price[row['Stock']], axis=1)
        df['Amount'] = df['Amount'].round(decimals=2)
        
        self.Opt_Hold.setRowCount(df.shape[0])
        self.Opt_Hold.setColumnCount(df.shape[1])
        
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.Opt_Hold.setItem(i, j, item)
        
        cursor.close()
        db.close()
    
    
    
    
    
    def setupUi(self, Optimization):
        Optimization.setObjectName("Optimization")
        Optimization.resize(867, 690)
        Optimization.setWindowIcon(QIcon('optimize.png'))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Optimization.sizePolicy().hasHeightForWidth())
        Optimization.setSizePolicy(sizePolicy)
        Optimization.setMinimumSize(QtCore.QSize(866, 629))
        Optimization.setMaximumSize(QtCore.QSize(869, 690))
        self.Opt_but = QtWidgets.QPushButton(Optimization,clicked = lambda : self.Opt())
        self.Opt_but.setGeometry(QtCore.QRect(320, 20, 211, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Opt_but.setFont(font)
        self.Opt_but.setObjectName("Opt_but")
        self.Curr_Hold = QtWidgets.QTableWidget(Optimization)
        self.Curr_Hold.setGeometry(QtCore.QRect(35, 90, 391, 521))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Curr_Hold.setFont(font)
        self.Curr_Hold.setObjectName("Curr_Hold")
        self.Curr_Hold.setColumnCount(3)
        self.Curr_Hold.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Curr_Hold.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Curr_Hold.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Curr_Hold.setHorizontalHeaderItem(2, item)
        self.Curr_Hold.horizontalHeader().setDefaultSectionSize(129)
        self.Curr_Hold.horizontalHeader().setMinimumSectionSize(30)
        self.Opt_Hold = QtWidgets.QTableWidget(Optimization)
        self.Opt_Hold.setGeometry(QtCore.QRect(440, 90, 391, 521))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Opt_Hold.sizePolicy().hasHeightForWidth())
        self.Opt_Hold.setSizePolicy(sizePolicy)
        self.Opt_Hold.setMinimumSize(QtCore.QSize(391, 521))
        self.Opt_Hold.setMaximumSize(QtCore.QSize(392, 522))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Opt_Hold.setFont(font)
        self.Opt_Hold.setObjectName("Opt_Hold")
        self.Opt_Hold.setColumnCount(3)
        self.Opt_Hold.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Opt_Hold.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Opt_Hold.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Opt_Hold.setHorizontalHeaderItem(2, item)
        self.Opt_Hold.horizontalHeader().setDefaultSectionSize(129)
        self.Opt_Hold.horizontalHeader().setMinimumSectionSize(30)
        
        self.rebal_but = QtWidgets.QPushButton(Optimization,clicked = lambda : self.Rebal())
        self.rebal_but.setGeometry(QtCore.QRect(330, 620, 211, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.rebal_but.setFont(font)
        self.rebal_but.setObjectName("rebal_but")
        self.rebal_but.clicked.connect(Optimization.close) 

        self.retranslateUi(Optimization)
        QtCore.QMetaObject.connectSlotsByName(Optimization)

    def retranslateUi(self, Optimization):
        _translate = QtCore.QCoreApplication.translate
        Optimization.setWindowTitle(_translate("Optimization", "Optimize"))
        self.Opt_but.setText(_translate("Optimization", "Optimize"))
        item = self.Curr_Hold.horizontalHeaderItem(0)
        item.setText(_translate("Optimization", "Name"))
        item = self.Curr_Hold.horizontalHeaderItem(1)
        item.setText(_translate("Optimization", "Cur_Quant..."))
        item = self.Curr_Hold.horizontalHeaderItem(2)
        item.setText(_translate("Optimization", "Invest..."))
        item = self.Opt_Hold.horizontalHeaderItem(0)
        item.setText(_translate("Optimization", "Name"))
        item = self.Opt_Hold.horizontalHeaderItem(1)
        item.setText(_translate("Optimization", "Opt_Quant..."))
        item = self.Opt_Hold.horizontalHeaderItem(2)
        item.setText(_translate("Optimization", "Invest..."))
        self.rebal_but.setText(_translate("Optimization", "Rebalance"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Optimization = QtWidgets.QDialog()
    ui = Ui_Optimization()
    ui.setupUi(Optimization)
    Optimization.show()
    sys.exit(app.exec_())

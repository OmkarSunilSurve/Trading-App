
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import sqlite3


class Ui_Dialog(object):
    
    
    def display(self):
        
            self.ref_but.setEnabled(False)
            db_path = os.path.join(os.path.dirname(sys.argv[0]), "Stock_data.db")
            db = sqlite3.connect(str(db_path))
            cursor = db.cursor()
            
            command = ''' SELECT * FROM Stock order by Date'''
            
            result = cursor.execute(command)
            
            
            self.table.setRowCount(0)
            
            for row_number , row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number , data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            
            ## For Portfloio chart
            query = ''' SELECT Name , Amount FROM Stock '''
            df = pd.read_sql_query(query, db)
            df['Amount'] = pd.to_numeric(df['Amount'])
            category_totals = df.groupby('Name')['Amount'].sum()
            
            self.figure_portfolio.clear()
            axes = self.figure_portfolio.add_subplot(111)
            axes.pie(category_totals, labels=category_totals.index, wedgeprops={'edgecolor': 'white'},autopct='%1.1f%%')
            circle = plt.Circle((0, 0), 0.6, color='white')
            axes.add_artist(circle)
            
            legend = axes.legend(category_totals.index, loc='center')
            legend.set_bbox_to_anchor((0, 1))  # Adjust the position of the legend within the figure
            plt.setp(legend.get_title(), fontsize='large') 
            
            axes.set(aspect='equal')
            self.canvas_portfolio.draw()
            
            
            ## For Data Display
            query = '''SELECT Name , Quantity , Amount from Stock'''
            df = pd.read_sql_query(query, db)
            df['Quantity'] = pd.to_numeric(df['Quantity'])
            df['Amount'] = pd.to_numeric(df['Amount'])
            Data = df.groupby('Name')[['Quantity','Amount']].sum().reset_index()
            
            try:
                Data = Data[Data['Quantity'] > 0]
            except IndexError:
                pass
            
            Data['Amount'] = Data['Amount'].round(decimals=2)
            Data.to_sql('Data', db, if_exists='replace', index=False)
            
            
            command = '''SELECT * FROM Data'''
            result = cursor.execute(command)
            for row_number , row_data in enumerate(result):
                self.Data_table.insertRow(row_number)
                for column_number , data in enumerate(row_data):
                    self.Data_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            
            cursor.close()
            db.close()
    
    
    
    
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(875, 585)
        Dialog.setWindowIcon(QIcon('database.png'))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(875, 585))
        Dialog.setMaximumSize(QtCore.QSize(875, 585))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-10, 40, 891, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(60, 255, 73);\n"
"background-color: rgb(125, 153, 126);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.ref_but = QtWidgets.QPushButton(Dialog,clicked = lambda :self.display())
        self.ref_but.setGeometry(QtCore.QRect(70, 520, 161, 51))
        
        font = QtGui.QFont()
        font.setPointSize(18)
        self.ref_but.setFont(font)
        self.ref_but.setObjectName("ref_but")
        self.Data = QtWidgets.QTabWidget(Dialog)
        self.Data.setGeometry(QtCore.QRect(20, 100, 831, 411))
        self.Data.setObjectName("Data")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.table = QtWidgets.QTableWidget(self.tab)
        self.table.setGeometry(QtCore.QRect(10, 10, 811, 371))
        self.table.setMinimumSize(QtCore.QSize(811, 0))
        self.table.setMaximumSize(QtCore.QSize(811, 16777215))
        self.table.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.table.setObjectName("table")
        self.table.setColumnCount(6)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, item)
        self.Data.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.Data_table = QtWidgets.QTableWidget(self.tab_3)
        self.Data_table.setGeometry(QtCore.QRect(0, 0, 821, 381))
        self.Data_table.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.Data_table.setObjectName("Data_table")
        self.Data_table.setColumnCount(3)
        self.Data_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(16)
        item.setFont(font)
        self.Data_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(16)
        item.setFont(font)
        self.Data_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(16)
        item.setFont(font)
        self.Data_table.setHorizontalHeaderItem(2, item)
        self.Data_table.horizontalHeader().setDefaultSectionSize(272)
        self.Data.addTab(self.tab_3, "")
        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.Portfolio = QtWidgets.QGraphicsView(self.tab_2)
        self.Portfolio.setGeometry(QtCore.QRect(0, 0, 821, 381))
        self.Portfolio.setObjectName("Portfolio")
        self.figure_portfolio = Figure(figsize=(11, 5))
        self.canvas_portfolio = FigureCanvas(self.figure_portfolio)
        self.scene_portfolio = QtWidgets.QGraphicsScene(self.Portfolio)
        self.scene_portfolio.addWidget(self.canvas_portfolio)
        self.Portfolio.setScene(self.scene_portfolio)
        self.Data.addTab(self.tab_2, "")
        
        
        self.CloseButton = QtWidgets.QPushButton(Dialog)
        self.CloseButton.setGeometry(QtCore.QRect(660, 520, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.CloseButton.setFont(font)
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.clicked.connect(Dialog.close) 

        self.retranslateUi(Dialog)
        self.Data.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PortFolio"))
        self.label.setText(_translate("Dialog", "Stock"))
        self.ref_but.setText(_translate("Dialog", "Refresh"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Date"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Name"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Action"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Quantity"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Price"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Amount"))
        self.Data.setTabText(self.Data.indexOf(self.tab), _translate("Dialog", "Transaction"))
        item = self.Data_table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name"))
        item = self.Data_table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Quantity"))
        item = self.Data_table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Amount"))
        self.Data.setTabText(self.Data.indexOf(self.tab_3), _translate("Dialog", "Data"))
        self.Data.setTabText(self.Data.indexOf(self.tab_2), _translate("Dialog", "Portfolio"))
        self.CloseButton.setText(_translate("Dialog", "Close"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

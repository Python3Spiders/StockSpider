# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/12/18 21:54
# file_name:        rightview.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QTabWidget,QLabel,QTableWidget,QAbstractItemView,QTableWidgetItem
from PyQt5.QtCore import Qt


class RightTableView(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        tabWidgets = QTabWidget()

        label = QLabel("前一日涨幅排名前十的股票详细信息")
        tabWidgets.addTab(label, "涨幅排名")
        label = QLabel("前一日成交量排名前十的股票详细信息")
        tabWidgets.addTab(label, "成交量排名")

        tabWidgets.currentChanged['int'].connect(self.tabClicked)   # 绑定标签点击时的信号与槽函数

        self.mainLayout.addWidget(tabWidgets)

        self.tableView = QTableWidget()
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.table.setHorizontalHeaderLabels(["股票代码", "开盘", "收盘",'最高','最低','成交量'])  # 设置行表头

        self.mainLayout.addWidget(self.table)
        self.mainLayout.setStretch(0,1)
        self.mainLayout.setStretch(1,12)
        self.setLayout(self.mainLayout)

        self.updateView()

    def updateView(self):
        self.table.insertRow(0)

        stock_code = QTableWidgetItem("1001")
        stock_code.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        stock_code.setTextAlignment(Qt.AlignCenter)

        stock_open = QTableWidgetItem("10.20")  # 我们要求它可以修改，所以使用默认的状态即可
        stock_open.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        stock_open.setTextAlignment(Qt.AlignCenter)

        stock_close = QTableWidgetItem("10.20")  # 我们要求它可以修改，所以使用默认的状态即可
        stock_close.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        stock_close.setTextAlignment(Qt.AlignCenter)


        stock_high = QTableWidgetItem("10.20")  # 我们要求它可以修改，所以使用默认的状态即可
        stock_high.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        stock_high.setTextAlignment(Qt.AlignCenter)


        stock_low = QTableWidgetItem("10.20")  # 我们要求它可以修改，所以使用默认的状态即可
        stock_low.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        stock_low.setTextAlignment(Qt.AlignCenter)


        stock_dealNum = QTableWidgetItem("10.20")  # 我们要求它可以修改，所以使用默认的状态即可
        stock_dealNum.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        stock_dealNum.setTextAlignment(Qt.AlignCenter)


        self.table.setItem(0, 0, stock_code)
        self.table.setItem(0, 1, stock_open)
        self.table.setItem(0, 2, stock_close)
        self.table.setItem(0, 3, stock_high)
        self.table.setItem(0, 4, stock_low)
        self.table.setItem(0, 5, stock_dealNum)



    def tabClicked(self,index):
        print(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = RightTableView()
    mainWin.show()
    sys.exit(app.exec_())

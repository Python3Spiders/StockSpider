# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/12/2 15:22
# file_name:        gui.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import  QApplication, QHBoxLayout, QWidget, \
     QAction,QMainWindow,QVBoxLayout,QPushButton
from PyQt5.QtGui import QIcon
from pyecharts import Bar, Pie, Line, Overlap,Kline
from pyecharts_javascripthon.api import TRANSLATOR

from stock_analysis.utils import myDict
from rightview import RightTableView

import pymongo


class Visualization(QMainWindow):

    themes = ['light', 'dark']
    themesTip = ['切换为深色主题','切换为浅色主题']

    def __init__(self):
        super().__init__()

        self.leftTopView = None
        self.leftTopEcharts = False

        self.BottomView = None
        self.BottomEcharts = False
        self.initDataSet()
        self.initUi()
        self.loadUrl()

    def initUi(self):

        self.statusBar().showMessage('加载中...')

        self.setGeometry(100, 60, 600, 400)
        self.setWindowTitle('关注微信公众号：月小水长')
        self.setWindowIcon(QIcon('logo.jpg'))

        self.themeSetAct = QAction('更换图表主题(&T)', self)
        self.themeSetAct.setShortcut('Ctrl+T')
        # 默认浅色主题
        self.themeIndex = 0
        self.themeSetAct.setStatusTip(Visualization.themesTip[self.themeIndex])
        self.themeSetAct.triggered.connect(self.changeTheme)

        menubar = self.menuBar()
        setMenu = menubar.addMenu('设置(&S)')
        setMenu.addAction(self.themeSetAct)


        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # 添加web view
        self.leftTopView = QWebEngineView()
        self.leftTopView.setContextMenuPolicy(Qt.NoContextMenu)

        self.BottomView = QWebEngineView()
        self.BottomView.setContextMenuPolicy(Qt.NoContextMenu)



        h1box = QHBoxLayout()
        h1box.addWidget(self.leftTopView)
        h1box.addWidget(RightTableView())
        h1box.setStretch(0,1)
        h1box.setStretch(1,1)


        h2box = QHBoxLayout()
        # v2box = QVBoxLayout()
        h2box.addWidget(self.BottomView)


        vbox = QVBoxLayout()
        vbox.addLayout(h1box)
        vbox.addLayout(h2box)
        vbox.setStretch(0,1)
        vbox.setStretch(1,1)


        self.widget.setLayout(vbox)

    def resizeEvent(self, *args, **kwargs):
        w, h = self.width(), self.height()


    def changeTheme(self):
        self.themeIndex = (self.themeIndex+1)%2
        self.themeSetAct.setStatusTip(Visualization.themesTip[self.themeIndex])

        if not self.BottomView:
            return
        options = self.getOptions(type='K')

        self.BottomView.page().runJavaScript(
            '''
                myChart.dispose();
                var myChart = echarts.init(document.getElementById('container'), '{theme}', {{renderer: 'canvas'}});
                myChart.clear();
                window.onresize = function(){{
                    myChart.resize();
                }}
                var option = eval({options});
                myChart.setOption(option);
            '''.format(theme=Visualization.themes[self.themeIndex],options=options)
        )

        if not self.leftTopView:
            return
        options = self.getOptions(type='Pie')

        self.leftTopView.page().runJavaScript(
            '''
                myChart.dispose();
                var myChart = echarts.init(document.getElementById('container'), '{theme}', {{renderer: 'canvas'}});
                myChart.clear();
                window.onresize = function(){{
                    myChart.resize();
                }}
                var option = eval({options});
                myChart.setOption(option);
            '''.format(theme=Visualization.themes[self.themeIndex], options=options)
        )

    def loadUrl(self):
        url = QUrl("file:///template.html")

        self.leftTopView.load(url)
        self.leftTopView.loadFinished.connect(self.setOptions)

        self.BottomView.load(url)
        self.BottomView.loadFinished.connect(self.setOptions)
        self.statusBar().showMessage('准备就绪')

    def setOptions(self):
        if not self.BottomView:
            return
        if not self.BottomEcharts:
            # 初始化echarts
            self.BottomView.page().runJavaScript(
                '''
                    var myChart = echarts.init(document.getElementById('container'), 'light', {renderer: 'canvas'});
                    window.onresize = function(){{
                        myChart.resize();
                    }}
                '''
            )
            self.BottomEcharts = True

        options = self.getOptions(type='K')

        self.BottomView.page().runJavaScript(
            '''
                var option = eval({});
                myChart.setOption(option);
            '''.format(options)
        )

        if not self.leftTopView:
            return
        if not self.leftTopEcharts:
            # 初始化echarts
            self.leftTopView.page().runJavaScript(
                '''
                    var myChart = echarts.init(document.getElementById('container'), 'light', {renderer: 'canvas'});
                    window.onresize = function(){{
                        myChart.resize();
                    }}
                '''
            )
            self.leftTopEcharts = True

        options = self.getOptions(type='Pie')

        self.leftTopView.page().runJavaScript(
            '''
                var option = eval({});
                myChart.setOption(option);
            '''.format(options)
        )

    def getOptions(self,type):
        if type==None or type=='K':
            return self.createKlines()
        elif type=='Pie':
            return self.create_pie(v=[3000,600,5000])


    def createKlines(self):
        overlap = Overlap()
        for quote in self.quote_data:
            line = Line(quote['title'])
            print(quote)
            line.add('open',quote['date'],quote['open'],is_smooth=True)
            line.add('close',quote['date'],quote['close'],is_smooth=True)
            line.add('high',quote['date'],quote['high'],is_smooth=True)
            line.add('low',quote['date'],quote['low'],is_smooth=True)

            overlap.add(line)

        snippet = TRANSLATOR.translate(overlap.options)
        options = snippet.as_snippet()
        return options

    def create_pie(self, v):
        pie = Pie()
        pie.add("昨日行情",['涨','平','跌'], v, is_label_show=True)
        snippet = TRANSLATOR.translate(pie.options)
        options = snippet.as_snippet()
        return options


    def initDataSet(self):
        client = pymongo.MongoClient(host="localhost", port=27017)
        db = client['stock']
        table_basic = db['basic']

        self.stock_basis = myDict.AllowKeyRepeatDict()
        for basic in table_basic.find():
            self.stock_basis.add(key=basic['name'], value=basic['code'])

        self.quote_data = []

        stock_name = '中信证券'
        stock_code = self.stock_basis.query(key=stock_name)[0]
        title = stock_name + '_' + stock_code
        table_quote = db[title]
        queryDateRange = [20190301,20191130]
        date = []
        open = []
        close = []
        high = []
        low = []
        # 为什么不能用 in 而要用 gte lte
        for quote in table_quote.find({'date':{'$gte':queryDateRange[0],'$lte':queryDateRange[1]}}).sort('date',pymongo.ASCENDING):
            date.append(str(quote['date']))
            open.append(float(quote['open']))
            close.append(float(quote['close']))
            high.append(float(quote['high']))
            low.append(float(quote['low']))


        self.quote_data.append({
            'title':title,
            'date':date,
            'open':open,
            'close': close,
            'high': high,
            'low': low

        })
        self.statusBar().showMessage('数据加载完成')
        print('数据加载完成')




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Visualization()
    form.show()
    sys.exit(app.exec_())
import os
import time

import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QTreeWidgetItem

from core.actionCSV import *
from core.run_algorithm import runAlgorithm


class detailClusterred(QMainWindow):
    def __init__(self, parent=None):
        super(detailClusterred, self).__init__()
        loadUi("view/detailClustered.ui", self)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("view/Clustering_App.ui", self)
        self.widgetPieChart.setContentsMargins(0, 0, 0, 0)
        self.lay = QtWidgets.QHBoxLayout(self.widgetPieChart)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.loadFile.clicked.connect(self.loadDataset)
        self.browserDir.clicked.connect(self.getFileName)
        self.getBaseInDataset.clicked.connect(self.getBaseInDatasetFunc)
        self.getBaseInFile.clicked.connect(self.getBaseInFileFunc)
        self.btn_saveFile.clicked.connect(self.saveFileName)
        self.btn_Run.clicked.connect(self.runBtnAction)
        self.detailWindows = detailClusterred(self)
        self.btn_detail.clicked.connect(self.showDetail)
        self.fieldBaseLabel.setWordWrap(True)
        self.tabAll.currentChanged.connect(self.checkTabCurrent)
        self.tableWidgetPredict.setColumnWidth(0, 440)
        self.tableWidgetPredict.setColumnWidth(1, 297)
        self.btnResetPredict.clicked.connect(self.resetPredict)
        self.show()

    """
    --------------------------------------TAB1-----------------------------------------------------------
    """

    def getFileName(self):
        file_filter = 'Data File (*.csv);'
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.loadFile,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data File (*.csv)'
        )
        # print(response)
        self.dirtext.setText(response[0])

    def loadDataset(self):
        # Xóa tất cả cá biến
        # biến tab1
        self.n_Sample.clear()
        self.n_Field.clear()
        self.listViewField.clear()
        self.delVar(["dataset", "header"])
        # try:
        #     del self.dataset, self.header
        # except:
        #     pass
        # Biến tab2
        self.cbb_FieldBase.clear()
        self.fieldBaseLabel.clear()
        self.listWidgetFeildBase.clear()
        self.n_clusterBaseLabel.clear()
        self.delVar(["headerBase", "datasetBase_raw", "datasetBase", "kMin"])
        # try:
        #     del self.headerBase, self.datasetBase_raw, self.datasetBase, self.kMin
        # except:
        #     pass
        #  biến tab3
        self.kMax.clear()
        self.listWidgetField4Run.clear()
        self.delVar(["clusteredData", "listPercent", "labels", "field4RunList"])
        # try:
        #     del self.clusteredData, self.listPercent, self.labels, self.field4RunList
        # except:
        #     pass
        # đọc từ file
        dir = self.dirtext.toPlainText()
        if dir.strip() == "" or not os.path.exists(dir):
            self.showdialog("Đường dẫn không hợp lệ hoặc tập tin không tồn tại!")
        else:
            self.dataset, self.header = readDataset(dir)
            self.n_Sample.setText(str(len(self.dataset)))
            self.n_Field.setText(str(len(self.header)))
            for item in self.header:
                if "\ufeff" in item:
                    item.replace("\ufeff", "")
                # print(item)
                self.listViewField.addItem(item)

    """
    --------------------------------------------------TAB2-----------------------------------------------------
    """

    def getBaseInFileFunc(self):
        # Biến tab2
        self.cbb_FieldBase.clear()
        self.fieldBaseLabel.clear()
        self.listWidgetFeildBase.clear()
        self.n_clusterBaseLabel.clear()
        self.delVar(["headerBase", "datasetBase_raw", "datasetBase", "kMin"])

        # try:
        #     del self.headerBase, self.datasetBase_raw, self.datasetBase, self.kMin
        # except:
        #     pass
        #  biến tab3
        self.kMax.clear()
        self.listWidgetField4Run.clear()
        self.delVar(["clusteredData", "listPercent", "labels", "field4RunList"])

        # try:
        #     del self.clusteredData, self.listPercent, self.labels, self.field4RunList
        # except:
        #     pass
        #
        file_filter = 'Data File (*.csv)'
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.getBaseInFile,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data File (*.csv)'
        )
        dir = response[0]
        try:
            self.datasetBase_raw, self.headerBase = readDataset(dir)
        except:
            self.showdialog("File không tồn tại!")
            return
        self.cbb_FieldBase.clear()
        self.setOption2cbbBase(self.headerBase)
        self.cbb_FieldBase.currentIndexChanged.connect(self.indexChanged1)
        # self.indexChanged(self.cbb_FieldBase.currentIndex())
        self.listWidgetFeildBase.clear()

    def getBaseInDatasetFunc(self):
        # Biến tab2
        self.cbb_FieldBase.clear()
        self.fieldBaseLabel.clear()
        self.listWidgetFeildBase.clear()
        self.n_clusterBaseLabel.clear()
        self.delVar(["headerBase", "datasetBase_raw", "datasetBase", "kMin"])

        # try:
        #     del self.headerBase, self.datasetBase_raw, self.datasetBase, self.kMin
        # except:
        #     pass
        #  biến tab3
        self.kMax.clear()
        self.listWidgetField4Run.clear()
        self.delVar(["clusteredData", "listPercent", "labels", "field4RunList"])

        # try:
        #     del self.clusteredData, self.listPercent, self.labels, self.field4RunList
        # except:
        #     pass

        try:
            self.dataset,
            self.header
        except:
            self.showdialog("Vui lòng thêm tập dữ liệu ở thẻ dataset!")
            return
        # print(self.header)
        self.cbb_FieldBase.clear()
        self.setOption2cbbBase(self.header)
        self.cbb_FieldBase.currentIndexChanged.connect(self.indexChanged0)
        # self.indexChanged(self.cbb_FieldBase.currentIndex())
        self.listWidgetFeildBase.clear()

    def indexChanged1(self, index):
        #  biến tab3
        self.kMax.clear()
        self.listWidgetField4Run.clear()
        self.delVar(["clusteredData", "listPercent", "labels", "field4RunList"])

        # try:
        #     del self.clusteredData, self.listPercent, self.labels, self.field4RunList
        # except:
        #     pass
        if index == 0:
            self.listWidgetFeildBase.clear()
            self.fieldBaseLabel.clear()
            self.n_clusterBaseLabel.clear()
            return
        if index > 0:
            index = index - 1
            self.listWidgetFeildBase.clear()
            # print(index)
            self.datasetBase, val_Cell = cluseringByCell(self.datasetBase_raw, index)
            self.kMin = len(val_Cell)
            self.fieldBaseLabel.setText(self.headerBase[index])
            self.n_clusterBaseLabel.setText(str(len(val_Cell)))
            for item in val_Cell:
                self.listWidgetFeildBase.addItem(item)

    def setOption2cbbBase(self, optionList):
        self.kMax.clear()
        self.listWidgetField4Run.clear()
        self.cbb_FieldBase.addItem("Vui lòng chọn")
        for item in optionList:
            self.cbb_FieldBase.addItem(item)

    def indexChanged0(self, index):
        #  biến tab3
        self.kMax.clear()
        self.listWidgetField4Run.clear()
        self.delVar(["clusteredData", "listPercent", "labels", "field4RunList"])

        # try:
        #     del self.clusteredData, self.listPercent, self.labels, self.field4RunList
        # except:
        #     pass
        if index == 0:
            self.listWidgetFeildBase.clear()
            self.fieldBaseLabel.clear()
            self.n_clusterBaseLabel.clear()
            return
        if index > 0:
            index = index - 1
            self.listWidgetFeildBase.clear()
            self.datasetBase, val_Cell = cluseringByCell(self.dataset, index)
            self.kMin = len(val_Cell)
            self.headerBase = []
            self.headerBase = self.header
            # print(self.headerBase[index])
            self.fieldBaseLabel.setText(self.headerBase[index])
            self.n_clusterBaseLabel.setText(str(len(val_Cell)))
            for item in val_Cell:
                # print(item)
                self.listWidgetFeildBase.addItem(item)

    """
    ------------------------------------TAB3-------------------------------------------------
    """

    def showListField4Run(self):
        self.listWidgetField4Run.clear()
        #  Chọn các thuộc tính chung của tập giống và tập phân cụm
        item = QListWidgetItem()
        item.setText("Chọn tất cả")
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidgetField4Run.addItem(item)
        sharedField = list(set(self.header) & set(self.headerBase))
        if len(sharedField) < 2:
            self.showdialog("Vui lòng chọn đúng tập giống")
            self.tabAll.setCurrentIndex(1)
            return
        for itemstr in sharedField:
            item = QListWidgetItem()
            item.setText(itemstr)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidgetField4Run.addItem(item)

        self.listWidgetField4Run.itemChanged.connect(self.item_Changed)

    def item_Changed(self, item):
        if item.text() == "Chọn tất cả":
            if item.checkState() == QtCore.Qt.Checked:
                self.checkAll(True)
            else:
                self.checkAll(False)

    def checkAll(self, state):
        if state:
            for x in range(self.listWidgetField4Run.count()):
                self.listWidgetField4Run.item(x).setCheckState(QtCore.Qt.Checked)
        else:
            for x in range(self.listWidgetField4Run.count()):
                self.listWidgetField4Run.item(x).setCheckState(QtCore.Qt.Unchecked)

    def runBtnAction(self):
        kmax = self.kMax.toPlainText()
        if kmax.isdigit():
            kmax = int(kmax)
            if kmax <= self.kMin:
                self.showdialog(f"Số cụm tối đa phải lớn hơn số cụm tập giống (lớn hơn {self.kMin})")
                return
        else:
            self.showdialog("Vui lòng nhập số cụm tối đa là số")
            return
        self.setProgressBar(5)
        self.field4RunList = self.getField4Run()
        self.setProgressBar(10)
        self.clusteredData, self.listPercent, self.labels = runAlgorithm(self.dataset, self.datasetBase, self.header,
                                                                         self.headerBase, self.field4RunList, kmax)
        self.setProgressBar(98)
        try:
            self.lay.removeWidget(self.chartview)
        except AttributeError:
            pass
        self.tabAll.setCurrentIndex(3)
        # print(self.clusteredData)
        # print(self.listPercent)

    def getField4Run(self):
        field4RunList = []
        for x in range(1, self.listWidgetField4Run.count()):
            if self.listWidgetField4Run.item(x).checkState() == QtCore.Qt.Checked:
                field4RunList.append(self.listWidgetField4Run.item(x).text())
        if len(field4RunList) >= 2:
            return field4RunList
        else:
            self.showdialog("Vui lòng chọn ít nhất 2 trường phân để phân loại")
            return

    """
    ----------------------------------TAB4---------------------------------------------------
    """

    def create_piechart(self):
        try:
            self.lay.removeWidget(self.chartview)
        except:
            pass
        series = QPieSeries()
        for i in range(len(self.listPercent)):
            series.append(f"Nhóm {i + 1}", self.listPercent[i])
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Tổng quang các cụm")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        self.chartview = QChartView(chart)
        # chartview.setRenderHint(QPainter.Antialiasing)
        self.lay.addWidget(self.chartview)

    def showDetail(self):
        self.detailWindows.treeDetail.clear()
        self.detailWindows.show()
        print(self.field4RunList)
        for i in range(len(self.clusteredData)):
            tmp = QTreeWidgetItem([f"Nhóm {i + 1}"])
            self.detailWindows.treeDetail.addTopLevelItem(tmp)
            for k in range(len(self.clusteredData[i])):
                tmpChild = QTreeWidgetItem([f"{self.field4RunList[k]} :"])
                tmp.addChild(tmpChild)
                tmpChild.addChild(QTreeWidgetItem([f"{self.clusteredData[i][k]}"]))

    def saveFileName(self):
        file_filter = 'Data File (*.csv)'
        response = QtWidgets.QFileDialog.getSaveFileName(
            parent=self.btn_saveFile,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data File (*.csv)'
        )
        try:
            print(self.field4RunList)
            saveResult(response[0], np.array(self.dataset), self.labels, len(self.clusteredData), self.header)
        except:
            return

    """
    ------------------------------------------TAB5---------------------------------------------------------------
    """

    def viewTablePredict(self):
        def getCellValue(cellId, list):
            tmp = []
            for item in list:
                if item[cellId] not in tmp:
                    tmp.append(item[cellId])
            return tmp

        self.tableWidgetPredict.clearContents()
        self.tableWidgetPredict.setRowCount(len(self.field4RunList))
        self.listCBB = []
        for k in range(len(self.field4RunList)):
            self.tableWidgetPredict.setItem(k, 0, QtWidgets.QTableWidgetItem(f"{self.field4RunList[k]}"))
            self.listCBB.append(QtWidgets.QComboBox())
            self.listCBB[k].clear()
            self.listCBB[k].addItems(getCellValue(k, self.clusteredDataPredict))
            self.tableWidgetPredict.setCellWidget(k, 1, self.listCBB[k])
            self.listCBB[k].currentIndexChanged.connect(
                lambda: self.filterListPredict(self.listCBB[self.tableWidgetPredict.currentRow()].currentIndex(),
                                               self.listCBB[self.tableWidgetPredict.currentRow()].currentText(),
                                               self.tableWidgetPredict.currentRow()))

    def filterListPredict(self, index, text, cellId):
        for item in self.clusteredDataPredict:
            if text not in item[cellId]:
                self.clusteredDataPredict.remove(item)
        self.viewTablePredict()

    def resetPredict(self):
        self.clusteredDataPredict = self.clusteredData.copy()
        self.viewTablePredict()

    """
    ------------------------------------------------------------------------------------------------------
    """

    def delVar(self, list):
        for item in list:
            if item in dir(self):
                exec("del self.%s" % (item))

    def setProgressBar(self, index):
        currentIdx = self.progressBar.value()
        if index > currentIdx:
            for i in range(currentIdx, index, 5):
                self.progressBar.setValue(i)
                time.sleep(0.1)
        if self.progressBar.value() in [i for i in range(95, 101)]:
            self.progressBar.setValue(0)

    def showdialog(self, s):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(s)
        msg.setWindowTitle("Chú ý")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec()

    def checkTabCurrent(self):
        index = self.tabAll.currentIndex()
        # print(index)
        if index == 2:
            try:
                self.dataset,
                self.datasetBase,
                self.header,
                self.headerBase,
                self.kMin
            except:
                self.showdialog("Vui lòng thêm hoàn chỉnh dữ liệu ở 2 thẻ trước!")
                self.tabAll.setCurrentIndex(0)
                return
            # print(self.datasetBase)
            self.showListField4Run()
        if index == 3:
            try:
                self.dataset,
                self.datasetBase,
                self.header,
                self.headerBase
            except:
                self.showdialog("Vui lòng thêm hoàn chỉnh dữ liệu ở 2 thẻ đầu!")
                self.tabAll.setCurrentIndex(0)
                return
            try:
                self.clusteredData,
                self.listPercent
            except:
                self.showdialog("Vui lòng chạy thuật toán ở thẻ trước")
                self.tabAll.setCurrentIndex(2)
                return
            self.create_piechart()
        if index == 4:
            try:
                self.dataset,
                self.datasetBase,
                self.header,
                self.headerBase
            except:
                self.showdialog("Vui lòng thêm hoàn chỉnh dữ liệu ở 2 thẻ đầu!")
                self.tabAll.setCurrentIndex(0)
                return
            try:
                self.clusteredData,
                self.listPercent
            except:
                self.showdialog("Vui lòng chạy thuật toán ở thẻ trước")
                self.tabAll.setCurrentIndex(2)
                return
            self.clusteredDataPredict = self.clusteredData.copy()
            self.viewTablePredict()

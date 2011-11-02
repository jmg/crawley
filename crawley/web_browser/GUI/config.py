# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Sun Oct 23 23:18:00 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FrmConfig(object):
    def setupUi(self, FrmConfig):
        FrmConfig.setObjectName("FrmConfig")
        FrmConfig.resize(400, 131)
        self.bt_ok = QtGui.QPushButton(FrmConfig)
        self.bt_ok.setGeometry(QtCore.QRect(310, 100, 81, 27))
        self.bt_ok.setObjectName("bt_ok")
        self.bt_cancel = QtGui.QPushButton(FrmConfig)
        self.bt_cancel.setGeometry(QtCore.QRect(220, 100, 81, 27))
        self.bt_cancel.setObjectName("bt_cancel")
        self.formLayoutWidget = QtGui.QWidget(FrmConfig)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.tb_start_url = QtGui.QLineEdit(self.formLayoutWidget)
        self.tb_start_url.setObjectName("tb_start_url")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.tb_start_url)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.cb_max_depth = QtGui.QComboBox(self.formLayoutWidget)
        self.cb_max_depth.setObjectName("cb_max_depth")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cb_max_depth)

        self.retranslateUi(FrmConfig)
        QtCore.QMetaObject.connectSlotsByName(FrmConfig)

    def retranslateUi(self, FrmConfig):
        FrmConfig.setWindowTitle(QtGui.QApplication.translate("FrmConfig", "Project Configuration ", None, QtGui.QApplication.UnicodeUTF8))
        self.bt_ok.setText(QtGui.QApplication.translate("FrmConfig", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.bt_cancel.setText(QtGui.QApplication.translate("FrmConfig", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FrmConfig", "Start Url", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FrmConfig", "Max Depth", None, QtGui.QApplication.UnicodeUTF8))


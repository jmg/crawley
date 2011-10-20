# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Wed Oct 19 23:22:39 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FrmConfig(object):
    def setupUi(self, FrmConfig):
        FrmConfig.setObjectName("FrmConfig")
        FrmConfig.resize(414, 291)
        self.bt_ok = QtGui.QPushButton(FrmConfig)
        self.bt_ok.setGeometry(QtCore.QRect(320, 260, 81, 27))
        self.bt_ok.setObjectName("bt_ok")
        self.bt_cancel = QtGui.QPushButton(FrmConfig)
        self.bt_cancel.setGeometry(QtCore.QRect(230, 260, 81, 27))
        self.bt_cancel.setObjectName("bt_cancel")
        self.tb_config = QtGui.QPlainTextEdit(FrmConfig)
        self.tb_config.setGeometry(QtCore.QRect(10, 10, 391, 241))
        self.tb_config.setObjectName("tb_config")

        self.retranslateUi(FrmConfig)
        QtCore.QMetaObject.connectSlotsByName(FrmConfig)

    def retranslateUi(self, FrmConfig):
        FrmConfig.setWindowTitle(QtGui.QApplication.translate("FrmConfig", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.bt_ok.setText(QtGui.QApplication.translate("FrmConfig", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.bt_cancel.setText(QtGui.QApplication.translate("FrmConfig", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


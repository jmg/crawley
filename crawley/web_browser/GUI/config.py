# -*- coding: utf-8 -*-

"""
    Project configuration dialog form implementation.

    Ported from the Qt Designer ``config.ui`` generated PyQt4 module to
    PySide6. Widgets now live in ``QtWidgets``.
"""

from PySide6 import QtCore, QtWidgets


class Ui_FrmConfig(object):
    def setupUi(self, FrmConfig):
        FrmConfig.setObjectName("FrmConfig")
        FrmConfig.resize(400, 131)
        self.bt_ok = QtWidgets.QPushButton(FrmConfig)
        self.bt_ok.setGeometry(QtCore.QRect(310, 100, 81, 27))
        self.bt_ok.setObjectName("bt_ok")
        self.bt_cancel = QtWidgets.QPushButton(FrmConfig)
        self.bt_cancel.setGeometry(QtCore.QRect(220, 100, 81, 27))
        self.bt_cancel.setObjectName("bt_cancel")
        self.formLayoutWidget = QtWidgets.QWidget(FrmConfig)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tb_start_url = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.tb_start_url.setObjectName("tb_start_url")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tb_start_url)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cb_max_depth = QtWidgets.QComboBox(self.formLayoutWidget)
        self.cb_max_depth.setObjectName("cb_max_depth")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cb_max_depth)

        self.retranslateUi(FrmConfig)
        QtCore.QMetaObject.connectSlotsByName(FrmConfig)

    def retranslateUi(self, FrmConfig):
        _translate = QtCore.QCoreApplication.translate
        FrmConfig.setWindowTitle(_translate("FrmConfig", "Project Configuration "))
        self.bt_ok.setText(_translate("FrmConfig", "Ok"))
        self.bt_cancel.setText(_translate("FrmConfig", "Cancel"))
        self.label.setText(_translate("FrmConfig", "Start Url"))
        self.label_2.setText(_translate("FrmConfig", "Max Depth"))

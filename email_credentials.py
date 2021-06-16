import sys
import configparser
import sqlite3
import os

import smtplib
import mimetypes

from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5.QtWidgets import *
from PyQt5.Qt import QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from add_windows import *

class configFile:

    # def __init__(self):
        # self.Config = configparser.ConfigParser()

    def get_concern(self, concern):
        try:
            concern = concern.replace(" ", "")
            command = "CREATE TABLE IF NOT EXISTS {} (care_id INTEGER PRIMARY KEY, care_name text, care text)".format(concern)
            c.execute(command)
            selector = "SELECT * FROM {}".format(concern)
            c.execute(selector)
            table = c.fetchall()
            conn.commit()
            return(table)
        except:
            return (False)

    def ConfigSectionMap(self, section):

        dict1 = {}
        query = "SELECT * FROM {}".format(section)
        c.execute(query)
        rows = c.fetchall()
        for row in rows:
            dict1[row[0]] = row[1]
        return dict1

    # def addCon(self, name):
    #     new_concern = (name,)
    #     self.c.execute("REPLACE INTO concern (conc) VALUES (?)", new_concern)
    #     self.conn.commit()

    def addTestimonial(self, name, quote):
        new_test = (name, quote)
        c.execute("REPLACE INTO testimonial (name, test) VALUES (?,?)", new_test)
        conn.commit()

    def addCare(self, care_table, care_name, care):
        care_table = care_table.replace(' ', '')
        command  = "REPLACE INTO {0} (care_name, care) VALUES (\'{1}\', \'{2}\')".format(care_table, care_name, care)
        c.execute(command)
        conn.commit()

class LoginForm(QMainWindow):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(700, 400)
        self.setWindowTitle('Email Login')

        #making main widget for grid layout
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QGridLayout()
        wid.setLayout(layout)
        layout1 = QGridLayout()

        #email label and textboc
        email = QLabel('Email:')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.returnPressed.connect(self.Login)
        self.lineEdit_username.setPlaceholderText('email@example.com')

        #password label and text box
        password = QLabel('Password:')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please Enter Password')
        self.lineEdit_password.returnPressed.connect(self.Login)
        self.lineEdit_password.setEchoMode(self.lineEdit_password.Password)

        #checkbox for showing password
        self.echo = QRadioButton('Show Password')
        self.echo.toggled.connect(self.showPass)

        #Login and cancel buttons
        self.go = QPushButton('Login')
        self.go.setDefault(True)
        self.go.clicked.connect(self.Login)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.close)

        #structuring layout
        groupBox = QGroupBox()
        layout1.addWidget(email, 0, 0)
        layout1.addWidget(self.lineEdit_username, 0, 1)
        layout1.addWidget(password, 1, 0)
        layout1.addWidget(self.lineEdit_password, 1, 1)
        layout1.addWidget(self.echo, 2, 0)
        layout.addWidget(self.cancel, 1, 0)
        layout.addWidget(self.go, 1, 1)
        groupBox.setLayout(layout1)
        layout.addWidget(groupBox, 0, 0, 1, 2)


    def showPass(self):
        if self.echo.isChecked():
            self.lineEdit_password.setEchoMode(self.lineEdit_password.Normal)
        else:
            self.lineEdit_password.setEchoMode(self.lineEdit_password.Password)

    def Login(self):
        #This is where I'll figure out the login stuff

        global account
        global server
        global user

        user = self.lineEdit_username.text()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('jaz.zimms@gmail.com', '1969Mb429(')
            self.hide()

            main = Main(self, self.lineEdit_username)
            main.show()

        except smtplib.SMTPException:
            msg = QMessageBox.critical(self, 'Login Failed',
                                             "Username/Password combination incorrect", QMessageBox.Ok |
                                             QMessageBox.Retry, QMessageBox.Ok)

            if msg == QMessageBox.Retry:
                self.Login()

class addCareWindow(QDialog):
    def __init__(self, name, parent = None):
        self.name = name.lineEdit_clientName.text()
        self.concern = name.concern.currentText()
        self.setSelectedCare = name.setSelectedCare
        super(addCareWindow, self).__init__(parent)
        conn = sqlite3.connect('venv/include/config.db')
        c = conn.cursor()
        self.initUI()

    def initUI(self):

        #Where a user can select testimonials and they will be added to the email/preview
        self.resize(700, 600)
        self.setWindowTitle('Select Care: {}'.format(self.concern))

        #send to function to create table
        self.createTable()

        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()

        self.setLayout(Vlayout)

        self.addCareButton = QPushButton()
        self.addCareButton.setText('Add Care')
        self.addCareButton.clicked.connect(self.newCare)
        self.continueButton = QPushButton()
        self.continueButton.setText('Continue')
        self.continueButton.setDefault(True)
        self.continueButton.clicked.connect(self.saveList)

        Vlayout.addWidget(self.table)
        Hlayout.addWidget(self.addCareButton)
        Hlayout.addWidget(self.continueButton)
        Vlayout.addLayout(Hlayout)

    def createTable(self):

        self.table = QTableWidget()
        care_list = configFile().get_concern(self.concern)
        self.row_count = len(care_list)
        self.perm_row_count = len(care_list)
        self.table.setRowCount(self.row_count)
        self.table.setColumnCount(2)
        self.table.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.table.setMinimumHeight(300)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setWordWrap(True)

        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for row in care_list:
            self.table.setItem(row[0]-1, 0, QTableWidgetItem(row[1]))
            self.table.setItem(row[0]-1, 1, QTableWidgetItem(row[2]))
            self.table.setColumnWidth(0, 300)
            self.table.setColumnWidth(1, 400)
            if not self.setSelectedCare:
                self.table.selectRow(row[0]-1)


        if self.setSelectedCare:
            for row in self.setSelectedCare:
                self.table.selectRow(row)

    def newCare(self):
        # THIS IS WHERE I'LL ADD THE DIALOG THAT RETURNS THE NAME AND CARE
        self.row_count += 1
        self.table.setRowCount(self.row_count)

    def saveList(self):
        new_cares = self.row_count - self.perm_row_count
        concern_name = self.concern.replace(' ', '')
        for row in range (self.perm_row_count, self.row_count):
            care_name = self.table.item(row, 0)

            care = self.table.item(row, 1)
            try:
                care_name = care_name.text()
                care = care.text()
                insert_command = "REPLACE INTO {} (care_name, care) VALUES (?, ?)".format(concern_name)
                c.execute(insert_command, (care_name, care,))
            except:
                continue
        conn.commit()
        self.accept()

    def getSelection(self):
        self.setSelectedCare = [x.row() for x in self.table.selectionModel().selectedRows()]
        care_dict = {}
        for currentQTableWidgetItem in self.table.selectedItems():
            if currentQTableWidgetItem.column() == 0:
                carename = currentQTableWidgetItem.text()
            else:
                care_dict[carename] = currentQTableWidgetItem.text()

        return(care_dict, self.setSelectedCare)


class addTestWindow(QDialog):
    def __init__(self, name, parent = None):
        self.name = name.lineEdit_clientName.text()
        self.setSelected = name.setSelected
        super(addTestWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        #Where a user can select testimonials and they will be added to the email/preview
        self.resize(700, 600)
        self.setWindowTitle('Select Testimonial: {}'.format(self.name))

        #send to function to create table
        self.createTable()

        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()

        self.setLayout(Vlayout)

        self.addTestButton = QPushButton()
        self.addTestButton.setText('Add Testimonial')
        self.addTestButton.clicked.connect(self.newTestimonial)
        self.continueButton = QPushButton()
        self.continueButton.setText('Continue')
        self.continueButton.setDefault(True)
        self.continueButton.clicked.connect(self.saveList)

        Vlayout.addWidget(self.table)
        Hlayout.addWidget(self.addTestButton)
        Hlayout.addWidget(self.continueButton)
        Vlayout.addLayout(Hlayout)

    def createTable(self):
        self.table = QTableWidget()
        test_list = configFile().ConfigSectionMap('Testimonial')
        self.row_count = len(test_list)
        self.perm_row_count = len(test_list)
        self.table.setRowCount(self.row_count)
        self.table.setColumnCount(2)

        self.table.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.table.setMinimumHeight(300)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setWordWrap(True)

        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for row, name in enumerate(test_list):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(test_list[name]))
            self.table.setColumnWidth(0, 300)
            self.table.setColumnWidth(1, 600)

        if self.setSelected:
            for row in self.setSelected:
                self.table.selectRow(row)
        # self.table.selectRow()

    def newTestimonial(self):
        # THIS IS WHERE I'LL ADD THE DIALOG THAT RETURNS THE NAME AND CARE
        self.row_count += 1
        self.table.setRowCount(self.row_count)

    def saveList(self):
        # self.perm_row_count
        for row in range (self.row_count):
            test_name = self.table.item(row, 0)
            test = self.table.item(row, 1)
            try:
                test_name = test_name.text()
                test = test.text()
                c.execute("REPLACE INTO testimonial (name, test) VALUES (?, ?)", (test_name, test,))
            except:
                continue

        conn.commit()
        self.accept()

    def getSelection(self):
        self.setSelected = [x.row() for x in self.table.selectionModel().selectedRows()]
        testimonial_dict = {}
        for currentQTableWidgetItem in self.table.selectedItems():
            if currentQTableWidgetItem.column() == 0:
                personname = currentQTableWidgetItem.text()
            else:
                testimonial_dict[personname] = currentQTableWidgetItem.text()

        return(testimonial_dict, self.setSelected)


class Main(QMainWindow):

    def __init__(self, usernm, parent=None):
        self.usernm = usernm.lineEdit_username.text()
        super(Main, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setSelected = []
        self.setSelectedCare = []
        self.care_dict, self.test_dict = {}, {}
        #this is the main window with all the other thing
        self.resize(1200, 800)
        self.setWindowTitle('Client Concern Center')
        # making main widget for grid layout
        Vlayout = QVBoxLayout()
        gridlayout1 = QGridLayout()
        gridlayout2 = QHBoxLayout()
        gridlayout3 = QGridLayout()
        Hlayout = QHBoxLayout()
        widget = QWidget(self)
        widget.setLayout(Vlayout)
        self.setCentralWidget(widget)

        #client's email input
        clientlabel = QLabel('Client\'s Email')
        self.lineEdit_clientemail = QLineEdit()
        self.lineEdit_clientemail.setPlaceholderText('email@example.com')
        clientName = QLabel('Client\'s Name')
        self.lineEdit_clientName = QLineEdit()
        self.lineEdit_clientName.setPlaceholderText('Name')

        #concern dropdown
        concernlabel = QLabel('Client Concern')
        self.concern = QComboBox(self)
        self.concern.addItem('Select Concern')
        concern_list = configFile().ConfigSectionMap('concern')
        for concern in concern_list:
            self.concern.addItem(concern_list[concern])

        self.add_concern = QPushButton('Add Concern')
        self.add_concern.clicked.connect(self.addConcern)

        #testimonial and basic care selections
        self.care = QPushButton('Basic Care')
        self.care.clicked.connect(self.addCare)
        self.care_check = QCheckBox(self)
        # self.care_check.clicked.connect(self.careCheck)

        self.test = QPushButton('Testimonial')
        self.test.clicked.connect(self.addTest)
        self.test_check = QCheckBox(self)
        # self.test_check.clicked.connect(self.testCheck)

        #preview
        self.preview_box = QTextEdit()
        self.preview_box.setAcceptRichText(True)

        #preview button
        self.preview = QPushButton('Preview')
        self.preview.clicked.connect(self.makePreview)

        #send button
        self.send = QPushButton('Send Email')
        self.send.clicked.connect(self.sendEmail)

        #attach button
        c.execute("SELECT item FROM misc WHERE id = 1")
        path = c.fetchall()
        fpath = path[0][0]
        if fpath:
            fpath = fpath.split('/')[-1][0:-2]
        else:
            fpath = 'Add Attachment'

        self.attach_button = QPushButton(fpath)
        self.attach_button.setIcon(QtGui.QIcon('venv/include/paperclip-512.png'))
        self.attach_button.clicked.connect(self.addAttachment)

        #Main menu
        editPresetAction = QAction('&Edit Preset Messge', self)
        editPresetAction.setStatusTip('Change message presets.')
        editPresetAction.triggered.connect(self.editPreset)
        # self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Options')
        fileMenu.addAction(editPresetAction)

        clientlabel.setMaximumWidth(180)
        gridlayout1.addWidget(clientlabel, 0, 0, 1, 1)
        gridlayout1.addWidget(self.lineEdit_clientemail, 0, 1, 1, 1)
        gridlayout1.addWidget(clientName,0, 2, 1, 1)
        gridlayout1.addWidget(self.lineEdit_clientName, 0, 3, 1, 1)
        gridlayout1.addWidget(concernlabel, 1, 0, 1, 1)
        gridlayout1.addWidget(self.concern, 1, 1, 1, 1)
        gridlayout1.addWidget(self.add_concern, 1, 2, 1 ,2)
        Vlayout.addLayout(gridlayout1)
        gridlayout2.addWidget(self.care)
        gridlayout2.setStretch(0, 1)
        gridlayout2.addWidget(self.care_check)
        gridlayout2.addWidget(self.test)
        gridlayout2.setStretch(2, 1)
        gridlayout2.addWidget(self.test_check)
        Vlayout.addLayout(gridlayout2)
        groupBox = QGroupBox('Preview:')
        gridlayout3.addWidget(self.preview_box,0,0)
        groupBox.setLayout(gridlayout3)
        Vlayout.addWidget(groupBox)
        # attach button
        Hlayout.addWidget(self.attach_button, alignment=Qt.AlignLeft)
        Hlayout.addWidget(self.preview, alignment=Qt.AlignRight)
        Hlayout.addWidget(self.send, alignment=Qt.AlignRight)

        Hlayout.setStretch(0, 1)
        Vlayout.addLayout(Hlayout)

    def editPreset(self):
        conn.commit()
        form = editPresets(self)
        form.exec_()

    def addAttachment(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select Attachment", "",
                                                "All Files (*);;PDF Files (*.pdf)", options=options)
        if files:
            files = str(files)
            c.execute("INSERT OR REPLACE INTO misc (id, category, item) VALUES (1, ?, ?)", ('path', files,))
            conn.commit()

        c.execute("SELECT item FROM misc WHERE id = 1")
        path = c.fetchall()
        fpath = path[0][0]
        if fpath:
            fpath = fpath.split('/')[-1][0:-2]
        else:
            fpath = 'Add Attachment'

        self.attach_button.setIcon(QtGui.QIcon('venv/include/paperclip-512.png'))
        self.attach_button.setText(fpath)
        self.attach_button.update()

    def makePreview(self):
        try:
            name = self.lineEdit_clientName.text()
            concern = str(self.concern.currentText())
            c.execute("SELECT item FROM misc WHERE id = 3")
            intro = c.fetchall()
            intro = intro[0][0].replace('$NAME$', name)
            intro = intro.replace('$CONCERN$', concern)
            c.execute("SELECT item FROM misc WHERE id = 4")
            steps_body = c.fetchall()
            steps_body = steps_body[0][0].replace('$NAME$', name)
            steps_body = steps_body.replace('$CONCERN$', concern)
            c.execute("SELECT item FROM misc WHERE id = 5")
            test_body = c.fetchall()
            test_body = test_body[0][0].replace('$NAME$', name)
            test_body = test_body.replace('$CONCERN$', concern)
            c.execute("SELECT item FROM misc WHERE id = 6")
            signature = c.fetchall()
            signature = signature[0][0].replace('$NAME$', name)
            signature = signature.replace('$CONCERN$', concern)
        except:
            form = editPresets(self)
            form.exec_()
            self.makePreview()

        self.preview_box.setText(intro + '\n\n' + steps_body + '\n')

        if self.care_check.isChecked() == True:
            for num, key in enumerate(self.care_dict):
                self.preview_box.append('\t{0}: {1}\n'.format(num+1, self.care_dict[key]))

        if self.test_check.isChecked() == True:
            self.preview_box.append(test_body+'\n')
            for key in self.test_dict:
                self.preview_box.append('\"{0}\"\n\t\t-{1}\n'.format(self.test_dict[key], key))

        self.preview_box.append(signature)

    def addConcern(self):
        ##This is where the action of adding a new concern will go. A dialog will return the concern.

        conn.commit()

        form = new_concern_button(self)
        form.exec_()
        self.concern.clear()
        self.concern.addItem('Select Concern')
        concern_list = configFile().ConfigSectionMap('concern')
        for concern in concern_list:
            self.concern.addItem(concern_list[concern])

    def addCare(self):
        if self.concern.currentText() != 'Select Concern':
            care = addCareWindow(self, self)
            care.exec_()
            self.care_dict, self.setSelectedCare = care.getSelection()

    def addTest(self):
        test = addTestWindow(self, self)
        test.exec_()
        self.test_dict, self.setSelected = test.getSelection()

    def sendEmail(self):

        self.makePreview()
        c.execute("SELECT item FROM misc WHERE id = 2")
        subject = c.fetchall()
        subject = subject[0][0].replace('$NAME$', self.lineEdit_clientName.text())
        subject = subject.replace('$CONCERN$', str(self.concern.currentText()))

        try:
            msg = MIMEMultipart()
            msg['From'] = self.usernm
            msg['To'] = self.lineEdit_clientemail.text()
            msg['Subject'] = subject

            # add in the message body
            msg.attach(MIMEText(self.preview_box.toPlainText(), 'plain'))
            #Add attachment
            c.execute("SELECT item FROM misc WHERE id = 1")
            path = c.fetchall()
            if path:
                path = path[0][0].strip('[]\'')
                filename = os.path.basename(path)
                attachment = open(path, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(part)

            server.send_message(msg)

            message = QMessageBox(self)
            message.setText('Your message has been sent successfully.')
            message.setWindowTitle('Success!')
            message.exec_()

        except:
            message = QMessageBox.warning(self, 'Sending Error', 'Your message has not been sent. Please check client email and try again.', QMessageBox.Cancel | QMessageBox.Retry, QMessageBox.Cancel)
            if message == QMessageBox.Retry:
                self.sendEmail()

if __name__ == '__main__':

    global conn
    global c
    conn = sqlite3.connect('venv/include/config.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS testimonial (name text, test text)")
    c.execute("CREATE TABLE IF NOT EXISTS concern (id INTEGER PRIMARY KEY, conc text)")
    c.execute("CREATE TABLE IF NOT EXISTS misc (id INTEGER PRIMARY KEY, category text, item text)")
    c.execute("INSERT OR IGNORE INTO misc (id, category) VALUES (1, 'path')")

    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
    conn.commit()
    conn.close()

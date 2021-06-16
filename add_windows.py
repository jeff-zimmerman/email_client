from PyQt5.QtWidgets import *
from PyQt5.Qt import QVBoxLayout
from PyQt5.QtCore import Qt
import sqlite3
import sys

class new_concern_button(QDialog):
    def __init__(self, parent=None):
        # self.usernm = usernm.lineEdit_username.text()
        super(new_concern_button, self).__init__(parent)
        self.initUI()
        self.conn = sqlite3.connect('venv/include/config.db')
        self.c = self.conn.cursor()

    def initUI(self):

        self.setWindowTitle('Add New Concern')
        Vlayout = QVBoxLayout()
        gridlayout1 = QGridLayout()
        groupBox = QGroupBox('Care:')
        gBoxLayout = QHBoxLayout()
        pm_layout = QVBoxLayout()
        add_layout = QHBoxLayout()

        #to enter concern name
        label1 = QLabel('Concern:')
        self.concern_name = QLineEdit()
        self.concern_name.setPlaceholderText('Enter Concern')

        #to enter new care TO DO
        self.row_count = 1
        self.new_careTable = QTableWidget()
        self.new_careTable.setRowCount(self.row_count)
        self.new_careTable.setColumnCount(2)
        self.new_careTable.setColumnWidth(1, 600)
        self.new_careTable.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.new_careTable.setMinimumHeight(500)
        self.new_careTable.horizontalHeader().setStretchLastSection(True)
        #plus and minus buttons
        plus_button = QPushButton('+')
        minus_button = QPushButton('-')
        pm_layout.addWidget(plus_button)
        pm_layout.addWidget(minus_button)
        plus_button.clicked.connect(self.addRow)
        minus_button.clicked.connect(self.deleteRow)

        #add and cancel buttons
        add_button = QPushButton('Save Concern')
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        add_button.clicked.connect(self.saveTable)

        gridlayout1.addWidget(label1, 0, 0)
        gridlayout1.addWidget(self.concern_name, 0, 1)
        Vlayout.addLayout(gridlayout1)
        gBoxLayout.addWidget(self.new_careTable)
        gBoxLayout.addLayout(pm_layout)
        groupBox.setLayout(gBoxLayout)
        Vlayout.addWidget(groupBox)
        add_layout.addWidget(cancel_button)
        add_layout.addWidget(add_button)
        Vlayout.addLayout(add_layout)
        self.setLayout(Vlayout)


    def addRow(self):
        self.row_count += 1
        self.new_careTable.setRowCount(self.row_count)

    def deleteRow(self):
        self.row_count -= 1
        self.new_careTable.setRowCount(self.row_count)

    def saveTable(self):

        concern_name_space = self.concern_name.text()
        concern_name = concern_name_space.replace(' ', '')
        try:
            create_command = "CREATE TABLE IF NOT EXISTS {} (care_id INTEGER PRIMARY KEY, care_name text, care text)".format(
                concern_name)
            self.c.execute(create_command)
        except:
            msg = QMessageBox.critical(self, 'Add New Concern',
                                       "Please enter a concern.", QMessageBox.Retry)
            return(0)
        for row in range(self.row_count):
            care_name = self.new_careTable.item(row, 0)
            care = self.new_careTable.item(row, 1)
            try:
                care_name = care_name.text()
                care = care.text()
                insert_command = "REPLACE INTO {} (care_name, care) VALUES (?, ?)".format(concern_name)
                self.c.execute(insert_command, (care_name, care,))
            except:
                continue

        self.c.execute("REPLACE INTO concern (conc) VALUES (?)", (concern_name_space,))
        self.conn.commit()
        self.conn.close()
        self.close()


class editPresets(QDialog):

    def __init__(self, parent=None):
        # self.usernm = usernm.lineEdit_username.text()
        super(editPresets, self).__init__(parent)
        self.conn = sqlite3.connect('venv/include/config.db')
        self.c = self.conn.cursor()
        self.initUI()

    def initUI(self):
        QDialog()
        self.setWindowTitle('Edit Presets')
        gridLayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.setLayout(gridLayout)
        subjectLayout = QHBoxLayout()
        self.resize(700, 500)

        subjectLabel = QLabel('Email Subject: ')
        self.subject = QLineEdit()
        self.subject.setPlaceholderText('Subject')
        self.introduction = QLineEdit()
        self.introduction.setPlaceholderText('Introduction')
        self.steps_body = QTextEdit()
        self.steps_body.setPlaceholderText('Main Body')
        self.test_body = QTextEdit()
        self.test_body.setPlaceholderText('Testimonial Preset')
        self.signature = QTextEdit()
        self.signature.setPlaceholderText('Signature')

        self.c.execute("SELECT count(*) FROM misc")
        count = self.c.fetchall()[0][0]

        if count > 5:
            self.c.execute("SELECT item FROM misc WHERE id = 2")
            subject = self.c.fetchall()
            self.subject.setText(subject[0][0])
            self.c.execute("SELECT item FROM misc WHERE id = 3")
            intro = self.c.fetchall()
            self.introduction.setText(intro[0][0])
            self.c.execute("SELECT item FROM misc WHERE id = 4")
            steps_body = self.c.fetchall()
            self.steps_body.setText(steps_body[0][0])
            self.c.execute("SELECT item FROM misc WHERE id = 5")
            test_body = self.c.fetchall()
            self.test_body.setText(test_body[0][0])
            self.c.execute("SELECT item FROM misc WHERE id = 6")
            signature = self.c.fetchall()
            self.signature.setText(signature[0][0])

        #Buttons
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.saveMessage)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.accept)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        subjectLayout.addWidget(subjectLabel)
        subjectLayout.addWidget(self.subject)

        gridLayout.addLayout(subjectLayout)
        gridLayout.addWidget(self.introduction, alignment=Qt.AlignLeft)
        gridLayout.addWidget(self.steps_body)
        gridLayout.addWidget(self.test_body)
        gridLayout.addWidget(self.signature, alignment=Qt.AlignLeft)
        gridLayout.addLayout(button_layout)

    def saveMessage(self):

        subject = self.subject.text()
        intro = self.introduction.text()
        steps_body = self.steps_body.toPlainText()
        test_body = self.test_body.toPlainText()
        signature = self.signature.toPlainText()

        self.c.execute("INSERT OR REPLACE INTO misc (id, category, item) VALUES (?, ?, ?)", (2, 'subject', subject,))
        self.c.execute("INSERT OR REPLACE INTO misc (id, category, item) VALUES (?, ?, ?)", (3, 'intro', intro,))
        self.c.execute("INSERT OR REPLACE INTO misc (id, category, item) VALUES (?, ?, ?)", (4, 'steps_body', steps_body,))
        self.c.execute("INSERT OR REPLACE INTO misc (id, category, item) VALUES (?, ?, ?)", (5, 'test_body', test_body,))
        self.c.execute("INSERT OR REPLACE INTO misc (id, category, item) VALUES (?, ?, ?)", (6, 'signature', signature,))

        self.conn.commit()
        self.conn.close()

        self.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    form = editPresets()
    form.show()

    sys.exit(app.exec_())
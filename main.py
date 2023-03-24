import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QScrollArea, QCheckBox


def version():
    v = "Mastery Manager - v0.0"
    return v


class MyWidget(QWidget):
    user = 'Select user'

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel(self.user, self)
        font = label.font()
        font.setPointSize(13)
        label.setFont(font)
        label.move(25, 25)
        quit_btn = QPushButton('Quit', self)
        quit_btn.setGeometry(255, 5, 40, 20)

        # text box with submit button and refresh button
        submit_field = QLineEdit(self)
        submit_field.move(25, 50)
        submit_btn = QPushButton("Search", self)  # magnefying glass as icon
        submit_btn.setGeometry(163, 48, 55, 24)
        submit_btn.clicked.connect(self.clicked_search)
        refresh_btn = QPushButton("Refresh", self)  # refresh arrows as icon
        refresh_btn.setGeometry(220, 48, 55, 24)
        refresh_btn.clicked.connect(self.clicked_refresh)

        # filtering dropdown window with checkboxes, update on refresh button above
        checkbox_mastery_level_7 = QCheckBox('M7', self)
        checkbox_mastery_level_7.move(25, 75)
        checkbox_mastery_level_6 = QCheckBox('M6', self)
        checkbox_mastery_level_6.move(60, 75)
        checkbox_mastery_level_5 = QCheckBox('M5', self)
        checkbox_mastery_level_5.move(95, 75)
        checkbox_mastery_level_4 = QCheckBox('M4', self)
        checkbox_mastery_level_4.move(130, 75)
        checkbox_mastery_level_3 = QCheckBox('M3', self)
        checkbox_mastery_level_3.move(165, 75)
        checkbox_mastery_level_2 = QCheckBox('M2', self)
        checkbox_mastery_level_2.move(200, 75)
        checkbox_mastery_level_1 = QCheckBox('M1', self)
        checkbox_mastery_level_1.move(235, 75)

        # Scroll area for champion population and stat display
        champions_area = QScrollArea(self)
        champions_area.setGeometry(25, 100, 250, 375)

        self.setGeometry(2250, 888, 300, 500)  # x, y, width, height
        self.setWindowTitle(version())

    def clicked_search(self):
        print("Getting user from api")

    def clicked_refresh(self):
        if self.user != "Select user":
            print("Refreshing")
        else:
            print("No user selected")

    def search_filtering(self, checked):
        pass


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()

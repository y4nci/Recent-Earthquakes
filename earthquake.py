import sys
from quaketools import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        get_earthquakes()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Recent Earthquakes")
        self.setGeometry(200, 150, 1600, 900)
        self.search_message = QtWidgets.QLabel("Search in the last 500 earthquakes:")
        self.search_area = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton("Go")
        self.map_button = QtWidgets.QPushButton("See the map")
        self.list_button = QtWidgets.QPushButton("See the last 500 earthquakes")
        self.last_update = QtWidgets.QLabel(f"last update: {datetime.datetime.now()}")

        self.back_button = QtWidgets.QPushButton("Back")

        search_top = QtWidgets.QHBoxLayout()
        search_top.addWidget(self.search_message)
        search_top.addWidget(self.search_area)
        search_top.addWidget(self.search_button)

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addStretch()
        panel_layout.addLayout(search_top)
        panel_layout.addWidget(self.map_button)
        panel_layout.addWidget(self.list_button)
        panel_layout.addStretch()
        panel_layout.addWidget(self.last_update)

        final_layout = QtWidgets.QHBoxLayout()
        final_layout.addStretch()
        final_layout.addLayout(panel_layout)
        final_layout.addStretch()

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(final_layout)

        self.show()

        self.search_button.clicked.connect(self.search)
        self.map_button.clicked.connect(self.show_map)
        self.list_button.clicked.connect(self.show_list)

    def search(self):
        keyword = ascii(self.search_area.text()).upper()
        header = "Date       Time      Latit(N)  Long(E)   Depth(km)     MD   ML   Mw    Region\n" \
                 "---------- --------  --------  -------   ----------    ------------    -----------\n"
        occurrences = []

        with open("data", "r", encoding="utf-8") as file:
            data = file.readlines()

        for quake in data:
            if keyword in quake:
                occurrences.append(quake)

        if len(occurrences) >= 50:
            occurrences = occurrences[:50] + ["..."]

        output = "".join(occurrences)

        if not occurrences:
            header = ""
            output = "No result found."

        self.search_results = QtWidgets.QLabel(header + output)
        self.search_results.setFont(QFont('Courier', 10))

        result_layout = QtWidgets.QHBoxLayout()
        result_layout.addStretch()
        result_layout.addWidget(self.search_results)
        result_layout.addStretch()

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addStretch()
        vlayout.addLayout(result_layout)
        vlayout.addWidget(self.back_button)
        vlayout.addStretch()

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(vlayout)

        self.back_button.clicked.connect(self.init_ui)

        self.show()

    def show_map(self):
        self.earthquake_map = QtWidgets.QLabel()
        pixmap = QPixmap("quakes.jpg")
        self.earthquake_map.setPixmap(pixmap)

        map_layout = QtWidgets.QHBoxLayout()
        map_layout.addStretch()
        map_layout.addWidget(self.earthquake_map)
        map_layout.addStretch()

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addStretch()
        vlayout.addLayout(map_layout)
        vlayout.addWidget(self.back_button)
        vlayout.addStretch()

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(vlayout)

        self.back_button.clicked.connect(self.init_ui)

        self.show()

    def show_list(self):
        self.sort_by = QtWidgets.QComboBox()
        self.sort_by.addItems(["by date", "by latitude", "by longitude", "by depth", "by magnitude", "by location"])
        self.sort_order = QtWidgets.QComboBox()
        self.sort_order.addItems(["ascending", "descending"])
        self.sort_button = QtWidgets.QPushButton("Sort")
        header = "Date       Time      Latit(N)  Long(E)   Depth(km)     MD   ML   Mw    Region\n" \
                 "---------- --------  --------  -------   ----------    ------------    -----------\n"
        text = sort(self.sort_by.currentText(), self.sort_order.currentText())
        self.scrollable = ScrollLabel(self)
        self.scrollable.label.setText(header + text)
        self.scrollable.setFont(QFont('Courier', 12))
        self.scrollable.setGeometry(0, 0, 1600, 750)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(self.sort_by)
        vlayout.addWidget(self.sort_order)
        vlayout.addWidget(self.sort_button)
        vlayout.addWidget(self.back_button)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addStretch()
        hlayout.addLayout(vlayout)
        hlayout.addStretch()

        final_layout = QtWidgets.QVBoxLayout()
        final_layout.addWidget(self.scrollable)
        final_layout.addLayout(hlayout)

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(final_layout)

        # self.scrollit = self.sorted_list()

        self.sort_button.clicked.connect(self.sorted_list)
        self.back_button.clicked.connect(self.init_ui)

        self.show()

    def sorted_list(self):
        header = "Date       Time      Latit(N)  Long(E)   Depth(km)     MD   ML   Mw    Region\n" \
                 "---------- --------  --------  -------   ----------    ------------    -----------\n"
        text = sort(self.sort_by.currentText(), self.sort_order.currentText())
        self.scrollable.label.setText(header + text)
        self.scrollable.setFont(QFont('Courier', 12))
        self.scrollable.setGeometry(0, 0, 1600, 750)


class ScrollLabel(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QtWidgets.QWidget(self)
        self.setWidget(content)
        layout = QtWidgets.QVBoxLayout(content)
        self.label = QtWidgets.QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        self.back_button = QtWidgets.QPushButton("Back")
        layout.addWidget(self.label)

        self.show()


app = QtWidgets.QApplication(sys.argv)

window = Window()

sys.exit(app.exec())









import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from db.database import DeviceReadingsDB, DeviceConfigDB


def main():
    configs = DeviceConfigDB()
    readings = DeviceReadingsDB()
    
    app = QApplication(sys.argv)
    window = MainWindow(configs, readings)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

import sys

from PyQt6.QtWidgets import QApplication

from controller import Controller
from model import Model
from view import View
from config import Config


def main():
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    view.show()

    controller = Controller(view, model)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

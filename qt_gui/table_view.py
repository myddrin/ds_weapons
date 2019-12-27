import math
import sys
from typing import Any

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide2.QtGui import QKeySequence, QColor
from PySide2.QtWidgets import QMainWindow, QAction, QApplication, QHBoxLayout, QSizePolicy, QTableView, QWidget, \
    QHeaderView

from storage.objects import Deck, GameConfig, Weapon, Character


class WeaponDeckView(QAbstractTableModel):

    def __init__(self, deck: Deck, *args, **kwargs):
        super(WeaponDeckView, self).__init__(*args, **kwargs)
        self.deck = deck
        self.game_cfg = GameConfig.normal_game()
        self.n_players = 4

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.deck.weapons)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 1 + len(self.deck.characters)

    def headerData(self, section:int, orientation:Qt.Orientation, role:int) -> Any:
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == 0:
                return 'Card'
            else:
                return self.deck.get_character(section - 1).name.title()
        else:
            return f'{section}'

    def display_level(self, character: Character, weapon: Weapon) -> str:
        souls = character.need_souls(weapon, self.game_cfg)
        if souls is not None:
            souls_per_room = self.game_cfg.souls_per_room(self.n_players)
            return str(math.ceil(souls / souls_per_room))
        return '-'

    def data(self, index, role:int = Qt.DisplayRole) -> Any:
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            weapon = self.deck.get_weapon(row)
            if column == 0:
                return weapon.name
            else:
                character = self.deck.get_character(column - 1)
                return self.display_level(character, weapon)
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Dark Souls Weapons')

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()

        # Game Data
        deck = Deck.from_json_file('../base_game.json')

        # Weapon QWidget
        self.weapon_widget = QWidget()
        weapon_layout = QHBoxLayout()
        self.weapon_widget.setLayout(weapon_layout)

        self.weapon_model = WeaponDeckView(deck)
        table_view = QTableView()
        table_view.setModel(self.weapon_model)

        weapon_layout.addWidget(table_view)
        h_header = table_view.horizontalHeader()
        for i in range(1, self.weapon_model.columnCount()):
            h_header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(0, QHeaderView.Stretch)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.weapon_widget.setSizePolicy(size)

        self.setCentralWidget(self.weapon_widget)

    # def load_file(self, filename: str):
    #     self.status.showMessage(f'Loading {filename}')
    #     self.deck.extend_from_file(filename)
    #     self.status.showMessage(
    #         f'Deck has {len(self.deck.characters)} characters '
    #         f'and {len(self.deck.weapons)} cards'
    #     )


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

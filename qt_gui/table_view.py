import math
import sys
from typing import Any, Optional

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL
from PySide2.QtGui import QKeySequence, QColor
from PySide2.QtWidgets import (
    QMainWindow,
    QAction,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
    QHeaderView,
    QTableView,
    QGridLayout,
    QLabel,
)

from storage.objects import Deck, GameConfig, Weapon, Character, Stats


class WeaponView(QWidget):

    def __init__(self, weapon: Weapon, parent: QWidget):
        # noinspection PyTypeChecker
        super(WeaponView, self).__init__(parent, Qt.WindowType.Dialog)
        layout = QGridLayout()
        layout.addWidget(
            QLabel(weapon.name.title()),
            0, 0,
            1, 3,
        )
        layout.addWidget(
            QLabel(weapon.type.value.title()),
            0, 3,
        )
        if weapon.character is not None:
            character = f'{weapon.character.name.title()} only'
        else:
            character = 'All characters'
        layout.addWidget(
            QLabel(character),
            1, 0,
            1, 3,
        )
        # if weapon.game is not None:
        #     layout.addWidget(
        #         QLabel(f'{weapon.game}'),
        #         1, 3,
        #     )
        stats_row = layout.rowCount()
        for i, s in enumerate(weapon.stats):
            layout.addWidget(
                QLabel(f'{Stats.titles[i]}: {weapon.stats[i]}'),
                stats_row, i,
            )
        self.setWindowTitle(weapon.name.title())
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLayout(layout)


class WeaponDeckView(QAbstractTableModel):

    def __init__(self, deck: Deck, *args, **kwargs):
        super(WeaponDeckView, self).__init__(*args, **kwargs)
        self.deck = deck
        self.game_cfg = GameConfig.normal_game()
        self.n_players = 4
        self.weapon_widget: Optional[QWidget] = None

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.deck.weapons)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 1 + len(self.deck.characters)

    # noinspection PyMethodOverriding
    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> Any:
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

    def data(self, index, role: int = Qt.DisplayRole) -> Any:
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            weapon = self.deck.get_weapon(row)
            if column == 0:
                return weapon.name.title()
            else:
                character = self.deck.get_character(column - 1)
                return self.display_level(character, weapon)
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

    def cell_double_clicked(self, index: QModelIndex):
        weapon = self.deck.get_weapon(index.row())
        print(f'Double clicked "{weapon.name.title()}"')
        weapon_widget = WeaponView(weapon, parent=self.weapon_widget)
        weapon_widget.show()

    @classmethod
    def create_view(cls, deck) -> "WeaponDeckView":
        obj = cls(deck)
        obj.weapon_widget = QWidget()
        weapon_layout = QHBoxLayout()
        obj.weapon_widget.setLayout(weapon_layout)

        table_view = QTableView()
        table_view.setModel(obj)
        # noinspection PyTypeChecker
        obj.connect(table_view, SIGNAL('doubleClicked(QModelIndex)'), obj.cell_double_clicked)

        h_header = table_view.horizontalHeader()
        for i in range(1, obj.columnCount()):
            h_header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(0, QHeaderView.Stretch)

        weapon_layout.addWidget(table_view)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        obj.weapon_widget.setSizePolicy(size)

        return obj


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
        # noinspection PyUnresolvedReferences
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()

        # Game Data
        deck = Deck.from_json_file('../base_game.json')

        # Weapon QWidget
        self.weapon_model = WeaponDeckView.create_view(deck)
        self.setCentralWidget(self.weapon_model.weapon_widget)

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

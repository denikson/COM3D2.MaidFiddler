from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QLineEdit, QDoubleSpinBox , QSpinBox , QCheckBox, QWidget, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt, QObject
from .ui_tab import UiTab
from maidfiddler.ui.qt_elements import NumberElement, TextElement
from maidfiddler.util.translation import tr

class MaidStatsTab(UiTab):
    def __init__(self, ui, core, maid_mgr):
        UiTab.__init__(self, ui, core, maid_mgr)

        self.properties = {}
        self.bonus_properties = {}
        self.type_generators = {
            "int" : lambda: NumberElement(QSpinBox()),
            "double": lambda: NumberElement(QDoubleSpinBox()),
            "string": lambda: TextElement(QLineEdit())
        }

    def update_ui(self):
        self.properties.clear()
        self.bonus_properties.clear()

        self.ui.maid_params_lockable_table      \
            .horizontalHeader()                 \
            .setSectionResizeMode(0, QHeaderView.Stretch)

        self.ui.maid_params_lockable_table      \
            .horizontalHeader()                 \
            .setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ui.maid_params_lockable_table      \
            .horizontalHeader()                 \
            .setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.ui.maid_params_lockable_table.setRowCount(
            len(self.game_data["maid_status_settable"]))

        for (i, maid_prop) in enumerate(self.game_data["maid_status_settable"]):
            prop_type = self.game_data["maid_status_settable"][maid_prop]
            name = QTableWidgetItem(f"maid_props.{maid_prop}")
            line = self.type_generators[prop_type]()
            line.qt_element.setStyleSheet("width: 15em;")

            checkbox = QCheckBox()
            widget = QWidget()
            hbox = QHBoxLayout(widget)
            hbox.addWidget(checkbox)
            hbox.setAlignment(Qt.AlignCenter)
            hbox.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(hbox)

            self.ui.maid_params_lockable_table.setItem(i, 0, name)
            self.ui.maid_params_lockable_table.setCellWidget(i, 1, line.qt_element)
            self.ui.maid_params_lockable_table.setCellWidget(i, 2, widget)

            line.qt_element.setProperty("prop_name", maid_prop)
            checkbox.setProperty("prop_name", maid_prop)
            self.properties[maid_prop] = (line, checkbox)

        # Maid bonus stats table

        self.ui.maid_params_bonus_table     \
            .horizontalHeader()             \
            .setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.maid_params_bonus_table     \
            .horizontalHeader()             \
            .setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ui.maid_params_bonus_table     \
            .setRowCount(len(self.game_data["maid_bonus_status"]))

        for (i, maid_prop) in enumerate(self.game_data["maid_bonus_status"]):
            name = QTableWidgetItem(maid_prop)
            line = QSpinBox()
            line.setStyleSheet("width: 15em;")

            self.ui.maid_params_bonus_table.setItem(i, 0, name)
            self.ui.maid_params_bonus_table.setCellWidget(i, 1, line)

            line.setProperty("prop_name", maid_prop)
            self.bonus_properties[maid_prop] = line

    def init_events(self, event_poller):
        self.ui.maid_list.currentItemChanged.connect(self.maid_selected)

        for prop, widgets in self.properties.items():
            widgets[0].connect(self.commit_property)
            widgets[1].stateChanged.connect(self.commit_lock)

        event_poller.on("maid_prop_changed", self.prop_changed)

    def prop_changed(self, args):
        if args["property_name"] not in self.properties:
            return

        prop = self.properties[args["property_name"]]
        prop[0].set_value(args["value"])

    def commit_property(self):
        element = self.sender()
        prop = element.property("prop_name")
        el = self.properties[prop][0]
        self.core.SetMaidPropertyActive(prop, el.value())

    def commit_bonus(self):
        element = self.sender()
        prop = element.property("prop_name")
        print(f"Setting bonus {prop} to {element.text()}")

    def commit_lock(self, state):
        element = self.sender()
        prop = element.property("prop_name")
        n_state = self.core.ToggleActiveMaidLock(prop, state == Qt.Checked)
        
        element.blockSignals(True)
        element.setCheckState(Qt.Checked if n_state else Qt.Unchecked)
        element.blockSignals(False)

    def maid_selected(self):
        if self.maid_mgr.selected_maid is None:
            return

        maid = self.maid_mgr.selected_maid

        for name, widgets in self.properties.items():
            widgets[0].set_value(maid["properties"][name])
            widgets[1].setCheckState(Qt.Checked if maid["prop_locks"][name] else Qt.Unchecked)
            # TODO: Add lock

        for name, widget in self.bonus_properties.items():
            widget.setValue(maid["bonus_properties"][name])

    def translate_ui(self):
        self.ui.ui_tabs.setTabText(1, tr(self.ui.tab_maid_stats, self.ui.ui_tabs.tabText(1)))
        
        for group in self.ui.tab_maid_stats.findChildren(QGroupBox):
            group.setTitle(tr(group, group.title()))

        for row in range(0, self.ui.maid_params_lockable_table.rowCount()):
            name = self.ui.maid_params_lockable_table.item(row, 0)
            name.setText(tr(name, name.text()))
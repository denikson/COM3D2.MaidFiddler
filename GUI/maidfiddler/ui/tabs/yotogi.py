from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QCheckBox, QSpinBox, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from .ui_tab import UiTab

class YotogiTab(UiTab):
    def __init__(self, ui, core, maid_mgr):
        UiTab.__init__(self, ui, core, maid_mgr)

        self.skill_elements = {}
    
    def update_ui(self):
        self.skill_elements.clear()

        self.ui.yotogi_skills_table.setRowCount(
            len(self.game_data["yotogi_skills"]))

        yotogi_skills_header = self.ui.yotogi_skills_table.horizontalHeader()

        yotogi_skills_header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)
        yotogi_skills_header.setSectionResizeMode(1, QHeaderView.Stretch)
        yotogi_skills_header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)
        yotogi_skills_header.setSectionResizeMode(
            3, QHeaderView.ResizeToContents)
        yotogi_skills_header.setSectionResizeMode(
            4, QHeaderView.ResizeToContents)

        for (i, skill) in enumerate(self.game_data["yotogi_skills"]):
            name = QTableWidgetItem(skill["name"])
            line_level = QSpinBox()
            line_level.setMinimum(0)
            line_level.setMaximum(99999)
            line_exp = QSpinBox()
            line_exp.setMinimum(0)
            line_exp.setMaximum(99999)
            line_play_count = QSpinBox()
            line_play_count.setMinimum(0)
            line_play_count.setMaximum(99999)

            checkbox = QCheckBox()
            widget = QWidget()
            hbox = QHBoxLayout(widget)
            hbox.addWidget(checkbox)
            hbox.setAlignment(Qt.AlignCenter)
            hbox.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(hbox)
            
            checkbox.setProperty("id", skill["id"])
            line_level.setProperty("id", skill["id"])
            line_exp.setProperty("id", skill["id"])
            line_play_count.setProperty("id", skill["id"])

            self.ui.yotogi_skills_table.setCellWidget(i, 0, widget)
            self.ui.yotogi_skills_table.setItem(i, 1, name)
            self.ui.yotogi_skills_table.setCellWidget(i, 2, line_level)
            self.ui.yotogi_skills_table.setCellWidget(i, 3, line_exp)
            self.ui.yotogi_skills_table.setCellWidget(i, 4, line_play_count)

            self.skill_elements[skill["id"]] = (checkbox, line_level, line_exp, line_play_count)

    def init_events(self, event_poller):
        self.ui.maid_list.currentItemChanged.connect(self.maid_selected)

        for (cb, level, exp, play_count) in self.skill_elements.values():
            cb.stateChanged.connect(self.toggle_skill)
            level.valueChanged.connect(self.set_level)
            exp.valueChanged.connect(self.set_exp)
            play_count.valueChanged.connect(self.set_play_count)

        event_poller.on("yotogi_skill_add", self.on_skill_add)
        event_poller.on("yotogi_skill_remove", self.on_skill_remove)

    def on_skill_add(self, args):
        (cb, level, exp, play_count) = self.skill_elements[args["skill_id"]]

        cb.blockSignals(True)
        cb.setCheckState(Qt.Checked)
        cb.blockSignals(False)

        level.blockSignals(True)
        level.setValue(0)
        level.blockSignals(False)

        exp.blockSignals(True)
        exp.setValue(0)
        exp.blockSignals(False)

        play_count.blockSignals(True)
        play_count.setValue(0)
        play_count.blockSignals(False)
    
    def on_skill_remove(self, args):
        (cb, level, exp, play_count) = self.skill_elements[args["skill_id"]]

        cb.blockSignals(True)
        cb.setCheckState(Qt.Unchecked)
        cb.blockSignals(False)

        level.blockSignals(True)
        level.setValue(0)
        level.blockSignals(False)

        exp.blockSignals(True)
        exp.setValue(0)
        exp.blockSignals(False)

        play_count.blockSignals(True)
        play_count.setValue(0)
        play_count.blockSignals(False)

    def toggle_skill(self, state):
        cb = self.sender()
        self.core.ToggleYotogiSkillActive(cb.property("id"), state == Qt.Checked)

    def set_level(self):
        level = self.sender()
        self.core.SetYotogiSkillLevelActive(level.property("id"), level.value())

    def set_exp(self):
        exp = self.sender()
        self.core.SetYotogiSkillExpActive(exp.property("id"), exp.value())

    def set_play_count(self):
        play_count = self.sender()
        self.core.SetYotogiSkillPlayCountActive(play_count.property("id"), play_count.value())

    def maid_selected(self):
        if self.maid_mgr.selected_maid is None:
            return

        maid = self.maid_mgr.selected_maid

        for skill_id, (cb, level, exp, play_count) in self.skill_elements.items():
            cb.blockSignals(True)
            level.blockSignals(True)
            exp.blockSignals(True)
            play_count.blockSignals(True)

            if skill_id not in maid["yotogi_skill_data"]:
                cb.setCheckState(Qt.Unchecked)
                level.setValue(0)
                exp.setValue(0)
                play_count.setValue(0)
            else:
                skill = maid["yotogi_skill_data"][skill_id]
                cb.setCheckState(Qt.Checked)
                level.setValue(skill["level"])
                exp.setValue(skill["cur_exp"])
                play_count.setValue(skill["play_count"])

            cb.blockSignals(False)
            level.blockSignals(False)
            exp.blockSignals(False)
            play_count.blockSignals(False)

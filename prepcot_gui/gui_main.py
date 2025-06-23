import sys
import os
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QTextEdit, QTabWidget, QHBoxLayout, QInputDialog,
    QMessageBox, QListWidget
)
from PySide6.QtGui import QPalette, QColor, QIcon, QFont
from PySide6.QtCore import Qt, QDateTime

from template_manager.template_loader import load_all_templates
from data_mapper.formatter import format_data


def launch_gui():
    app = QApplication(sys.argv)

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prepcot — Apricot Data Assistant")
        self.setGeometry(200, 200, 1000, 650)

        icon_path = os.path.join("icons", "P_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.templates = load_all_templates("templates")
        self.mapping_folder = "value_mappings"
        self.output_folder = "output_data"
        self.log_file = os.path.join("logs", "job_history.log")

        self.loaded_file = None
        self.selected_program = None
        self.preview_data = None
        self.last_output_path = None

        self.init_ui()
        self.setAcceptDrops(True)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # --- Import Tab ---
        import_tab = QWidget()
        import_layout = QVBoxLayout()

        btn_row = QHBoxLayout()
        self.upload_btn = QPushButton("Upload File")
        self.upload_btn.clicked.connect(self.open_file)
        self.format_btn = QPushButton("Prepare for Apricot")
        self.format_btn.clicked.connect(self.confirm_format)
        self.clear_btn = QPushButton("Clear Preview")
        self.clear_btn.clicked.connect(self.clear_preview)
        self.revert_btn = QPushButton("Revert Last Import")
        self.revert_btn.clicked.connect(self.revert_last_output)
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close)

        for btn in [self.upload_btn, self.format_btn, self.clear_btn, self.revert_btn, self.exit_btn]:
            btn_row.addWidget(btn)

        self.preview_box = QTextEdit()
        self.preview_box.setReadOnly(True)
        self.preview_box.setFont(QFont("Courier New", 10))

        import_layout.addLayout(btn_row)
        import_layout.addWidget(self.preview_box)
        import_tab.setLayout(import_layout)
        self.tabs.addTab(import_tab, "Import Preview")

        # --- Log Tab ---
        self.log_tab = QTextEdit()
        self.log_tab.setReadOnly(True)
        self.tabs.addTab(self.log_tab, "Activity Log")
        self.load_log()

        # --- Output Viewer Tab ---
        viewer_tab = QWidget()
        viewer_layout = QVBoxLayout()

        self.output_list = QListWidget()
        self.output_list.itemClicked.connect(self.load_output_file)

        self.output_viewer = QTextEdit()
        self.output_viewer.setReadOnly(True)
        self.output_viewer.setFont(QFont("Courier New", 10))

        viewer_layout.addWidget(QLabel("🗂️ Select a file to view its contents:"))
        viewer_layout.addWidget(self.output_list)
        viewer_layout.addWidget(self.output_viewer)

        viewer_tab.setLayout(viewer_layout)
        self.tabs.addTab(viewer_tab, "Output Viewer")

        layout.addWidget(self.tabs)

        # --- Footer ---
        footer = QHBoxLayout()
        credit = QLabel("Powered by support from the Wilmington Alliance")
        credit.setStyleSheet("color: gray;")
        footer.addStretch()
        footer.addWidget(credit)
        footer.addStretch()
        layout.addLayout(footer)

        main_widget.setLayout(layout)
        self.populate_output_list()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.process_file(file_path)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)")
        if path:
            self.process_file(path)

    def process_file(self, file_path):
        self.loaded_file = None
        self.selected_program = None
        self.preview_data = None

        program = self.select_program_dialog()
        if not program or program not in self.templates:
            self.preview_box.setText("⚠️ Program not selected or unrecognized.")
            return

        try:
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            df = df.iloc[:, 1:]  # Skip first column
            df = df.iloc[:, :5]  # Limit to first 5 columns
            preview = df.head(10).to_string(index=False)

            self.loaded_file = file_path
            self.selected_program = program
            self.preview_data = df

            self.preview_box.setText(preview)
            self.preview_box.append(f"\n✅ Loaded: {os.path.basename(file_path)}")
            self.preview_box.append(f"📁 Program: {program}\nClick 'Prepare for Apricot' to continue...")

        except Exception as e:
            self.preview_box.setText(f"❌ Error loading file:\n{str(e)}")

    def confirm_format(self):
        if not self.loaded_file or not self.selected_program:
            QMessageBox.warning(self, "No File", "Please upload a file before formatting.")
            return

        confirm = QMessageBox.question(
            self, "Proceed?", f"Format this file for '{self.selected_program}'?",
            QMessageBox.Yes | QMessageBox.Cancel
        )
        if confirm == QMessageBox.Yes:
            try:
                output = format_data(
                    input_path=self.loaded_file,
                    template_profile=self.templates[self.selected_program],
                    program_name=self.selected_program,
                    mapping_folder=self.mapping_folder,
                    output_folder=self.output_folder
                )
                self.last_output_path = output
                self.preview_box.append(f"\n✅ Saved to:\n{output}")
                self.append_log_entry(self.selected_program, self.loaded_file, output)
                self.populate_output_list()

            except Exception as e:
                self.preview_box.setText(f"❌ Formatting error:\n{str(e)}")

    def clear_preview(self):
        self.preview_box.clear()
        self.loaded_file = None
        self.selected_program = None
        self.preview_data = None

    def revert_last_output(self):
        if self.last_output_path and os.path.exists(self.last_output_path):
            try:
                os.remove(self.last_output_path)
                self.preview_box.append(f"\n🗑️ Deleted:\n{self.last_output_path}")
                self.last_output_path = None
                self.populate_output_list()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete file:\n{str(e)}")
        else:
            QMessageBox.information(self, "No File", "No output to remove.")

    def select_program_dialog(self):
        options = list(self.templates.keys())
        program, ok = QInputDialog.getItem(self, "Select Program", "Choose a template:", options, 0, False)
        return program if ok else None

    def append_log_entry(self, program, input_file, output_file):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        entry = f"[{timestamp}] • {program}: {os.path.basename(input_file)} ➜ {os.path.basename(output_file)}\n"
        os.makedirs("logs", exist_ok=True)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry)
        self.log_tab.append(entry)

    def load_log(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                self.log_tab.setText(f.read())
        else:
            self.log_tab.setText("No activity yet.")

    def populate_output_list(self):
        self.output_list.clear()
        if os.path.exists(self.output_folder):
            files = [f for f in os.listdir(self.output_folder) if f.endswith(".csv")]
            for f in sorted(files):
                self.output_list.addItem(f)

    def load_output_file(self, item):
        file_path
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QSplitter, QVBoxLayout, 
    QHBoxLayout, QPushButton, QFrame, QLabel, QGridLayout, QInputDialog,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt


class PyrometerWidget(QFrame):
    """A single Pyrometer display widget."""
    def __init__(self, index: int, name: str = None):
        super().__init__()
        self.index = index
        self.name = name or f"Pyrometer {index+1}"
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background: #f8f9fa; border: 1px solid #ccc; border-radius: 8px;")

        self.layout = QVBoxLayout(self)
        self.title = QLabel(self.name)
        self.title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.value = QLabel("-- °C")
        self.value.setStyleSheet("font-size: 12px; color: #444;")

        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.value, alignment=Qt.AlignCenter)

    def set_name(self, name: str):
        """Update the pyrometer's display name."""
        self.name = name
        self.title.setText(name)


class ConfigureNamesDialog(QDialog):
    """Dialog for renaming pyrometers."""
    def __init__(self, names: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Pyrometer Names")
        self.resize(300, 400)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.line_edits = []
        for i, name in enumerate(names):
            edit = QLineEdit(name)
            self.line_edits.append(edit)
            form_layout.addRow(f"Pyrometer {i+1}:", edit)

        layout.addLayout(form_layout)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_names(self) -> list[str]:
        """Return updated names from user."""
        return [edit.text().strip() or f"Pyrometer {i+1}" 
                for i, edit in enumerate(self.line_edits)]


class PyrometerDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pyrometer Dashboard")
        self.setGeometry(200, 100, 1000, 600)

        # Split screen (top/bottom)
        splitter = QSplitter(Qt.Vertical)
        self.setCentralWidget(splitter)

        # Top part
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Configure button bar
        button_bar = QHBoxLayout()
        button_bar.addStretch()

        self.config_button = QPushButton("⚙ Configure Count")
        self.config_button.clicked.connect(self.configure_pyrometers)
        button_bar.addWidget(self.config_button)

        self.name_button = QPushButton("✏ Configure")
        self.name_button.clicked.connect(self.configure_names)
        button_bar.addWidget(self.name_button)

        top_layout.addLayout(button_bar)

        # Pyrometer grid container
        self.pyrometer_container = QWidget()
        self.grid_layout = QGridLayout(self.pyrometer_container)
        top_layout.addWidget(self.pyrometer_container)

        splitter.addWidget(top_widget)

        # Bottom part (logs/graphs placeholder)
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        placeholder = QLabel("Bottom area (Logs / Graphs / Details)")
        placeholder.setStyleSheet("color: gray; font-style: italic;")
        bottom_layout.addWidget(placeholder, alignment=Qt.AlignCenter)
        splitter.addWidget(bottom_widget)

        splitter.setSizes([500, 400])  # initial sizes

        # Default 16 pyrometers
        self.num_pyrometers = 16
        self.pyrometer_names = [f"Pyrometer {i+1}" for i in range(16)]
        self.create_pyrometers()

    def create_pyrometers(self):
        """Create dynamic grid of pyrometer widgets."""
        # Clear existing widgets
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Determine grid size (square-like distribution)
        cols = int(self.num_pyrometers ** 0.5)
        if cols * cols < self.num_pyrometers:
            cols += 1
        rows = (self.num_pyrometers + cols - 1) // cols

        # Add pyrometer widgets
        for i in range(self.num_pyrometers):
            r, c = divmod(i, cols)
            widget = PyrometerWidget(i, self.pyrometer_names[i])
            self.grid_layout.addWidget(widget, r, c)

        self.grid_layout.setSpacing(10)

    def configure_pyrometers(self):
        """Ask user for number of pyrometers and update grid."""
        count, ok = QInputDialog.getInt(
            self, "Configure Count", "Enter number of pyrometers (1-16):",
            value=self.num_pyrometers, min=1, max=16
        )
        if ok:
            self.num_pyrometers = count
            # Keep or trim names
            if len(self.pyrometer_names) < count:
                self.pyrometer_names.extend([f"Pyrometer {i+1}" for i in range(len(self.pyrometer_names), count)])
            else:
                self.pyrometer_names = self.pyrometer_names[:count]
            self.create_pyrometers()

    def configure_names(self):
        """Open dialog to rename pyrometers."""
        dialog = ConfigureNamesDialog(self.pyrometer_names[:self.num_pyrometers], self)
        if dialog.exec_():
            self.pyrometer_names[:self.num_pyrometers] = dialog.get_names()
            self.create_pyrometers()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyrometerDashboard()
    window.show()
    sys.exit(app.exec_())

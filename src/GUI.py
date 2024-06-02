import sys
import json
import globals
from DSM import DSM
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMessageBox

class DSMGui(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DSM Simulator')
        
        layout = QVBoxLayout()

        self.total_pages_label = QLabel('Total Pages:', self)
        self.total_pages_input = QLineEdit(self)
        layout.addWidget(self.total_pages_label)
        layout.addWidget(self.total_pages_input)

        self.cpus_label = QLabel('CPUs:', self)
        self.cpus_input = QLineEdit(self)
        layout.addWidget(self.cpus_label)
        layout.addWidget(self.cpus_input)

        self.pages_per_cpu_label = QLabel('Pages per CPU:', self)
        self.pages_per_cpu_input = QLineEdit(self)
        layout.addWidget(self.pages_per_cpu_label)
        layout.addWidget(self.pages_per_cpu_input)

        self.algorithm_label = QLabel('Algorithm (LRU, OPTIMAL, FIFO):', self)
        self.algorithm_input = QLineEdit(self)
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_input)

        self.replication_label = QLabel('Replication (True/False):', self)
        self.replication_input = QLineEdit(self)
        layout.addWidget(self.replication_label)
        layout.addWidget(self.replication_input)

        self.references_label = QLabel('References File:', self)
        self.references_input = QLineEdit(self)
        self.references_button = QPushButton('Browse', self)
        self.references_button.clicked.connect(self.load_references)
        layout.addWidget(self.references_label)
        layout.addWidget(self.references_input)
        layout.addWidget(self.references_button)

        self.config_button = QPushButton('Load Config File', self)
        self.config_button.clicked.connect(self.load_config)
        layout.addWidget(self.config_button)

        self.start_button = QPushButton('Start Simulation', self)
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_references(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load References File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            self.references_input.setText(file_name)

    def load_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Config File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as cf:
                config = json.load(cf)
                self.total_pages_input.setText(str(config['total_pages']))
                self.cpus_input.setText(str(config['cpus']))
                self.pages_per_cpu_input.setText(str(config['pages_per_cpu']))
                self.algorithm_input.setText(config['algorithm'])
                self.replication_input.setText(str(config['replication']))
            self.references_input.setText(file_name.replace("config", "references"))

    def start_simulation(self):
        try:
            total_pages = int(self.total_pages_input.text())
            cpus = int(self.cpus_input.text())
            pages_per_cpu = int(self.pages_per_cpu_input.text())
            algorithm = self.algorithm_input.text().upper()
            replication = self.replication_input.text().lower() == 'true'
            references_file = self.references_input.text()

            with open(references_file, 'r') as rf:
                references = [tuple(ref) for ref in json.load(rf)]

            globals.init(
                Total_pages=total_pages,
                num_CPUs=cpus,
                Pages_per_cpu=pages_per_cpu,
                Algorithm=algorithm,
                Replication=replication,
                References=references
            )

            dsm = DSM()
            dsm.simulate(1)  # You can add an interval input if needed

            self.result_label.setText("Simulation completed successfully.")
            self.show_message("Success", "Simulation completed successfully.")
        except Exception as e:
            self.show_message("Error", str(e))

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    ex = DSMGui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
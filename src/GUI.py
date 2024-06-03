import sys
import json
import globals
from DSM import DSM
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import QPropertyAnimation, QRectF, Qt, QPointF

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

        self.interval_label = QLabel('Interval:', self)
        self.interval_input = QLineEdit(self)
        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_input)

        self.references_label = QLabel('References File:', self)
        self.references_input = QLineEdit(self)
        self.references_button = QPushButton('Browse References File', self)
        self.references_button.clicked.connect(self.load_references)
        layout.addWidget(self.references_label)
        layout.addWidget(self.references_input)
        layout.addWidget(self.references_button)

        self.config_label = QLabel('Config File:', self)
        self.config_input = QLineEdit(self)
        self.config_button = QPushButton('Browse Config File', self)
        self.config_button.clicked.connect(self.load_config)
        layout.addWidget(self.config_label)
        layout.addWidget(self.config_input)
        layout.addWidget(self.config_button)

        self.start_button = QPushButton('Start Simulation', self)
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.prev_iteration)
        self.prev_button.setEnabled(False)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.next_iteration)
        self.next_button.setEnabled(False)
        layout.addWidget(self.next_button)

        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.resize(1200, 1200)

    def load_references(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load References File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            self.references_input.setText(file_name)

    def load_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Config File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            self.config_input.setText(file_name)
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
            interval = self.interval_input.text()
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
            
            if interval == 'N' or interval == "":
                interval = len(globals.references)
            else:
                interval = int(interval)

            dsm = DSM()
            dsm.simulate(interval)

            self.result_label.setText("Simulation completed successfully.")
            self.show_message("Success", "Simulation completed successfully.")

            self.current_iteration = 0
            self.update_scene()
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)

        except Exception as e:
            self.show_message("Error", str(e))

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def update_scene(self):
        self.scene.clear()
        page_items = []
        cpu_items = []
        left_space = 300
        pages_width = globals.total_pages * 50
        cpus_width = globals.num_cpus * 100 + (globals.num_cpus - 1) * 50
        buffer = (pages_width - cpus_width) / 2

        # Position pages horizontally
        for i in range(globals.total_pages):
            page_rect = self.scene.addRect(QRectF(left_space + 50 * i, 50, 50, 50), brush=Qt.yellow)
            page_id = i
            text_item = self.scene.addText(str(page_id))
            text_item.setPos(left_space + 50 * i + 15, 60)
            page_items.append(page_rect)
        
        # Center CPUs horizontally
        for i in range(globals.num_cpus):
            cpu_rect = self.scene.addRect(QRectF(left_space + buffer + 150 * i, 150, 100, 100), brush=Qt.green)
            cpu_text = self.scene.addText(f"CPU {i}")
            cpu_text.setPos(left_space + buffer + 150 * i + 35, 255)  # Position text below the CPU rectangle
            
            # Add the state of each CPU
            state = globals.saved_state[self.current_iteration][i + 1]
            state_text = self.scene.addText(", ".join(map(str, state)))
            state_text.setPos(left_space + buffer + 150 * i + 35, 190)
            
            cpu_items.append(cpu_rect)
        
        # Add Virtual Memory
        ram_item = self.scene.addRect(QRectF(left_space, 300, pages_width, 100), brush=Qt.cyan)
        ram_text = self.scene.addText("Virtual Memory")
        ram_text.setPos(left_space + pages_width / 2 - 50, 410)  # Position text below the Virtual Memory rectangle
        
        # Add the state of the Virtual Memory
        virtual_memory_state = globals.saved_state[self.current_iteration][0]
        vm_state_text = self.scene.addText(", ".join(map(str, virtual_memory_state)))
        vm_state_text.setPos(left_space + pages_width / 2 - 50, 330)
        
        # Add references text
        for index, ref in enumerate(globals.references):
            cpu_id, page_id, mode = ref
            ref_text = f"CPU {cpu_id} wants Page {page_id} with Mode {mode}"
            ref_text_item = self.scene.addText(ref_text)
            ref_text_item.setPos(50, 50 + index * 20)
            
            if index == self.current_iteration:
                ref_text_item.setDefaultTextColor(Qt.red)  # Highlight the current reference in red
            else:
                ref_text_item.setDefaultTextColor(Qt.black)  # Use black color for other references

    def prev_iteration(self):
        if self.current_iteration > 0:
            self.current_iteration -= 1
            self.update_scene()

    def next_iteration(self):
        if self.current_iteration < len(globals.saved_state) - 1:
            self.current_iteration += 1
            self.update_scene()

def main():
    app = QApplication(sys.argv)
    ex = DSMGui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
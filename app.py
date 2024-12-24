from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QComboBox, QPushButton, QLabel, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import sys

class DataPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Plotting Tool")
        self.setGeometry(100, 100, 1000, 700)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Dataset variables
        self.dataset = None
        
        # Load Dataset Button
        self.load_button = QPushButton("Load Dataset")
        self.load_button.clicked.connect(self.load_dataset)
        self.layout.addWidget(self.load_button)
        
        # Dropdowns for Field Selection
        self.field1_label = QLabel("Field 1:")
        self.layout.addWidget(self.field1_label)
        self.field1_dropdown = QComboBox()
        self.layout.addWidget(self.field1_dropdown)
        
        self.field2_label = QLabel("Field 2 (Optional):")
        self.layout.addWidget(self.field2_label)
        self.field2_dropdown = QComboBox()
        self.layout.addWidget(self.field2_dropdown)
        
        # Plot Type Selection
        self.plot_type_label = QLabel("Select Plot Type:")
        self.layout.addWidget(self.plot_type_label)
        self.plot_type_dropdown = QComboBox()
        self.plot_type_dropdown.addItems(["Histogram", "Scatter Plot", "Box Plot"])
        self.layout.addWidget(self.plot_type_dropdown)
        
        # Plot Button
        self.plot_button = QPushButton("Generate Plot")
        self.plot_button.clicked.connect(self.generate_plot)
        self.layout.addWidget(self.plot_button)
        
        # Matplotlib Canvas for Displaying Plots
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)
    
    def load_dataset(self):
        # Load dataset from file
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Open Dataset", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if file:
            if file.endswith('.csv'):
                self.dataset = pd.read_csv(file)
            elif file.endswith('.xlsx'):
                self.dataset = pd.read_excel(file)
            
            # Populate dropdowns with column names
            self.field1_dropdown.clear()
            self.field2_dropdown.clear()
            columns = self.dataset.columns
            self.field1_dropdown.addItems(columns)
            self.field2_dropdown.addItems(columns)
    
    def generate_plot(self):
        # Clear the canvas
        self.canvas.figure.clear()
        
        if self.dataset is None:
            return
        
        # Get selected fields and plot type
        field1 = self.field1_dropdown.currentText()
        field2 = self.field2_dropdown.currentText()
        plot_type = self.plot_type_dropdown.currentText()
        
        # Generate a plot based on selected type
        ax = self.canvas.figure.add_subplot(111)
        if plot_type == "Histogram" and field1:
            # Histogram for a single field
            ax.hist(self.dataset[field1], bins=20, alpha=0.7)
            ax.set_xlabel(field1)
            ax.set_title(f"Histogram: {field1}")
        elif plot_type == "Scatter Plot" and field1 and field2 and field1 != field2:
            # Scatter plot for two fields
            ax.scatter(self.dataset[field1], self.dataset[field2], alpha=0.7)
            ax.set_xlabel(field1)
            ax.set_ylabel(field2)
            ax.set_title(f"Scatter Plot: {field1} vs {field2}")
        elif plot_type == "Box Plot" and field1:
            # Box plot for a single field
            ax.boxplot(self.dataset[field1].dropna(), vert=False)
            ax.set_xlabel(field1)
            ax.set_title(f"Box Plot: {field1}")
        else:
            # Handle invalid selections
            ax.text(0.5, 0.5, "Invalid Selection", fontsize=15, ha='center')
        
        # Render the plot on the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DataPlotApp()
    main_window.show()
    sys.exit(app.exec_())

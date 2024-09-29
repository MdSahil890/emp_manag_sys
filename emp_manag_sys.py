import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore

# File to store employee data
filename = 'emp_manag_sys.json'

# Load employee data
try:
    with open(filename, 'r') as file:
        employee_data = json.load(file)
except FileNotFoundError:
    employee_data = []  # Start with an empty list if the file doesn't exist
except json.JSONDecodeError:
    employee_data = []  # Handle cases where the file is corrupt

class EmpManagSys:
    def __init__(self):
        self.employee_data = employee_data

    def add_employee(self, name, age, department, position, salary):
        employee_id = len(self.employee_data) + 1
        self.employee_data.append({
            "id": employee_id,
            "name": name,
            "age": age,
            "department": department,
            "position": position,
            "salary": salary
        })
        return True

    def view_employees(self):
        return self.employee_data

    def update_employee(self, employee_id, field, new_value):
        for emp in self.employee_data:
            if emp["id"] == employee_id:
                emp[field] = new_value
                return True
        return False

    def delete_employee(self, employee_id):
        self.employee_data = [emp for emp in self.employee_data if emp["id"] != employee_id]
        return True

    def exit_save(self):
        with open(filename, 'w') as file:
            json.dump(self.employee_data, file, indent=4)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QtGui.QIcon("path_to_your_logo.png"))
        
        # Overall dark mode styles
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF; font-family: Arial;")

        self.emp_sys = EmpManagSys()
        self.initUI()

    def initUI(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Title
        title = QtWidgets.QLabel("Employee Management System")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")  # Title color
        self.layout.addWidget(title)

        # Input Fields
        self.name_input = self.create_input_field("Name")
        self.age_input = self.create_spin_box("Age", 18, 65)
        self.department_input = self.create_input_field("Department")
        self.position_input = self.create_input_field("Position")
        self.salary_input = self.create_spin_box("Salary", 12000, 250000)

        # Buttons
        self.add_button = self.create_button("Add Employee", self.add_employee)
        self.view_button = self.create_button("View Employees", self.view_employees)
        self.update_button = self.create_button("Update Employee", self.update_employee)
        self.delete_button = self.create_button("Delete Employee", self.delete_employee)
        self.quit_button = self.create_button("Exit & Save", self.exit_save)

        # Button Layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.quit_button)

        # Add Widgets to Layout
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.department_input)
        self.layout.addWidget(self.position_input)
        self.layout.addWidget(self.salary_input)
        self.layout.addLayout(button_layout)

        # Table Widget for Employee Data
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "Age", "Department", "Position", "Salary"])
        
        # Set the background and text color for the table
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #2E2E2E; 
                color: #FFFFFF;
                border: 1px solid #444;
            }
            QTableWidget::item {
                background-color: #2E2E2E; 
                color: #FFFFFF;  /* Text color */
            }
            QHeaderView::section {
                background-color: #3E3E3E; 
                color: #FFFFFF;  /* Header text color */
                padding: 4px;
                border: 1px solid #444;
            }
        """)
        
        self.layout.addWidget(self.table_widget)

    def create_input_field(self, placeholder):
        input_field = QtWidgets.QLineEdit(self)
        input_field.setPlaceholderText(f"Enter employee's {placeholder.lower()}")
        input_field.setStyleSheet("padding: 10px; background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #444;")
        return input_field

    def create_spin_box(self, placeholder, min_value, max_value):
        spin_box = QtWidgets.QSpinBox(self)
        spin_box.setRange(min_value, max_value)
        spin_box.setStyleSheet("padding: 10px; background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #444;")
        return spin_box

    def create_button(self, text, handler):
        button = QtWidgets.QPushButton(text, self)
        button.setStyleSheet("padding: 5px; background-color: #007ACC; color: #FFFFFF; border: none; border-radius: 5px;")
        button.clicked.connect(handler)
        return button

    def add_employee(self):
        name = self.name_input.text().capitalize()
        age = self.age_input.value()
        department = self.department_input.text().upper()
        position = self.position_input.text().upper()
        salary = self.salary_input.value()

        if self.emp_sys.add_employee(name, age, department, position, salary):
            QtWidgets.QMessageBox.information(self, "Success", "Employee added successfully!")
            self.clear_inputs()
            self.refresh_employee_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to add employee.")

    def view_employees(self):
        self.refresh_employee_table()

    def refresh_employee_table(self):
        employees = self.emp_sys.view_employees()
        self.table_widget.setRowCount(len(employees))

        for row, emp in enumerate(employees):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(emp['id'])))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(emp['name']))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(emp['age'])))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(emp['department']))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(emp['position']))
            self.table_widget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(emp['salary'])))

    def update_employee(self):
        employee_id, ok = QtWidgets.QInputDialog.getInt(self, "Update Employee", "Enter Employee ID to update:")
        if ok:
            field, ok = QtWidgets.QInputDialog.getItem(self, "Update Field", "Select field to update:", ["name", "age", "department", "position", "salary"])
            if ok:
                new_value, ok = QtWidgets.QInputDialog.getText(self, "New Value", f"Enter new value for {field}:")
                if field in ["age", "salary"]:
                    new_value = int(new_value) if field == "age" else float(new_value)
                if self.emp_sys.update_employee(employee_id, field, new_value):
                    QtWidgets.QMessageBox.information(self, "Success", "Employee updated successfully!")
                    self.refresh_employee_table()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Employee not found.")

    def delete_employee(self):
        employee_id, ok = QtWidgets.QInputDialog.getInt(self, "Delete Employee", "Enter Employee ID to delete:")
        if ok:
            if self.emp_sys.delete_employee(employee_id):
                QtWidgets.QMessageBox.information(self, "Success", f"Employee with ID {employee_id} deleted successfully!")
                self.refresh_employee_table()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Employee not found.")

    def exit_save(self):
        self.emp_sys.exit_save()
        QtWidgets.QMessageBox.information(self, "Success", "Employee data saved successfully!")
        self.close()

    def clear_inputs(self):
        self.name_input.clear()
        self.age_input.setValue(18)
        self.department_input.clear()
        self.position_input.clear()
        self.salary_input.setValue(12000)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

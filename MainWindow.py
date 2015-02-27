import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QSpinBox, QGridLayout, QHBoxLayout,
                             QApplication, QPushButton)
import sympy as sp
import math

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Used for computing the results
        self.function = None
        self.symbols = []
        self.num_var = 1

        # Get the number of variables
        self.var_label = QLabel('# of vars:')
        # Maximum number of variables for our function. Could be changed
        self.max_var = 10

        self.var_spin = QSpinBox()
        self.var_spin.setMinimum(1)
        self.var_spin.setMaximum(self.max_var)
        self.var_spin.valueChanged[int].connect(self.var_num_changed)

        head_layout = QHBoxLayout()
        head_layout.addWidget(self.var_label)
        head_layout.addWidget(self.var_spin)

        # Main Layout
        self.grid = QGridLayout()

        self.grid.addLayout(head_layout, 0, 0)
        self.grid.addWidget(QLabel("name:"), 0, 1)
        self.grid.addWidget(QLabel("value:"), 0, 2)
        self.grid.addWidget(QLabel("error:"), 0, 3)

        # Layout for defining variables and function
        self.var_labels = []
        self.var_names = []
        self.var_values = []
        self.var_errors = []
        for i in range(self.max_var):
            label = QLabel("var{}".format(i))
            var_name = QLineEdit()
            var_value = QLineEdit()
            var_error = QLineEdit()

            # Add one to the index because at 0 there's already a widget
            self.grid.addWidget(label, i+1, 0)
            self.grid.addWidget(var_name, i+1, 1)
            self.grid.addWidget(var_value, i+1, 2)
            self.grid.addWidget(var_error, i+1, 3)

            self.var_labels.append(label)
            self.var_names.append(var_name)
            self.var_values.append(var_value)
            self.var_errors.append(var_error)

            label.hide()
            var_name.hide()
            var_value.hide()
            var_error.hide()

        self.var_num_changed(self.num_var)

        # Add function widgets
        self.grid.addWidget(QLabel("function"), self.max_var+1, 0)
        self.func_edit = QLineEdit()
        self.grid.addWidget(self.func_edit, self.max_var+1, 1)

        self.cmp_btn = QPushButton("Compute")
        self.grid.addWidget(self.cmp_btn, self.max_var+2, 1)

        self.cmp_btn.clicked.connect(self.compute)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('sigma')
        self.show()

    def var_num_changed(self, num):
        self.num_var = num
        for i in range(self.max_var):
            self.var_names[i].hide()
            self.var_labels[i].hide()
            self.var_values[i].hide()
            self.var_errors[i].hide()

        for i in range(num):
            self.var_names[i].show()
            self.var_labels[i].show()
            self.var_values[i].show()
            self.var_errors[i].show()

    def compute(self):
        # Get user function and delete old symbols
        input_str = self.func_edit.displayText()
        self.function = sp.S(input_str)
        self.symbols = []

        # Read all displayed vars into symbols
        for i in range(self.num_var):
            symbol = sp.Symbol(self.var_names[i].displayText())
            self.symbols.append(symbol)

        # Derive func after every var and print
        for var in self.symbols:
            print("df/d{} = {}".format(var, sp.diff(self.function, var)))

        # Get values as dict
        vals = {}
        for i in range(self.num_var):
            vals[self.symbols[i]] = float(self.var_values[i].displayText())

        # Get errors as num list
        errors = []
        for i in range(self.num_var):
            errors.append(float(self.var_errors[i].displayText()))

        # Get every derivative
        derivs = []
        for i in range(self.num_var):
            derivs.append(sp.diff(self.function, self.symbols[i]))

        error_sq = 0.0
        for i in range(self.num_var):
            temp = derivs[i].evalf(subs=vals)
            temp *= errors[i]
            temp *= temp
            error_sq += temp

        print("Result: {} +- {}".format(float(self.function.evalf(subs=vals)),
                                        float(math.sqrt(error_sq))))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

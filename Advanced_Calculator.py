import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, integrate, solve, simplify
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy_financial as npf

class AdvancedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Calculator")
        self.geometry("600x800")
        self.create_widgets()

    def create_widgets(self):
        # Display and buttons layout here
        self.display = tk.Entry(self, font=("Arial", 20), borderwidth=5, relief=tk.SUNKEN)
        self.display.grid(row=0, column=0, columnspan=5)

        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'DEL',
            '1', '2', '3', '-', 'x^2',
            '0', '.', '=', '+', 'sqrt'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            tk.Button(self, text=button, width=5, height=2, font=("Arial", 18),
                      command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # Advanced functionalities (Math, Trig, Graph, etc.)
        tk.Button(self, text='Graph', width=20, height=2, font=("Arial", 18),
                  command=self.plot_graph).grid(row=row_val, column=0, columnspan=2)
        tk.Button(self, text='Math', width=20, height=2, font=("Arial", 18),
                  command=self.math_functions).grid(row=row_val, column=2, columnspan=2)

    def on_button_click(self, button):
        if button == 'C':
            self.display.delete(0, tk.END)
        elif button == 'DEL':
            current_text = self.display.get()
            self.display.delete(len(current_text)-1, tk.END)
        elif button == '=':
            expression = self.display.get()
            try:
                result = eval(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif button == 'x^2':
            current_text = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current_text + '**2')
        elif button == 'sqrt':
            current_text = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, 'sqrt(' + current_text + ')')
        else:
            self.display.insert(tk.END, button)

    def plot_graph(self):
        window = tk.Toplevel(self)
        window.title("Graphing")
        window.geometry("500x500")

        figure = plt.Figure(figsize=(5, 5), dpi=100)
        ax = figure.add_subplot(111)

        x = np.linspace(-10, 10, 400)
        y = np.sin(x)  # Example plot, you can extend to other functions

        ax.plot(x, y)
        ax.set_title('Graph')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        canvas = FigureCanvasTkAgg(figure, window)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def math_functions(self):
        window = tk.Toplevel(self)
        window.title("Math Functions")
        window.geometry("400x400")

        functions = [
            'Fraction', 'Decimal', 'Factor', 'Expand', 'Simplify', 
            'Differentiate', 'Integrate', 'Solve', 'PV', 'FV'
        ]

        for function in functions:
            tk.Button(window, text=function, width=20, height=2, font=("Arial", 18),
                      command=lambda f=function: self.handle_math_function(f)).pack()

    def handle_math_function(self, function):
        if function == 'Fraction':
            expression = self.display.get()
            try:
                result = simplify(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif function == 'Decimal':
            expression = self.display.get()
            try:
                result = float(eval(expression))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif function == 'Differentiate':
            expression = self.display.get()
            try:
                x = symbols('x')
                result = diff(parse_expr(expression), x)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif function == 'Integrate':
            expression = self.display.get()
            try:
                x = symbols('x')
                result = integrate(parse_expr(expression), x)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif function == 'Solve':
            expression = self.display.get()
            try:
                x = symbols('x')
                result = solve(parse_expr(expression), x)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif function == 'PV':
            rate = float(input("Enter the interest rate (as a decimal): "))
            nper = int(input("Enter the number of periods: "))
            pmt = float(input("Enter the payment made each period: "))
            fv = float(input("Enter the future value: "))
            pv = npf.pv(rate, nper, pmt, fv)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(pv))
        elif function == 'FV':
            rate = float(input("Enter the interest rate (as a decimal): "))
            nper = int(input("Enter the number of periods: "))
            pmt = float(input("Enter the payment made each period: "))
            pv = float(input("Enter the present value: "))
            fv = npf.fv(rate, nper, pmt, pv)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(fv))

if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()

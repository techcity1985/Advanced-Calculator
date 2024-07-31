from flask import Flask, render_template, request
import os
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import numpy_financial as npf
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    function = request.form['function']
    x = np.linspace(-10, 10, 400)
    y = eval(function)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Graph')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    return render_template('index.html', graph=graph)

@app.route('/calculate_pv', methods=['POST'])
def calculate_pv():
    rate = float(request.form['rate'])
    nper = int(request.form['nper'])
    pmt = float(request.form['pmt'])
    fv = float(request.form['fv'])
    pv = npf.pv(rate, nper, pmt, fv)
    return render_template('index.html', result=f'The present value is: {pv}')

@app.route('/calculate_fv', methods=['POST'])
def calculate_fv():
    rate = float(request.form['rate'])
    nper = int(request.form['nper'])
    pmt = float(request.form['pmt'])
    pv = float(request.form['pv'])
    fv = npf.fv(rate, nper, pmt, pv)
    return render_template('index.html', result=f'The future value is: {fv}')

@app.route('/solve', methods=['POST'])
def solve():
    equations = request.form['equations'].split(';')
    variables = request.form['variables'].split(',')
    variables = [sp.symbols(var.strip()) for var in variables]
    eqs = [sp.sympify(eq) for eq in equations]
    solutions = sp.linsolve(eqs, variables)
    return render_template('index.html', result=f'The solutions are: {solutions}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

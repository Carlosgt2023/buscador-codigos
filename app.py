from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def buscar_codigo(codigo):
    with open('data.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Primera columna es el código
            if row[0].strip() == codigo.strip():
                return row[1:5]  # Devuelve las 4 columnas siguientes
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    codigo_ingresado = None
    if request.method == 'POST':
        codigo_ingresado = request.form.get('codigo')
        resultado = buscar_codigo(codigo_ingresado)
    return render_template('index.html', resultado=resultado, codigo=codigo_ingresado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

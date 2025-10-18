from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', resultado=None, codigo=None, error=None)

@app.route('/buscar', methods=['POST'])
def buscar():
    resultado = None
    codigo_buscado = None
    error_message = None

    codigo_buscado = request.form['codigo'].strip().upper()

    # Intenta con diferentes nombres de archivo
    archivos_posibles = ['datos.txt', 'data.txt', 'datos.csv']
    archivo = None
    
    for nombre in archivos_posibles:
        if os.path.exists(nombre):
            archivo = nombre
            print(f"Archivo encontrado: {nombre}")
            break
    
    if archivo is None:
        error_message = f"ERROR: No se encontró ningún archivo de datos. Archivos buscados: {archivos_posibles}"
        print(error_message)
        print(f"Archivos en el directorio actual: {os.listdir('.')}")
        return render_template('index.html', resultado=None, codigo=codigo_buscado, error=error_message)

    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                # Detecta automáticamente el delimitador
                if ';' in linea:
                    delimitador = ';'
                elif '|' in linea:
                    delimitador = '|'
                else:
                    delimitador = ','
                
                # Divide por el delimitador correcto
                partes = linea.strip().split(delimitador)
                
                # Limpia espacios
                partes = [p.strip() for p in partes]
                
                print(f"DEBUG - Comparando: '{partes[0]}' con '{codigo_buscado}'")
                
                if partes[0].upper() == codigo_buscado:
                    resultado = partes[1:5] if len(partes) > 1 else []
                    print(f"¡Encontrado! Resultado: {resultado}")
                    break
                    
    except Exception as e:
        error_message = f"ERROR al leer archivo: {e}"
        print(error_message)

    return render_template('index.html', resultado=resultado, codigo=codigo_buscado, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
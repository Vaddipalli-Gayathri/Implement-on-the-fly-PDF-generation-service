
# Apartado donde se importaran todos los modulos necesarios para el funcionamiento del proyecto.
from flask import Flask, render_template, Response, request
from tempfile import TemporaryFile
import io
from xhtml2pdf import pisa

# Variable que guarda el nombre del archivo de arranque para la ejecución del código. 
app = Flask(__name__)

# Ruta principal donde se encuentra el formulario para la generación de pdf.
@app.route('/')
# Función que retorna la vista del archivo html con el maquetado principal
# del proyecto "Index principal".
def home():
    return render_template("index.html")

# Función para verificar si la extensión del archivo es compatible.
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen "PERMITIDOS".
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Obtener la extensión del archivo que se desea evaluar si se encuentra entre los parametros.
    # Esto funciona al definir una variable de llamada estension, la cual obtendra como valor el str
    # que se obtiene al separar el nombre del archivo por el separador de ".", y desplazando el valor
    # de la cadena creada al final, donde se encontrara la extensión, osea se obtiene la cadena de texto
    # despues del punto ".".
    extension = filename.rsplit('.', 1)[1].lower()

    # Verificar si la extensión está permitida.
    if '.' in filename and extension in extensiones_permitidas:
        # Retornar verdadero si el resultado es positivo.
        return True
    else:
        # Reetornar falso si el resultado es negativo.
        return False

import os

# Ruta base para archivos relativos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ruta principal para la construcción del pdf.
@app.route('/generar_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        # Captura los datos del formulario
        raza = request.form['raza']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['archivo']

        # Condicional donde utilizaremos la funcion de extensiones_validas, para evaluar si el archivo esta permitido o no.
        if(request.files['archivo'] and extensiones_validas(imagen.filename)):
            # Crea un archivo temporal para guardar la imagen
            from tempfile import NamedTemporaryFile
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(imagen.filename)[1]) as tmp_file:
                imagen.save(tmp_file)
                ruta_temporal = tmp_file.name
        else:
            # En caso de no tener un archivo permitido se retornara el mensaje de error.
            return "archivo invalido"         
           
        # Renderiza la plantilla HTML y reemplaza los marcadores de posición con datos
        rendered_template = render_template('example.html', raza=raza, nombre_hermano=nombre, descripcion=descripcion, imagen=ruta_temporal)
        
        # Combina el contenido HTML y los estilos CSS
        css_path = os.path.join(BASE_DIR, 'static', 'css', 'style.css')
        with open(css_path, 'r') as css_file:
            css_content = css_file.read()
        html_content = f"{rendered_template}\n<style>{css_content}</style>"
        
        # Crea un objeto de tipo BytesIO para almacenar el PDF generado
        pdf_buffer = io.BytesIO()
        
        # Genera el PDF a partir del contenido HTML con estilos CSS
        pisa.CreatePDF(src=html_content, dest=pdf_buffer)
        
        # Mueve el puntero al inicio del objeto BytesIO
        pdf_buffer.seek(0)
        
        # Crea un objeto Response para enviar el PDF al navegador
        response = Response(pdf_buffer.read(), content_type='application/pdf')
        
        # Agrega el encabezado para la descarga del PDF
        response.headers['Content-Disposition'] = 'inline; filename=mi_pdf.pdf'
        
        # Ruta completa de guardado (puedes cambiarla según tus necesidades)
        ruta_de_guardado = os.path.join(BASE_DIR, 'static', 'pdf', 'pdfgenerado.pdf')

        # Guarda el archivo PDF con el nombre generado automáticamente
        with open(ruta_de_guardado, 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())
        
        # Retorna la petición http, entregando el resultado, osea la visualización del pdf construido.  
        return response
    else:
        # Si no se envió el formulario, muestra un mensaje
        mensaje = "No se encontraron datos, por lo que no es posible generar el PDF correctamente."
        return mensaje


# Condicional encargada de arrancar o inicializar el proyecto.
if __name__ == '__main__':
    app.run(debug=True,  port=5030)
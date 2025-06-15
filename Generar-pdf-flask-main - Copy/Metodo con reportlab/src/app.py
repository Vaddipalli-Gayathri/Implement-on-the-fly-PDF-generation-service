from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    # Get form data
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    company = request.form.get('company', '')
    start_date = request.form.get('start_date', '')
    salary = request.form.get('salary', '')
    location = request.form.get('location', '')
    hr_name = request.form.get('hr_name', '')
    date_of_letter = request.form.get('date_of_letter')
    if not date_of_letter:
        date_of_letter = datetime.today().strftime('%Y-%m-%d')

    # Create PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Draw border line on the right side with some margin
    margin = 40
    c.setLineWidth(1)
    c.line(width - margin, margin, width - margin, height - margin)

    # Title
    c.setFont('Times-Bold', 20)
    c.drawString(50, height - 50, "Offer Letter")

    # Date
    c.setFont('Times-Roman', 12)
    c.drawString(50, height - 80, f"Date: {date_of_letter}")

    # Body text
    text = c.beginText(50, height - 120)
    text.setFont('Times-Roman', 12)
    text.setLeading(18)  # 1.5 line spacing (12 * 1.5)
    lines = [
        "[Company Letterhead or Logo]",
        "",
        f"Date: {date_of_letter}",
        "",
        f"To,",
        f"{nombre}",
        # Optional address line can be added here if needed
        "",
        f"Subject: Offer of Employment for the position of ",
        f"{descripcion.upper()}",
        "",
        f"Dear {nombre},",
        "",
        f"We are delighted to extend to you an offer for the position of ",
        f"{descripcion.upper()}",
        f" at {company}. After careful consideration of your skills and experience, we are confident that you will make a significant contribution to our team.",
        "",
        f"Your employment is expected to commence on ",
        f"{start_date}",
        f". You will be based at our office located in ",
        f"{location}. Your total annual compensation will be ",
        f"{salary}",
        f", subject to applicable deductions as per company policy and relevant laws.",
        "",
        "Your detailed responsibilities and terms of employment will be outlined in the formal contract, which will be provided upon your joining. We trust you will uphold the company’s standards and values throughout your tenure.",
        "",
        "Kindly confirm your acceptance of this offer by signing and returning a copy of this letter at your earliest convenience.",
        "",
        "We eagerly look forward to welcoming you aboard and working together towards mutual success.",
        "",
        f"Sincerely,",
        f"{hr_name}",
        "HR Manager",
        f"{company}",
        "",
        "(Signature)"
    ]
    for line in lines:
        text.textLine(line)
    c.drawText(text)

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='offer_letter.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True, port=3000)

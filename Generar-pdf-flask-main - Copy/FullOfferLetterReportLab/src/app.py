from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-offer', methods=['POST'])
def generate_offer():
    # Get form data
    name = request.form['name']
    position = request.form['position']
    company = request.form['company']
    start_date = request.form['start_date']
    salary = request.form['salary']
    location = request.form['location']
    hr_name = request.form['hr_name']
    date_of_letter = request.form.get('date_of_letter')
    if not date_of_letter:
        date_of_letter = datetime.today().strftime('%Y-%m-%d')

    # Create PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont('Helvetica-Bold', 20)
    c.drawString(50, height - 50, "Offer Letter")

    # Date
    c.setFont('Helvetica', 12)
    c.drawString(50, height - 80, f"Date: {date_of_letter}")

    # Body text
    text = c.beginText(50, height - 120)
    text.setFont('Helvetica', 12)
    lines = [
        f"Dear {name},",
        "",
        f"We are pleased to offer you the position of {position} at {company}.",
        f"Your start date will be {start_date}, and you will be based in our {location} office.",
        "",
        f"You will be paid a salary of {salary}. Further details of your employment will be provided in your contract.",
        "",
        "We look forward to having you on our team.",
        "",
        f"Sincerely,",
        f"{hr_name}",
        "HR Manager",
        f"{company}"
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

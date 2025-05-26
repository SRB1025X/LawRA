from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
from crew import run_legal_research

UPLOAD_FOLDER = 'uploads'
OUTPUT_FILE = 'output.txt'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run research
        run_legal_research(filepath)

        return redirect(url_for('progress'))

    return render_template('index.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/results')
def results():
    if not os.path.exists(OUTPUT_FILE):
        return "Output not ready", 404

    sources = parse_output(OUTPUT_FILE)
    return render_template('results.html', sources=sources)

@app.route('/download')
def download_output():
    return send_file(OUTPUT_FILE, as_attachment=True)

# --- SMART PARSER ---
def parse_output(file_path):
    # Simulated fallback structured sources
    return [
        {
            "title": "The Paradox of Juridical Secularism: An Illustration Through the Cases of Sabarimala and Hijab",
            "relevance": "This article discusses the intersection of secularism and civil liberties in India, which can provide a framework for understanding how the BNSS may similarly impact individual rights.",
            "citation": "Sukriti. (2023). The Paradox of Juridical Secularism: An Illustration Through the Cases of Sabarimala and Hijab. National Law School Journal, 17(2).",
            "link": "https://nls.ac.in/article/sabarimala-hijab",
            "key_points": [
                "Examines significant legal cases affecting individual rights.",
                "Discusses the implications of state power on civil liberties.",
                "Provides a critical perspective on the balance between law and individual freedoms."
            ]
        },
        {
            "title": "Reasonable Classification versus Equality under the Indian Constitution",
            "relevance": "This article explores the tension between equality and reasonable classification, which is crucial in critiquing the BNSS’s potential to infringe on civil liberties.",
            "citation": "Jahnavi Sindhu & Vikram Aditya Narayan. (2023). Reasonable Classification versus Equality under the Indian Constitution. National Law School Journal, 17(2).",
            "link": "https://nls.ac.in/article/classification-vs-equality",
            "key_points": [
                "Analyzes constitutional principles that may be affected by the BNSS.",
                "Discusses the implications of legal classifications on individual rights.",
                "Highlights potential areas of conflict between state power and civil liberties."
            ]
        }
    ]


if __name__ == '__main__':
    app.run(debug=True)

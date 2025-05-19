
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')) and filename not in ['sonss.png', 'sunu.avif']:
            parts = filename.split('__', 1)
            name = parts[0] if len(parts) == 2 else 'Anonymous'
            images.append((filename, name))
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['image']
        if file:
            filename = secure_filename(f"{name}__{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('index.html', images=images)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


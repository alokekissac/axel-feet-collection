from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Render your index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Proxy to fetch images from axelsbirthday.xyz
@app.route('/proxy/images')
def proxy_images():
    try:
        response = requests.get("https://axelsbirthday.xyz/api/images", verify=False)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch images'}), 500

# Optional: Proxy for uploading too (to keep your API key/server secure if needed)
@app.route('/proxy/upload', methods=['POST'])
def proxy_upload():
    try:
        files = {'image': request.files['image']}
        data = {'name': request.form['name']}
        res = requests.post("https://axelsbirthday.xyz/api/upload-image", files=files, data=data, verify=False)
        res.raise_for_status()
        return redirect(url_for('index'))
    except requests.RequestException:
        return "Upload failed", 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Home route renders the main HTML page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Proxy route to fetch images from the external API
@app.route('/proxy/images')
def proxy_images():
    try:
        response = requests.get("https://axelsbirthday.xyz/api/images", verify=False)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        print("Image fetch error:", e)
        return jsonify({'error': 'Failed to fetch images'}), 500

# Proxy route to upload an image to the external API
@app.route('/proxy/upload', methods=['POST'])
def proxy_upload():
    try:
        print("Upload request received")

        # Retrieve the uploaded image and name
        image = request.files['image']
        name = request.form['name']

        print(f"Uploading: {name}, File: {image.filename}, Type: {image.content_type}")

        # Set correct content type so multer (on external API) recognizes it as an image
        files = {
            'image': (image.filename, image.stream, image.content_type)
        }
        data = {'name': name}

        # Send the request to the external API
        res = requests.post(
            "https://axelsbirthday.xyz/api/upload-image",
            files=files,
            data=data,
            verify=False
        )
        res.raise_for_status()

        print("Upload to external API succeeded")
        return jsonify({'message': 'Upload successful'}), 200

    except requests.RequestException as e:
        if e.response is not None:
            print("Upload error (response):", e.response.text)
        else:
            print("Upload error (exception):", str(e))
        return jsonify({'error': 'Upload failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)

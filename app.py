from flask import Flask, request, render_template
import requests
import base64

app = Flask(__name__)

# Replace this with your Hugging Face API key
API_KEY = "your_huggingface_api_key"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

def generate_image(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"inputs": prompt}
    
    # Send the request to Hugging Face API
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        # Decode the base64 image data
        image_data = base64.b64encode(response.content).decode("utf-8")
        return f"data:image/png;base64,{image_data}"
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form["prompt"]
        image_url = generate_image(prompt)
        return render_template("index.html", image_url=image_url, prompt=prompt)
    return render_template("index.html", image_url=None)

if __name__ == "__main__":
    app.run(debug=True)

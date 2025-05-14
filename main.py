from flask import Flask, request, jsonify
from verify_data import create_output

# Grunden til at jeg benytter Flask, er for at jeg nemt kan sende og ændre på data.
# Alternativt kunne jeg bare have lagt filen ind i projektet, men på denne måde
# kan I nemmere ændre på dataene og tilføje flere data, uden at skulle droppe filer ind i
# projektet.

app = Flask(__name__)

@app.route("/")
def main_page():
    return "Velkommen til TopRefusion!"

@app.route("/process_json", methods=["POST"])
def process_json():
    try:
        input_data = request.get_json()

        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        result = create_output(input_data)
        return result
    except Exception as e:
        return jsonify({"error": str(e)}), 500
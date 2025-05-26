from flask import Flask, request, jsonify
from verify_data import create_output
from flasgger import Swagger, swag_from

"""
Grunden til at jeg benytter Flask, er for at jeg nemt kan sende og ændre på data.
Alternativt kunne jeg bare have lagt filen ind i projektet, men på denne måde
kan I nemmere ændre på dataene og tilføje flere data, uden at skulle droppe filer ind i
projektet.
Jeg har valgt at bruge Flasgger til at dokumentere API'et, så det er nemt at se, hvilke
data der skal sendes ind, og hvad der kommer ud, samt gøre det nemmere at teste API'et.
"""

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def main_page():
    """
    Velkommen til TopRefusion!
    ---
    responses:
      200:
        description: Welcome message
    """
    return "Velkommen til TopRefusion!"

@app.route("/process_json", methods=["POST"])
@swag_from({
    'tags': ['Process JSON'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'medarbejder_id': {'type': 'string'},
                        'beloeb': {'type': 'integer'},
                        'valuta': {'type': 'string'},
                        'kategori': {'type': 'string'},
                        'dato_udgift': {'type': 'string', 'format': 'date'}
                    },
                    'required': ['id', 'medarbejder_id', 'beloeb', 'valuta', 'kategori', 'dato_udgift']
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Resultatet af behandlingen af JSON-data',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'status': {'type': 'string'},
                        'begrundelse': {'type': 'string'}
                    }
                }
            }
        },
        400: {'description': 'No input data provided'},
        500: {'description': 'Internal server error'}
    }
})
def process_json():
    try:
        input_data = request.get_json()

        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        result = create_output(input_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
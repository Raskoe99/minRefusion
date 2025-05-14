from datetime import datetime, timedelta

def create_output(input=None):
    """
    Verify the input data received, from the application.
    
    Parameters:
    - input: The input data to be verified. Default is None.
    
    Returns:
    - dict: A dictionary with an id, status, and "begrundelse" for response.
    """
    
    response = []

    for item in input:
        verified_item = verify_input(item)
        response.append(verified_item)
        
    return response


def verify_input(item):
    response_object = {"id": item["id"], "status": "godkendt", "begrundelse": ""}

    beloeb = int(item["beloeb"])
    if beloeb <= 0:
        response_object["status"] = "afvist"
        response_object["begrundelse"] = ("Beløb er mindre end eller lig 0.")
        return response_object


    if (item["kategori"] == "Repraesentation" and beloeb > 1000):
        response_object["status"] = "afvist"
        response_object["begrundelse"] = ("Hvis kategorien er repræsentation, " \
        "så må beløbet ikke være større end 1.000 kr.")
        return response_object
    
    if (item["kategori"] == "Kontorartikler" and beloeb > 300):
        response_object["status"] = "afvist"
        response_object["begrundelse"] = ("Hvis kategorien er kontorartikler, " \
        "så må beløbet ikke være større end 300 kr.")
        return response_object

    message = is_older_than_90_days(item["dato_udgift"])
    if message:
        response_object["status"] = "afvist"
        response_object["begrundelse"] = (message)
        return response_object
    
    required_fields = ["id", "medarbejder_id","beloeb", "valuta", "kategori", "dato_udgift"]
    for field in required_fields:
        if not item.get(field):
            response_object["status"] = "afvist"
            response_object["begrundelse"] = (f"{field} mangler.")

    return response_object


def is_older_than_90_days(date_str):
    try: 
        input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.today().date()
        ninety_days_ago = today - timedelta(days=90)

        if input_date < ninety_days_ago:
            return "Dato for udgift er mere end 90 dage gammel."
        else:
            return None
    except ValueError:
        return "Dato format er forkert eller manglende. Forventet format: YYYY-MM-DD."

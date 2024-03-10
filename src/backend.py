import logging
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load your trained scikit-learn model
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    app.logger.warning("test!!!")
    try:
        # Get data from the request
        data = request.get_json()

        # Extract features from the data
        features = [data["age"],
                        data["sex"],
                        data["arrems"],
                        data["tempf"],
                        data["pulse"],
                        data["respr"],
                        data["bpsys"],
                        data["bpdias"],
                        data["popct"],
                        data["cebvd"],
                        data["eddial"],
                        data["chf"],
                        data["alzhd"],
                        data["diabetes"],
                        data["cad"],
                        data["edhiv"],
                        data["nochron"],
                    ]

        # Make a prediction
        prediction = model.predict([features])

        preds = ["Patient at risk of death", "Patient not at risk"]

        return jsonify({'prediction': preds[0]})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=3000)

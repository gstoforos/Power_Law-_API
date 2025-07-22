# app.py
from flask import Flask, request, jsonify
from model_powerlaw import fit_power_law

app = Flask(__name__)

@app.route('/fit', methods=['POST'])
def fit():
    try:
        data = request.get_json()
        shear_rates = data['shear_rates']
        shear_stresses = data['shear_stresses']
        flow_rate = float(data.get('flow_rate', 1))
        diameter = float(data.get('diameter', 1))
        density = float(data.get('density', 1))

        if not (shear_rates and shear_stresses):
            return jsonify({"error": "Missing shear data"}), 400

        result = fit_power_law(shear_rates, shear_stresses, flow_rate, diameter, density)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



import os
from flask import Flask, request, Response
from src.insurance_cross_sell import InsuranceCrossSell

# Initialize API and load the model (for better performance)
app = Flask(__name__)
pipeline = InsuranceCrossSell()
#pipeline = InsuranceCrossSell(pipeline_path=pipeline_path)

@app.route('/insurance_cross_sell/predict', methods=['POST'])
def insurance_cross_sell_predict():
    payload = request.get_json()

    # Convert JSON payload to DataFrame
    df_original = pipeline.create_dataframe(payload)

    # TESTE PARA DEBUG
    print(">>> Columns recebidas:", list(df_original.columns))
    
    # Predict probabilities
    proba = pipeline.predict_proba(df_original)

    # Rank and return JSON
    output = pipeline.sort_by_rank(df_original, proba)
    return Response(output, mimetype='application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run('0.0.0.0', port=port, debug=False)
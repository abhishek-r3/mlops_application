from flask import Flask, request, render_template
import json
import joblib
import os
import urllib.request
import ssl

presistecy_flag_mapper = {
    0 : "DRUG IS NON-PERSISTENT",
    1 : "DRUG IS PERSITENT"
}

def rearrage_features_for_pred(data):
    prediction_input = []
    input_feat = ['gender', 'age_bucket', 'dexa_freq_during_rx', 'dexa_during_rx',
       'comorb_encounter_for_screening_for_malignant_neoplasms',
       'comorb_long_term_current_drug_therapy',
       'comorb_encounter_for_immunization',
       'comorb_encntr_for_general_exam_w_o_complaint',
       'comorb_other_joint_disorder_not_elsewhere_classified',
       'concom_cephalosporins', 'comorb_dorsalgia',
       'comorb_gastro_esophageal_reflux_disease',
       'comorb_other_disorders_of_bone_density_and_structure',
       'concom_viral_vaccines', 'concom_macrolides_and_similar_types']
    for feat in input_feat:
        prediction_input.append(int(data[feat]))
    return {'data' : [prediction_input]}


def encode_features(transform_data):

    nominal_columns = ['gender', 'dexa_during_rx',
                        'comorb_encounter_for_screening_for_malignant_neoplasms', 'comorb_long_term_current_drug_therapy',
                        'comorb_encounter_for_immunization', 'comorb_encntr_for_general_exam_w_o_complaint',
                        'comorb_other_joint_disorder_not_elsewhere_classified',
                        'concom_cephalosporins', 'comorb_dorsalgia', 'comorb_gastro_esophageal_reflux_disease',
                        'comorb_other_disorders_of_bone_density_and_structure',
                        'concom_viral_vaccines', 'concom_macrolides_and_similar_types']
    ordinal_columns = ['age_bucket']
    numerical_feat = ['dexa_freq_during_rx']

    for feat in numerical_feat:
        transform_data[feat] = int(transform_data[feat])

    encode_res = {}
    le = joblib.load("encoders/label_encoder.pkl")
    encode_res['age_bucket'] = le.transform([transform_data['age_bucket']])[0]

    print(encode_res['age_bucket'], "LE RESULT")


    ohe_data = {}
    remaining_features = {}
    for key, value in transform_data.items():
        if key in nominal_columns:
            ohe_data[key] = value
        elif key not in ordinal_columns:
            print(key, "not in data")
            remaining_features[key] = value


    ohe = joblib.load("encoders/ohe_encoder.pkl")
    print("HERE IS THE SELECTED DATA")
    print(list(ohe_data.values()))
    ohe_res = list(ohe.transform([list(ohe_data.values())]).toarray().astype('int')[0])
    print(ohe_res)
    ohe_result = dict(zip(list(ohe_data.keys()), ohe_res))
    print(ohe_result)
    encode_res.update(ohe_result)
    encode_res.update(remaining_features)
    print(encode_res)
    return encode_res

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context   

def end_point_predictions(end_point, data):
    """
    """
    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

    body = str.encode(json.dumps(data))
    url = end_point
    api_key = '' # Replace this with the API key for the web service

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
        return result

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    data = request.form
    print(data)
    transorm_data = dict(data)
    
    encoded_data = encode_features(transorm_data)
    input_for_prediction = rearrage_features_for_pred(encoded_data)

    print(input_for_prediction)

    #input_for_prediction = {'data' : [[0, 2, 2, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1]]}
    #print(input_for_prediction)

    end_point = "http://1daa2355-5f05-44e0-a4a2-df7d636e9216.eastus2.azurecontainer.io/score"
    predictions = end_point_predictions(end_point, input_for_prediction)
    print(predictions, "END POINT PREDICTIONS")
    data = dict(data)
    data["PERSISTENCY PREDICTION RESULT"] = presistecy_flag_mapper[int(predictions)]
    return render_template("results.html", output=data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

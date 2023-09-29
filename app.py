from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    living_area = float(request.form.get('living_area'))
    house_area = np.log(living_area)
    waterfront = 1 if request.form.get('waterfront') == 'Yes' else 0
    grade = float(request.form.get('grade'))
    view = float(request.form.get('view'))
    condition = float(request.form.get('condition'))
    age = float(request.form.get('age'))
    renovation = 1 if request.form.get('renovation') == 'Yes' else 0
    land = float(request.form.get('land'))
    land_area = float((request.form.get('land')))
    zipcode = float(request.form.get('zipcode'))
    
    month_to_number = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

    month = request.form.get('month')

    if month in month_to_number:
        numerical_value = month_to_number[month]
    else:
        numerical_value = None
    
    
    prediction = model.predict([[house_area, land_area, waterfront, 
                                view,condition, grade, numerical_value,
                                age, renovation,zipcode]])
    
    prediction_converted = np.exp(prediction)[0]
    
    if prediction_converted >= 1000000:
        output = '{:.3f} Million Dollar'.format(prediction_converted / 1000000)
    else:
        output = '{:.2f} Thousand Dollar'.format(prediction_converted / 1000)

    return render_template("index.html", prediction_text='The Price of This House is About: <br><p>{}</p>'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
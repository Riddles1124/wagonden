from flask import Flask
from flask import request, render_template
from predictor_api import make_prediction, names

app = Flask(__name__)

@app.route('/predict', methods=['GET','POST'])
def predict():
    x_input,predictions = make_prediction(request.args)
    return render_template('predictor.html',
            breed_names=names,
            x_input=x_input,
            predictions=predictions
            )


if __name__ == '__main__':
    app.run(debug=True)

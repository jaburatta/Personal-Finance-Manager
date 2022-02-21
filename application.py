# Import necessary libraries
from flask import Flask, request, render_template
import joblib

application= Flask(__name__)


model = joblib.load(open('mono.pkl','rb'))


@application.route('/', methods=['GET', 'POST'])
def home():

     output = ''
     if request.method == "POST":

        narration = request.form.get('narration')
        prediction = model.predict(narration)
        
        output = prediction[0]       
        
     return render_template('index.html', result=output)

if __name__ == "__main__":
    application.run(host="0.0.0.0")
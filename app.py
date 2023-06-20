from flask import Flask, render_template, request, url_for, send_file, redirect
import os
import csv
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import model_handling

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internal.db'
app.config['UPLOAD_FOLDER'] = 'activity_uploads'
db = SQLAlchemy(app=app)
db.init_app(app)

class activity_store(db.Model):
    activity_datetime = db.Column(db.DateTime, primary_key=True)
    activity_duration = db.Column(db.Integer)
    activity_load = db.Column(db.Integer)

    def __repr__(self):
        return '<Activity {}>'.format(self.activity_datetime) 

@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template("index.html")

@app.route("/modeling", methods=["GET"])
def modeling_load():
    return render_template('modeling.html')

@app.route("/activities", methods=['GET'])
def activities():
    try:
        activities = activity_store.query.order_by(activity_store.activity_datetime).all()
        return render_template('activities.html', activities=activities)
    except:
        return render_template('activities.html', activities=[])
    
@app.route("/plot")
def plot():
    # Generate some data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Plot the data
    plt.plot(x, y)

    # Save the plot as a PNG image
    plt.savefig("plot.png")

    # Return the PNG image as a response
    return send_file("plot.png", mimetype="image/png")


@app.route("/activityinput", methods=["GET"])
def activity_input():
    return render_template('activityinput.html')


@app.route("/activityinput/activitycsv", methods=["POST"])
def submit_activity_input_csv():
    # Churn through the csv for new activity data
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
        parseCSV(file_path)
        delete_file(file_path)
    try:
        return redirect('/')
    except Exception as exc:
        print(f'Exception :: {exc} occured while commiting new data')
        return 'There was an issue adding your activity'
    
def parseCSV(file_path):
    with open(file_path) as f:
        reader = csv.reader(f)
        header = next(reader)
        for i in reader:
            kwargs = {column: value for column, value in zip(header, i)}
            new_entry = activity_store(**kwargs)
            db.session.add(new_entry)
            db.session.commit()

def delete_file(file_path:os.path):
    os.remove(file_path)
    return 0

@app.route("/activityinput/activity", methods=["POST"])
def submit_activity_input():
    # Get the form data
    activity_datetime_str = request.form["activity_date"]
    activity_duration = int(request.form["activity_duration"])
    activity_load = int(request.form["activity_load"])

    activity_datetime = datetime.strptime(activity_datetime_str, "%Y-%m-%d")

    new_activity = activity_store(
        activity_datetime=activity_datetime,
        activity_duration=activity_duration,
        activity_load=activity_load)

    try:
        db.session.add(new_activity)
        db.session.commit()
        return redirect('/activityinput')
    except Exception as exc:
        print(f'Exception :: {exc} occured while commiting new data')
        return 'There was an issue adding your activity'

if __name__ == "__main__":
    app.run(debug=True)
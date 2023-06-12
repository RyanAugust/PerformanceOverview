from flask import Flask, render_template, request, url_for, send_file, redirect
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internal.db'
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


@app.route("/activities", methods=['GET'])
def activities():
    activities = activity_store.query.order_by(activity_store.activity_datetime).all()
    return render_template('activities.html', activities=activities)

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


@app.route("/activityinput", methods=["GET","POST"])
def submit_activity_input():
    if request.method == 'POST':
        # Get the form data
        activity_datetime = request.form["activity_date"]
        activity_duration = request.form["activity_duration"]
        activity_load = request.form["activity_load"]

        new_activity = activity_store(
            activity_date=activity_datetime,
            activity_duration=activity_duration,
            activity_load=activity_load)

        try:
            db.session.add(new_activity)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your activity'
    else:
        return render_template('activityinput.html')

if __name__ == "__main__":
    app.run(debug=True)
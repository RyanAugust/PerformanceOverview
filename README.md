# Overview
Incredibly simplistic UI that handles activity upload or logging and provides a venue to test out each of the different PMC & NN models against your activity history.


# Dev setup
Biggest thing is getting the db set up to ingest activity uploads. 
In a python shell run the following and the app will build out the compliant, blank db
```from app import app, db
with app.app_context():
    db.create_all()
```
That's it. Done.

For all I care upload directly to it for now and don't use the UI but at least it's there if you need it and the app will expect the db to be setup up with the schema constructed with the above.

## Flask things
`flask run` how easy is that. Nice...

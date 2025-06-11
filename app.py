from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from models import db, Sighting
import os, folium
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# create tables on startup
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

@app.route("/")
def index():
    # fetch sightings and build map
    all_sightings = Sighting.query.order_by(Sighting.time_spotted.desc()).all()
    m = folium.Map(
        location=[47.655, -122.308],
        zoom_start=14,
        width="500px",
        height="500px"
    )
    for s in all_sightings:
        folium.Marker(
            [s.latitude, s.longitude],
            popup=(
                f"{s.description}<br>"
                f"<b>{s.species}</b><br>"
                f"{s.time_spotted.strftime('%I:%M:%S %p')} @ {s.location}"
            )
        ).add_to(m)

    return render_template("index.html",
                           sightings=all_sightings,
                           map_html=m._repr_html_())

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # save new sighting to db
        new = Sighting(
            description   = request.form["description"],
            species       = request.form["species"],
            latitude      = float(request.form["latitude"]),
            longitude     = float(request.form["longitude"]),
            location      = request.form["location"],
            time_spotted  = datetime.now()
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("index"))

    # show folium pick-a-point map
    pick_map = folium.Map(
        location=[47.655, -122.308],
        zoom_start=14,
        width=600,
        height=400
    )
    pick_map.add_child(folium.LatLngPopup())
    return render_template("submission.html", map_html=pick_map._repr_html_())

@app.route("/delete/<int:id>", methods=["POST"])
def delete_sighting(id):
    # delete a sighting by clicking button on far right
    sighting = Sighting.query.get_or_404(id)
    db.session.delete(sighting)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # ensure tables exist then run
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)

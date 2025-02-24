from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Tab
import os
import re

app = Flask(__name__)
CORS(app) 

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

TAB_REGEX = re.compile(r'^[0-9\-]+$')

@app.route("/api/tabs", methods=["POST"])
def create_tab():
    data = request.get_json()
    
    errors = []
    if not data.get("title"):
        errors.append("Title is required.")
    if not TAB_REGEX.match(data.get("string1", "")):
        errors.append("Invalid characters in string1.")
    if not TAB_REGEX.match(data.get("string2", "")):
        errors.append("Invalid characters in string2.")
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    new_tab = Tab(
        title=data["title"],
        artist=data.get("artist", ""),
        tuning=data.get("tuning", ["D", "A"]),
        string1=data["string1"],
        string2=data["string2"]
    )
    
    db.session.add(new_tab)
    db.session.commit()
    
    return jsonify(new_tab.to_dict()), 201

@app.route("/api/tabs/<int:tab_id>", methods=["GET"])
def get_tab(tab_id):
    tab = Tab.query.get(tab_id)
    if not tab:
        return jsonify({"error": "Tab not found."}), 404
    return jsonify(tab.to_dict())

@app.route("/api/tabs/search", methods=["GET"])
def search_tabs():
    query = request.args.get("q", "")
    tabs = Tab.query.filter(
        (Tab.title.ilike(f"%{query}%")) | 
        (Tab.artist.ilike(f"%{query}%"))
    ).all()
    return jsonify([tab.to_dict() for tab in tabs])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
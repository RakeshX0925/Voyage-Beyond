from flask import Flask, flash, redirect, render_template, request, url_for
from analytics import get_analytics, load_planets
from database import get_quiz_summary, init_db, save_quiz_attempt

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-development-key"
init_db()

QUIZ_QUESTIONS = [
    {"question": "Which is the largest planet in our Solar System?", "options": ["Earth", "Jupiter", "Saturn", "Neptune"], "answer": "Jupiter"},
    {"question": "Which planet is closest to the Sun?", "options": ["Venus", "Earth", "Mercury", "Mars"], "answer": "Mercury"},
    {"question": "Which planet is known for its prominent rings?", "options": ["Mars", "Venus", "Saturn", "Mercury"], "answer": "Saturn"},
    {"question": "What category does Pluto belong to?", "options": ["Planet", "Dwarf planet", "Moon", "Star"], "answer": "Dwarf planet"},
    {"question": "Which planet is our home?", "options": ["Earth", "Mars", "Venus", "Uranus"], "answer": "Earth"},
]


@app.route("/")
def home():
    data = load_planets()
    return render_template("index.html", object_count=len(data), planet_count=int((data["category"] == "Planet").sum()))


@app.route("/explorer")
def explorer():
    data = load_planets()
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    if query:
        data = data[data["name"].str.contains(query, case=False, na=False)]
    if category in {"Planet", "Moon", "Dwarf planet"}:
        data = data[data["category"] == category]
    objects = data.fillna("").to_dict(orient="records")
    return render_template("explorer.html", objects=objects, query=query, category=category)


@app.route("/compare")
def compare():
    data = load_planets()
    names = data["name"].tolist()
    first_name = request.args.get("first", "Earth")
    second_name = request.args.get("second", "Jupiter")
    if first_name not in names:
        first_name = "Earth"
    if second_name not in names:
        second_name = "Jupiter"
    records = data.set_index("name").fillna("").to_dict(orient="index")
    return render_template("compare.html", names=names, first=first_name, second=second_name, a=records[first_name], b=records[second_name])


@app.route("/analytics")
def analytics():
    return render_template("analytics.html", report=get_analytics())


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        player_name = request.form.get("player_name", "").strip()
        if not player_name:
            flash("Please enter a name to save your score.", "error")
            return redirect(url_for("quiz"))
        answers = request.form
        score = sum(1 for i, question in enumerate(QUIZ_QUESTIONS) if answers.get(f"q{i}") == question["answer"])
        try:
            save_quiz_attempt(player_name, score, len(QUIZ_QUESTIONS))
        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("quiz"))
        flash(f"Your score is {score}/{len(QUIZ_QUESTIONS)}. Your attempt has been saved.", "success")
        return redirect(url_for("quiz"))
    return render_template("quiz.html", questions=QUIZ_QUESTIONS, summary=get_quiz_summary())


@app.route("/health")
def health():
    return {"status": "ok", "service": "Voyage Beyond"}


if __name__ == "__main__":
    app.run(debug=True)

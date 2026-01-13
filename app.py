from flask import Flask, render_template, request, redirect, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Profession
from forms import TestForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)


def admin_required():
    if not session.get("admin"):
        abort(403)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["action"]

        user = User.query.filter_by(username=username).first()

        if action == "register":
            if user:
                return render_template("index.html", error="User already exists")
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            session["user"] = username
            session["admin"] = False
            return redirect("/")

        if action == "login":
            if user and check_password_hash(user.password, password):
                session["user"] = user.username
                session["admin"] = user.is_admin
                return redirect("/")
            return render_template("index.html", error="Invalid login")

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/test", methods=["GET", "POST"])
def test():
    if not session.get("user"):
        return redirect("/")

    form = TestForm()

    if form.validate_on_submit():
        user_scores = {
            "math": (int(form.q1.data) + int(form.q2.data) + int(form.q10.data)) // 3,
            "tech": (int(form.q3.data) + int(form.q4.data)) // 2,
            "art": (int(form.q5.data) + int(form.q6.data)) // 2,
            "social": (int(form.q7.data) + int(form.q8.data) + int(form.q9.data)) // 3
        }

        professions = Profession.query.all()
        results = []

        for p in professions:
            score = (
                abs(p.math - user_scores["math"]) +
                abs(p.tech - user_scores["tech"]) +
                abs(p.art - user_scores["art"]) +
                abs(p.social - user_scores["social"])
            )
            results.append((score, p.name))

        results.sort()

        return render_template(
            "result.html",
            faculty=results[0][1] if results else "No data",
            alt1=results[1][1] if len(results) > 1 else "",
            alt2=results[2][1] if len(results) > 2 else ""
        )

    return render_template("test.html", form=form)


@app.route("/admin")
def admin_panel():
    admin_required()
    return render_template(
        "admin.html",
        professions=Profession.query.all(),
        users=User.query.all()
    )


@app.route("/admin/add", methods=["POST"])
def add_profession():
    admin_required()
    p = Profession(
        name=request.form["name"],
        math=int(request.form["math"]),
        tech=int(request.form["tech"]),
        art=int(request.form["art"]),
        social=int(request.form["social"])
    )
    db.session.add(p)
    db.session.commit()
    return redirect("/admin")


@app.route("/admin/delete/<int:id>")
def delete_profession(id):
    admin_required()
    p = Profession.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect("/admin")


with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)

    if Profession.query.count() == 0:
        db.session.add_all([
            Profession("პროგრამისტი",5,5,2,2),
            Profession("ინჟინერი",5,4,1,2),
            Profession("დიზაინერი",1,2,5,3),
            Profession("ფსიქოლოგი",1,1,3,5),
        ])
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)

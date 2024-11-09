from datetime import datetime, timedelta, timezone

from flask import Flask, flash, render_template, redirect, request, url_for

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import User, Group, Post, db

from sqlalchemy.sql import text

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

with app.app_context():
    db.init_app(app)
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_action():
    username = request.form["username"]
    # password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"No such user '{username}'")
        return redirect(url_for("login_page"))
    # if password != user.password:
    #     flash(f"Invalid password for the user '{username}'")
    #     return redirect(url_for("login_page"))

    login_user(user)
    flash(f"Welcome back, {username}!")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html", groups=Group.query.all())


@app.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_action():
    username = request.form["username"]
    if User.query.filter_by(username=username).first():
        flash(f"The username '{username}' is already taken")
        return redirect(url_for("register_page"))

    is_organizer = True if request.form.get('is_organizer') else False
    print(request.form.get("is_organizer"))
    user = User(username=username, is_organizer=is_organizer)

    db.session.add(user)
    db.session.commit()

    login_user(user)
    flash(f"Welcome {username}!")
    return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout_page():
    return render_template("logout.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout_action():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("index"))


@app.route("/group_posts/<int:group_id>", methods=['GET'])
def post_list(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template("post_list.html", group=group)


@app.route("/posts_by_group/<int:group_id>", methods=['GET'])
def posts_by_group(group_id):
    posts = Post.query.from_statement(
        text("SELECT * FROM posts WHERE group_id = :group_id order by date_fm desc")
    ).params(group_id=group_id).all()
    return render_template("post_list_group.html", posts=posts)



@app.route('/add_post/<int:group_id>', methods=['GET', 'POST'])
def add_post(group_id):
    group = Group.query.get_or_404(group_id)
    if request.method == 'POST':
        title = request.form['title']
        context = request.form['context']
        due_date = datetime.now(timezone.utc) + timedelta(days=10)
        db.session.add(Post(title=title, context=context, date_to=due_date,
                        group=group, editor=current_user ))
        db.session.commit()
        return redirect(url_for('post_list',  group_id=group_id))
    
    return render_template('create_post.html', group=group)


if __name__ == "__main__":
    app.run(debug=True, port=8000)

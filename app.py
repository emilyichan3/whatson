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
    return render_template("index.html", groups=Group.query.all(), user=current_user)


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
    return render_template("post_list.html", action='view', group=group, user=current_user)


@app.route("/posts_by_group/<int:group_id>", methods=['GET'])
def posts_by_group(group_id):
    posts = Post.query.from_statement(
        text("SELECT * FROM posts WHERE group_id = :group_id order by date_fm desc")
    ).params(group_id=group_id).all()
    return render_template("post_list_group.html", posts=posts)


@app.route('/add_post/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_post(group_id):
    group = Group.query.get_or_404(group_id)
    formatted_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    if request.method == 'POST':
        try:
            title = request.form['title']
            context = request.form['context']
            date_from = datetime.strptime(request.form['date_from'], '%Y-%m-%d')
            date_to = datetime.strptime(request.form['date_to'], '%Y-%m-%d')    
             # Validate that the date from is not later than the date to
            if is_date_from_earlier_date_to(date_from, date_to):
                # Add the new post to the database
                db.session.add(Post(title=title, 
                                    context=context, 
                                    date_fm=date_from, 
                                    date_to=date_to,
                                    group=group, 
                                    editor=current_user ))
                db.session.commit()
                return redirect(url_for('post_list',  group_id=group_id))
            else:
                # Flash message and re-render the page with the entered data
                flash("End date should not be earlier than the start date.", "error")
                return render_template(
                    'post.html',
                    action='add',
                    group=group,
                    title=title,
                    context=context,
                    date_from=request.form['date_from'],
                    date_to=request.form['date_to'],
                    default_date=formatted_date
                )
        except ValueError:
           # Flash an error message for invalid date input
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return render_template(
                'post.html',
                action='add',
                group=group,
                title=request.form.get('title', ''),
                context=request.form.get('context', ''),
                date_from=request.form.get('date_from', ''),
                date_to=request.form.get('date_to', ''),
                default_date=formatted_date
            )
    # Render the form with default data for GET requests
    return render_template('post.html', action='add', group=group, default_date=formatted_date)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    formatted_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    if request.method == 'POST':
        try:
            group_id = post.group_id
            post.title = request.form['title']
            post.context = request.form['context']
            post.date_fm = datetime.strptime(request.form['date_from'], '%Y-%m-%d')
            post.date_to = datetime.strptime(request.form['date_to'], '%Y-%m-%d')
            # Validate that the date from is not later than the date to
            if is_date_from_earlier_date_to(post.date_fm, post.date_to):
                db.session.commit()
                return redirect(url_for('post_list',  group_id=group_id))
            else:
                # Flash message and re-render the page with the entered data
                flash("End date should not be earlier than the start date.", "error")
                return render_template(
                    'post.html',
                    action='edit',
                    post=post,
                    title=request.form.get('title', ''),
                    context=request.form.get('context', ''),
                    date_from=request.form.get('date_from', ''),
                    date_to=request.form.get('date_to', ''),
                    default_date=formatted_date
                )
        except ValueError:
           # Flash an error message for invalid date input
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return render_template(
                'post.html',
                action='edit',
                post=post,
                title=request.form.get('title', ''),
                context=request.form.get('context', ''),
                date_from=request.form.get('date_from', ''),
                date_to=request.form.get('date_to', ''),
                default_date=formatted_date
            )
    # Render the form with default data for GET requests
    return render_template('post.html', action='edit',post=post,default_date=formatted_date)

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        description = request.form['description']
        db.session.add(Group(group_name=group_name, 
                             description=description, 
                             create_user=current_user))
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_group.html')

@app.route('/edit_group/<int:group_id>',  methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    if request.method == 'POST':
        print(group.description)
        group.description = request.form['group_description']
        db.session.commit()    
        return redirect(url_for('index'))
    
    return render_template('edit_group.html', group=group)

def is_date_from_earlier_date_to(date_from, date_to):
    return date_from <= date_to


if __name__ == "__main__":
    app.run(debug=True, port=8000)

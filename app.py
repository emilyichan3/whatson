from datetime import datetime, timedelta, timezone
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, Group, Event, db
from sqlalchemy.sql import text
from sqlalchemy import and_
import validation as validation

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
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"No such user '{username}'")
        return redirect(url_for("login_page"))

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

    if validation.validate_input(validation.User_Validation, 'username',username):
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
    else:
        flash("The max length of username is 20 characters")
        return redirect(url_for("register_page"))



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


@app.route("/group_events/<int:group_id>", methods=['GET'])
def event_list(group_id):
    formatted_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    group = Group.query.get_or_404(group_id)
    events = group.events.filter(
            and_(
                Event.date_to >= formatted_today
            )
        ).order_by(Event.date_fm).all()
    
    return render_template("event_list.html", action='view', group=group, events=events, user=current_user)


@app.route("/events_on", methods=['GET'])
def events_on():
    formatted_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    events = Event.query.from_statement(
        text("SELECT * FROM events WHERE date_fm <= :start_date AND date_to >=:start_date order by date_fm desc")
    ).params(start_date=formatted_today).all()

    return render_template("event_list_on.html", events=events)


@app.route('/add_event/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_event(group_id):
    group = Group.query.get_or_404(group_id)
    formatted_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if request.method == 'POST':
        try:
            title = request.form['title']
            context = request.form['context']
            location = request.form['location']
            date_from = datetime.strptime(request.form['date_from'], '%Y-%m-%d')
            date_to = datetime.strptime(request.form['date_to'], '%Y-%m-%d')    
             # Validate that the date from is not later than the date to
            if validation.is_date_from_earlier_date_to(date_from, date_to):
                # Add the new post to the database
                db.session.add(Event(title=title, 
                                    context=context, 
                                    location=location,
                                    date_fm=date_from, 
                                    date_to=date_to,
                                    group=group, 
                                    editor=current_user ))
                db.session.commit()
                return redirect(url_for('event_list',  group_id=group_id))
            else:
                # Flash message and re-render the page with the entered data
                flash("End date should not be earlier than the start date.", "date-error")
                return render_template(
                    'event.html',
                    action='add',
                    group=group,
                    title=title,
                    context=context,
                    location=location,
                    date_from=request.form['date_from'],
                    date_to=request.form['date_to'],
                    default_date=formatted_date
                )
        except ValueError:
           # Flash an error message for invalid date input
            flash("Invalid date format. Please use YYYY-MM-DD.", "date-error")
            return render_template(
                'event.html',
                action='add',
                group=group,
                title=request.form.get('title', ''),
                context=request.form.get('context', ''),
                location=request.form.get('location', ''),
                date_from=request.form.get('date_from', ''),
                date_to=request.form.get('date_to', ''),
                default_date=formatted_date
            )
    # Render the form with default data for GET requests
    return render_template('event.html', action='add', group=group, default_date=formatted_date)


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    formatted_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if request.method == 'POST':
        try:
            group_id = event.group_id
            event.title = request.form['title']
            event.context = request.form['context']
            event.location = request.form['location']
            event.date_fm = datetime.strptime(request.form['date_from'], '%Y-%m-%d')
            event.date_to = datetime.strptime(request.form['date_to'], '%Y-%m-%d')
            # Validate that the date from is not later than the date to
            if validation.is_date_from_earlier_date_to(event.date_fm, event.date_to):
                db.session.commit()
                return redirect(url_for('event_list',  group_id=group_id))
            else:
                # Flash message and re-render the page with the entered data
                flash("End date should not be earlier than the start date.", "date-error")
                return render_template(
                    'event.html',
                    action='edit',
                    event=event,
                    title=request.form.get('title', ''),
                    context=request.form.get('context', ''),
                    location=request.form.get('location', ''),
                    date_from=request.form.get('date_from', ''),
                    date_to=request.form.get('date_to', ''),
                    default_date=formatted_date
                )
        except ValueError:
           # Flash an error message for invalid date input
            flash("Invalid date format. Please use YYYY-MM-DD.", "date-error")
            return render_template(
                'event.html',
                action='edit',
                event=event,
                title=request.form.get('title', ''),
                context=request.form.get('context', ''),
                location=request.form.get('location', ''),
                date_from=request.form.get('date_from', ''),
                date_to=request.form.get('date_to', ''),
                default_date=formatted_date
            )
    # Render the form with default data for GET requests
    return render_template('event.html', action='edit',event=event,default_date=formatted_date)

@app.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('event_list',  group_id=event.group_id)) 
    return render_template('delete_event.html', event=event)

@app.route('/view_event/<int:event_id>', methods=['GET'])
@login_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    formatted_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return render_template('event.html', action='view',event=event,default_date=formatted_date)


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

@app.route('/view_group/<int:group_id>',  methods=['GET'])
def view_group(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('view_group.html', group=group)



if __name__ == "__main__":
    app.run(debug=True, port=8000)

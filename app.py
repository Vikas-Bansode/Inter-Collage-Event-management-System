from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Local#123",   # add your mysql password
    database="intercollege_event"
)

cursor = db.cursor(dictionary=True)

# Home Page
@app.route('/')
def index():
    return render_template("index.html")


# Register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        college_id = request.form['college']
        password = request.form['password']

        cursor.execute(
            "INSERT INTO students (name,email,phone,college_id,password) VALUES (%s,%s,%s,%s,%s)",
            (name, email, phone, college_id, password)
        )
        db.commit()
        flash("Registration Successful")
        return redirect('/login')

    cursor.execute("SELECT * FROM colleges")
    colleges = cursor.fetchall()
    return render_template("register.html", colleges=colleges)


# Login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect('/dashboard')
        else:
            flash("Invalid Credentials")

    return render_template("login.html")


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template("dashboard.html", name=session['user_name'])


# Events Page
@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return render_template("events.html", events=events)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        name = request.form['name']
        date = request.form['date']
        event_type = request.form['type']
        description = request.form['description']
        max_participants = request.form['max_participants']

        cursor.execute("""
            INSERT INTO events (event_name, event_date, event_type, description, max_participants)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, date, event_type, description, max_participants))

        db.commit()
        return redirect('/events')

    return render_template("add_event.html")

@app.route('/delete_event/<int:id>')
def delete_event(id):
    cursor.execute("DELETE FROM events WHERE id=%s", (id,))
    db.commit()
    return redirect('/events')

@app.route('/edit_event/<int:id>', methods=["GET", "POST"])
def edit_event(id):
    if request.method == "POST":
        name = request.form['name']
        date = request.form['date']
        event_type = request.form['type']
        description = request.form['description']
        max_participants = request.form['max_participants']

        cursor.execute("""
            UPDATE events
            SET event_name=%s, event_date=%s, event_type=%s,
                description=%s, max_participants=%s
            WHERE id=%s
        """, (name, date, event_type, description, max_participants, id))

        db.commit()
        return redirect('/events')

    cursor.execute("SELECT * FROM events WHERE id=%s", (id,))
    event = cursor.fetchone()

    return render_template("edit_event.html", event=event)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

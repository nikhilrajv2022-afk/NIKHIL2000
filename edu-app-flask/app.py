from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Mock Data
USER_CREDENTIALS = {'admin': 'admin123', 'student': 'student123'}

STUDENT_FEES = [
    {'id': 1, 'term': 'Term 1 (Fall)', 'amount': 15000, 'due_date': '2024-09-01', 'status': 'Paid'},
    {'id': 2, 'term': 'Term 2 (Spring)', 'amount': 15000, 'due_date': '2025-01-15', 'status': 'Pending'},
]

STUDENTS_ATTENDANCE = [
    {'id': 101, 'name': 'Alice Johnson', 'status': 'Present'},
    {'id': 102, 'name': 'Bob Smith', 'status': 'Absent'},
    {'id': 103, 'name': 'Charlie Brown', 'status': 'Present'},
]

PARENTS_REVIEWS = [
    {'parent': 'Mrs. Gupta', 'rating': 5, 'comment': 'Excellent improvements!'},
]

MESSAGES = [
    {'sender': 'Admin', 'body': 'Welcome to the portal.', 'time': '10:00 AM'},
]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username
            session['role'] = 'admin' if username == 'admin' else 'student'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('dashboard.html', role=session['role'])

@app.route('/fees')
def fees():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('fees.html', fees=STUDENT_FEES, role=session['role'])

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'user' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        if session['role'] == 'admin':
            flash('Attendance updated successfully!')
        else:
            flash('Permission Denied: Only Admins can mark attendance.')
    return render_template('attendance.html', students=STUDENTS_ATTENDANCE, role=session['role'])

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if 'user' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        if session['role'] == 'admin':
            flash('Marks uploaded successfully!')
        else:
            flash('Permission Denied: Only Admins can upload marks.')
    return render_template('marks.html', students=STUDENTS_ATTENDANCE, role=session['role'])

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if 'user' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        # Parents/Students can submit reviews
        parent_name = request.form.get('parent_name')
        comment = request.form.get('comment')
        rating = int(request.form.get('rating'))
        PARENTS_REVIEWS.insert(0, {'parent': parent_name, 'rating': rating, 'comment': comment})
        flash('Review submitted successfully!')
    return render_template('reviews.html', reviews=PARENTS_REVIEWS, role=session['role'])

@app.route('/communication', methods=['GET', 'POST'])
def communication():
    if 'user' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        msg = request.form.get('message')
        sender = 'Admin' if session['role'] == 'admin' else 'Student'
        MESSAGES.append({'sender': sender, 'body': msg, 'time': 'Now'})
    return render_template('communication.html', messages=MESSAGES, role=session['role'])

if __name__ == '__main__':
    app.run(debug=True)

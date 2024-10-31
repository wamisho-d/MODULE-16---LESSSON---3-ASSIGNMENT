# Task 1: Setting Up Flask with Flask-SQLAlchemy
# 1. Initialize Flask Project and Virtual Environment: 

# python3 -m venv venv
# On Windows: venv\Scripts\activate
# Install required packages:
# pip install Flask Flask-SQLAlchemy Flask-Marshmallow

# 2. Basic Flask Setup with Flask-SQLAlchemy:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/fitness_center_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

 

# 3. Define Members and WorkoutSessions Models:

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    # Relationship with WorkoutSession
    workout_sessions = db.relationship('WorkoutSession', backref='member', lazy=True)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    type = db.Column(db.String(100), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

# 4. Create the Database: 
# flask shell
# >>> from app import db
# >>> db.create_all()

# Task 2: Implementing CRUD Operations for Members Using ORM
# 1. Add Member Route (POST):
from flask import request, jsonify

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member added successfully!'}), 201

 

# 2. Retrieve Members (GET): 

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{'id': m.id, 'name': m.name, 'email': m.email, 'phone': m.phone} for m in members])

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)
    return jsonify({'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone})

 

# 3. Update Member (PUT): 

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    member = Member.query.get_or_404(id)
    member.name = data['name']
    member.email = data['email']
    member.phone = data['phone']
    db.session.commit()
    return jsonify({'message': 'Member updated successfully!'})

 

# 4. Delete Member (DELETE): 

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully!'})

 

# Task 3: Managing Workout Sessions with ORM


# 1. Schedule Workout Session (POST): 

@app.route('/workouts', methods=['POST'])
def add_workout_session():
    data = request.get_json()
    new_session = WorkoutSession(date=data['date'], duration=data['duration'], type=data['type'], member_id=data['member_id'])
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'Workout session scheduled successfully!'}), 201


# 2. Update Workout Session (PUT): 

@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout_session(id):
    data = request.get_json()
    session = WorkoutSession.query.get_or_404(id)
    session.date = data['date']
    session.duration = data['duration']
    session.type = data['type']
    db.session.commit()
    return jsonify({'message': 'Workout session updated successfully!'})

 
# 3. View All Workout Sessions (GET):

@app.route('/members/<int:id>/workouts', methods=['GET'])
def get_workout_sessions(id):
    member = Member.query.get_or_404(id)
    return jsonify([{
        'id': w.id,
        'date': w.date,
        'duration': w.duration,
        'type': w.type
    } for w in member.workout_sessions])

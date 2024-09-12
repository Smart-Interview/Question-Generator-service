from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    test_id = db.Column(db.Integer, nullable=False)  # Foreign key to link with the test
    question_text = db.Column(db.String, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Store the options as JSON
    correct_answer = db.Column(db.String, nullable=False)




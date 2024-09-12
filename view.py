from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Question

# Create a new SQLAlchemy engine
engine = create_engine('sqlite:///scores.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def view_questions():
    """View all questions stored in the database."""
    try:
        # Query all records in the Question table
        questions = session.query(Question).all()
        
        # Print the stored questions
        for question in questions:
            print(f"ID: {question.id}, Test ID: {question.test_id}, Question: {question.question_text}, Options: {question.options}, Answer: {question.correct_answer}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    view_questions()

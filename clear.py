from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Question

# Create a new SQLAlchemy engine
engine = create_engine('sqlite:///scores.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def clear_database():
    """Clear all records from the Question table."""
    try:
        # Start a transaction
        session.begin()
        
        # Query all records in the Question table
        questions = session.query(Question).all()
        
        # Print the stored questions (optional)
        for question in questions:
            print(f"ID: {question.id}, Test ID: {question.test_id}, Question: {question.question_text}, Options: {question.options}, Answer: {question.correct_answer}")
        
        # Delete all records
        session.query(Question).delete()
        
        # Commit the transaction
        session.commit()
        print("Database cleared successfully.")
        
    except Exception as e:
        # Rollback in case of error
        session.rollback()
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    clear_database()

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        # Name cannot be empty
        if not name:
            raise ValueError("Author must have a name.")
        
        # Name must be unique — check the database for existing record
        existing = Author.query.filter_by(name=name).first()
        if existing:
            raise ValueError(f"Author with name '{name}' already exists.")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # Must be exactly 10 digits, no letters or symbols
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        # Title cannot be empty
        if not title:
            raise ValueError("Post must have a title.")
        
        # Must contain at least one clickbait phrase
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must contain 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        
        return title

    @validates('content')
    def validate_content(self, key, content):
        # Content must be at least 250 characters
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        # Summary cannot exceed 250 characters
        if len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        # Only Fiction or Non-Fiction allowed
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
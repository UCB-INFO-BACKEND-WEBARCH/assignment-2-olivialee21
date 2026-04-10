from datetime import datetime
from app import db

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'due_date': self.due_date.isoformat()+'Z' if self.due_date else None,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'created_at': self.created_at.isoformat()+'Z',
            'updated_at': self.updated_at.isoformat()+'Z'
        }


class CategoryModel(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7))
    tasks = db.relationship('TaskModel', backref='category', lazy=True)

    def to_dict(self):
        return { 
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'task_count': len(self.tasks)      
        }
    
    def to_dict_w_tasks(self):
        return { 
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'tasks': [{'id':t.id, 'title':t.title, 'completed':t.completed} for t in self.tasks]      
        }

from flask import Blueprint, request, jsonify
from app.models import db, TaskModel, CategoryModel
from app.schemas import CategorySchema
from marshmallow import ValidationError

categories_blp = Blueprint('categories', __name__)
schema = CategorySchema()

@categories_blp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({"categories": [c.to_dict() for c in CategoryModel.query.all()]}), 200


@categories_blp.route('/categories/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    cat = CategoryModel.query.get_or_404(CategoryModel, cat_id)
    return jsonify(cat.to_dict_w_tasks()), 200

@categories_blp.route('/categories', methods=['POST'])
def create_category():
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    cat = CategoryModel(**data)
    db.session.add(cat)
    db.session.commit()

    return jsonify({"category": cat.to_dict()}), 201

@categories_blp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    cat = CategoryModel.query.get_or_404(cat_id)
    if cat.tasks:
        return jsonify({"error": "Cannot delete category with existing tasks. Move or delete tasks first."}), 400
    
    db.session.delete(cat)
    db.session.commit()

    return jsonify({"message": "Category deleted"}), 200


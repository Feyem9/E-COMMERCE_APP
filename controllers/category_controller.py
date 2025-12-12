from flask import render_template, request, redirect, url_for, session, jsonify
from config import db
from models.category_model import Categories

def index():
    categories = Categories.query.all()
    return jsonify([category.serialize() for category in categories])

def view_category(id):
    category = Categories.query.filter_by(id=id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category.serialize())

def update_category(id):
    category = Categories.query.filter_by(id=id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    if request.method == 'GET':
        return jsonify(category.serialize())
    elif request.method == 'POST':
        name = request.form.get('name')
        category.name = name
        db.session.add(category)
        db.session.commit()
        return jsonify(category.serialize())
    return jsonify(category.serialize())

def delete_category(id):
    if request.method == 'POST':
        if request.form.get('delete'):
            category = Categories.query.filter_by(id=id).first()
            if category:
                db.session.delete(category)
                db.session.commit()
                return jsonify({'message': 'Category deleted successfully'})
            return jsonify({'error': 'Category not found'}), 404
    return jsonify({'error': 'Method not allowed'}), 405

def show_category_form():
    return jsonify({'message': 'Use POST to add a category'})

def add_category():
    if request.method == 'GET':
        return jsonify({'message': 'Use POST to add a category'})
    elif request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        category = Categories(name)
        db.session.add(category)
        db.session.commit()
        return jsonify(category.serialize()), 201

    return jsonify({'error': 'Method not allowed'}), 405

# from flask import render_template , request  , redirect , url_for , session
# from config import db
# from models.category_model import Categories

# def index():
#     categories = Categories.query.all()
#     return render_template('index_category.html', categories=categories)

# def view_category(id):
#     category = Categories.query.filter_by(id=id).first()
#     if not category:
#         return redirect(url_for('index_category'))
#     return render_template('view_category.html', category=category)

# def update_category(id):
#     category = Categories.query.filter_by(id=id).first()
#     if not category:
#         return redirect(url_for('index_category'))
#     if request.method == 'GET':
#         return render_template('update_category.html', category=category)
#     elif request.method == 'POST':
#         name = request.form.get('name')
#         category.name = name
#         db.session.add(category)
#         db.session.commit()
#         return redirect(url_for('index_category'))  
#     return render_template('update_category.html', category=category , title='Update Category successfully')

# def delete_category(id):
#     if request.method == 'POST':
#         if request.form.get('delete'):
#             category = Categories.query.filter_by(id=id).first()
#             db.session.delete(category)
#             db.session.commit()
#             return redirect(url_for('index_category'))
        
# def category():
#     return render_template('add_category.html' , title='add a categories')
# def add_category():
#     if request.method == 'GET':
#         return render_template('add_category.html')
#     elif request.method == 'POST':
#         name = request.form.get('name')
#         category = Categories(name)
#         db.session.add(category)
#         db.session.commit()
#         return redirect(url_for('index_category'))

#     return render_template('add_category.html', title='Add Category successfully')

    

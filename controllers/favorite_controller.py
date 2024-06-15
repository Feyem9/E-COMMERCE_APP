# from flask import render_template , request  , redirect , url_for , session
# from config import db
# from models.favorite_model import Favorites

# def index():
#     favorites = Favorites.query.all()
#     return render_template('index_favorite.html', favorites=favorites)

# def view_favorite(id):
#     favorite = Favorites.query.filter_by(id=id).first()
#     if not favorite:
#         return redirect(url_for('index_favorite'))
#     return render_template('view_favorite.html', favorite=favorite)

# def delete_favorite(id):
#     if request.method == 'POST':
#         if request.form.get('delete'):
#             favorite = Favorites.query.filter_by(id=id).first()
#             db.session.delete(favorite)
#             db.session.commit()
#             return redirect(url_for('index_favorite'))
        
# def favorite():
#     return render_template('add_favorite.html' , title='add a favorite')

# def add_favorite():
#     if request.method == 'GET':
#         return render_template('add_favorite.html')
#     elif request.method == 'POST':
#         name = request.form.get('name')
#         favorite = Favorites(name)
#         db.session.add(favorite)
#         db.session.commit()
#         return redirect(url_for('index_favorite'))

#     return render_template('add_favorite.html', title='Add Favorite successfully')

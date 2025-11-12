from flask import render_template , request  , redirect , url_for , jsonify #type:ignore
from config import db
from models.cart_model import Carts

def index():
    carts = Carts.query.all()
    cart_list = [{
        "id": cart.id,
        "product_id":cart.product_id,
        "product_name":cart.product_name,
        "product_description":cart.product_description,
        "product_image":cart.product_image,
        "quantity": cart.quantity,
        "current_price": cart.current_price,
    }for cart in carts]
    print(cart_list)
    return jsonify(cart_list) , 200

# def view_cart(id):
#     cart = Carts.query.filter_by(id=id).first()
#     if not cart:
#         return redirect(url_for('index_cart'))
#     return render_template('view_cart.html', cart=cart)

# def update_cart(id):
#     if request.method != 'POST':
#         return jsonify({'error': 'Méthode non autorisée'}), 405

#     cart = Carts.query.filter_by(id=id).first()
#     if not cart:
#         return jsonify({'error': 'Produit introuvable dans le panier.'}), 404
#         return redirect(url_for('index_cart'))
    
#     # if request.method == 'GET':
#     #     return render_template('update_cart.html', cart=cart)
    
#     # elif request.method == 'POST':
#     quantity = request.get_json('quantity')
#     cart.quantity = quantity
#     db.session.add(cart)
#     db.session.commit()
#     print("Méthode utilisée :", request.method)
    
#     return jsonify({
#         'message': 'Quantité mise à jour avec succès.',
#         'new_quantity': cart.quantity
#     })
#     return redirect(url_for('index_cart'))  
#     # return jsonify("success method") , 200
#     # return render_template('update_cart.html', cart=cart , title='Update Cart successfully')

# def delete_cart(id):
#     if request.method == 'DELETE':
#         if request.form.get('delete'):
#             cart = Carts.query.filter_by(id=id).first()
#             db.session.delete(cart)
#             db.session.commit()
#             # return redirect(url_for('index_cart'))
#             return jsonify({
#             'message': 'produit supprimé  avec succès.',
#             'new_quantity': cart.quantity
#         }), 200

def delete_cart(id):
    # if request.method == 'DELETE':
        # if request.form.get('delete'):
    cart = Carts.query.filter_by(id=id).first()
    # print(cart)
    if not cart:
        return jsonify({'error': 'Produit non trouvé'}), 404
            
    quantity = cart.quantity  # sauvegarde AVANT suppression
    db.session.delete(cart)
    db.session.commit()
            
    return jsonify({
                'message': 'Produit supprimé avec succès.',
                'deleted_quantity': quantity
    }), 200
    #     else:
    #         return jsonify({'error': 'Clé "delete" manquante dans le formulaire'}), 400
    # return jsonify({'error': 'Méthode non autorisée'}), 405


def update_cart(id):
    cart = Carts.query.get(id)
    if not cart:
        return jsonify({'error': 'Produit introuvable dans le panier.'}), 404

    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Données de quantité manquantes'}), 400

    try:
        quantity = int(data['quantity'])
        if quantity < 0:
            return jsonify({'error': 'La quantité doit être un nombre positif'}), 400
        
        cart.quantity = quantity
        db.session.commit()
        
        response = jsonify({
            'message': 'Quantité mise à jour avec succès.',
            'new_quantity': cart.quantity
        })
        response.headers['Content-Type'] = 'application/json'
        return response, 200
    except ValueError:
        return jsonify({'error': 'La quantité doit être un nombre valide'}), 400
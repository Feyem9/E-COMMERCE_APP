# from flask import render_template , request  , redirect , url_for , session
# from config import db
# from models.transaction_model import Transactions

# def index():
#     transactions = Transactions.query.all()
#     return render_template('index_transaction.html', transactions=transactions)

# def view_transaction(id):
#     transaction = Transactions.query.filter_by(id=id).first()
#     if not transaction:
#         return redirect(url_for('index_transaction'))
#     return render_template('view_transaction.html', transaction=transaction)

# def update_transaction(id):
#     transaction = Transactions.query.filter_by(id=id).first()
#     if not transaction:
#         return redirect(url_for('index_transaction'))
#     if request.method == 'GET':
#         return render_template('update_transaction.html', transaction=transaction)
#     elif request.method == 'POST':
#         status = request.form.get('status')
#         transaction.status = status
#         db.session.add(transaction)
#         db.session.commit()
#         return redirect(url_for('index_transaction'))  
#     return render_template('update_transaction.html', transaction=transaction , title='Update Transaction successfully')

# def delete_transaction(id):
#     if request.method == 'POST':
#         if request.form.get('delete'):
#             transaction = Transactions.query.filter_by(id=id).first()
#             db.session.delete(transaction)
#             db.session.commit()
#             return redirect(url_for('index_transaction'))
        
from flask import Blueprint # type:ignore

from controllers.transaction_controller import index , view_transaction , update_transaction , delete_transaction , initiate_payment, generate_qrcode,confirm_transaction, user_transactions

transaction = Blueprint('transaction', __name__)

transaction.route('/', methods=['GET'])(index)
transaction.route('/view_transaction/<id>', methods=['GET'])(view_transaction)
transaction.route('/update_transaction/<id>', methods=['GET','POST'])(update_transaction)
transaction.route('/delete_transaction/<id>', methods=['POST'])(delete_transaction)
transaction.route('/payment', methods=['POST'])(initiate_payment)
transaction.route('/qrcode/<transaction_id>', methods=['GET'])(generate_qrcode)
transaction.route('/confirm', methods=['POST'])(confirm_transaction)
transaction.route('/user/<int:user_id>', methods=['GET'])(user_transactions)
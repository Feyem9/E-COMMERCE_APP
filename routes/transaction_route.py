from flask import Blueprint # type:ignore

from controllers.transaction_controller import index , view_transaction , update_transaction , delete_transaction , initiate_payment

transaction = Blueprint('transaction', __name__)

transaction.route('/', methods=['GET'])(index)
transaction.route('/view_transaction/<id>', methods=['GET'])(view_transaction)
transaction.route('/update_transaction/<id>', methods=['GET','POST'])(update_transaction)
transaction.route('/delete_transaction/<id>', methods=['POST'])(delete_transaction)
transaction.route('/payment', methods=['POST'])(initiate_payment)
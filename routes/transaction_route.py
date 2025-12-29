from flask import Blueprint # type:ignore

from controllers.transaction_controller import index , view_transaction , update_transaction , delete_transaction , initiate_payment, validate_transaction, payment_webhook

transaction = Blueprint('transaction', __name__)

transaction.route('/', methods=['GET'])(index)
transaction.route('/view_transaction/<transaction_id>', methods=['GET'])(view_transaction)
transaction.route('/update_transaction/<id>', methods=['GET','POST'])(update_transaction)
transaction.route('/delete_transaction/<id>', methods=['POST'])(delete_transaction)
transaction.route('/initiate', methods=['POST'])(initiate_payment)
transaction.route('/validate', methods=['POST'])(validate_transaction)
transaction.route('/webhook', methods=['POST'])(payment_webhook)  # 📧 Webhook PayUnit
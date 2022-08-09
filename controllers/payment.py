from flask import jsonify, request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import order
from .blueprint import product
from .blueprint import payment
from .auth import check_login, is_admin, redirect_to_signin_form, is_admin
from models.user import User
from models.order import Order
from models.payment import Payment
import requests, json

# 결제 요청 페이지 API
@payment.route('/request')
def request_payment():
    user = check_login()
    if not user:
        return redirect_to_signin_form()

    order_id = request.args.get('order_id') # 주소창에서 ?뒤에 있는 것을 받음
    order = Order.find_one(order_id)
    
    return render_template('payment.html', order=order)

# 결제 완료 및 주문 상태 업데이트 API / 결제 완료 > 결제가 실제로 정삭적으로 완료되었는지 확인 > 결제에 대한 정보를 저장 > 주문 document status 완료 상태로 업데이트
@payment.route('/complete', methods=['POST'])
def complete_payment():
    user = check_login()
    if not user:
        return redirect_to_signin_form()

    request_data = request.get_json()
    imp_uid = request_data['imp_uid']
    merchant_uid = request_data['merchant_uid']

    IAMPORE_GET_TOKEN_URL = 'https://api.iamport.kr/users/getToken'
    data = {
        'imp_key': "0548120712725156",
        'imp_secret': "Rx1BBfhoekF2fndtsjeEJvBs4HNSpSEc1VblXcsqnNVRmS3WPpeCZWxfdOku7oqzP9Z3bi7vkq8iFctU"
    }
    headers = {'Content_Type': 'application/json'}
    res = requests.post(IAMPORE_GET_TOKEN_URL, headers=headers, data=json.dumps(data))
    res = res.json()
    access_token = res['response']['access_token']

    iamport_get_payment_data_url = 'https://api.iamport.kr/payments/{imp_url}'
    headers = {'Authorization': access_token}

    res = requests.get(iamport_get_payment_data_url, headers=headers)
    res = res.json()

    payment_data = res['response']

    order = Order.fine_one(merchant_uid)
    if not order:
        return jsonify({"존재하지 않는 주문입니다."})

    if payment_data and payment_data['amount'] == order['product']['price']:
        status = 'success'
        Payment.insert_one(order, payment_data, status)
    else:
        status = 'fail'
        Payment.insert_one(order, payment_data, status)
        return jsonify({"비전상적인 주문입니다."})

    status = {'status': 'complete'}
    Order.update_one(merchant_uid, status)

    return jsonify({'order_id': merchant_uid, 'message': 'success'})
from flask import Flask, redirect, url_for
from controllers.product import product
from controllers.user import user
from controllers.order import order

app = Flask(__name__)

app.secret_key = 'cheong_store'

app.register_blueprint(product, url_prefix='/products')
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(order, url_prefix='/orders')

@app.route("/", methods=['GET']) # methods=['GET'] 방식일 때는 생략이 가능(기본값)
def home():
    return redirect(url_for('product.get_products'))

if __name__ == "__main__": # 자동으로 업데이트가 되지만 flask run이 아닌 python app.py를 이용하여 시작
    app.run(debug=True)
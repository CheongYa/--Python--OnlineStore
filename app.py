from gettext import install
from flask import Flask
from controllers.product import product

app = Flask(__name__)

app.register_blueprint(product, url_prefix='/products')

@app.route("/", methods=['GET']) # methods=['GET'] 방식일 때는 생략이 가능(기본값)
def hello():
    return "Hello, World!"

if __name__ == "__main__": # 자동으로 업데이트가 되지만 flask run이 아닌 python app.py를 이용하여 시작
    app.run(debug=True)
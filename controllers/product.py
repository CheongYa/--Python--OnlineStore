from flask import request, render_template, redirect, url_for
from .blueprint import product
from models.product import Product
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# 상품 등록 페이지 API
@product.route('/form')
def form():
    return render_template('product_form.html')


# 상품 등록 API
@product.route('/regist', methods=['POST']) # blueprint.py 쪽으로 들어감
def regist():
    # 전달받은 상품 정보
    form_data = request.form

    # 이미지 파일 정보
    thumbnail_img = request.files.get('thumbnail_img')
    detail_img = request.files.get('detail_img')
    thumbnail_img_url = ""
    detail_img_url = ""

    if thumbnail_img:
        thumbnail_img_url = _upload_file(thumbnail_img)
    if detail_img:
        detail_img_url = _upload_file(detail_img)

    Product.insert_one(form_data, thumbnail_img_url, detail_img_url) # 저장하는 일

    return "상품 등록 API입니다."

# 상품 리스트 조회 API
@product.route('/list')
def get_products():
    # 상품 리스트 정보 = mongo db products 컬렉션이 있는 documents
    products = Product.find()

    return render_template('products.html', products=products)

# 상품 삭제
@product.route('/<product_id>/delete') # product_id = 특정상품의 고유번호
def delete(product_id):
    # 상품 삭제 구현
    Product.delete_one(product_id)
    
    return "상품이 정삭적으로 삭제되었습니다."

# 상품 정보 수정 페이지 API
@product.route('/<product_id>/edit')
def edit(product_id):
    product = Product.find_one(product_id)

    return render_template('product_edit.html', product=product)

# 상품 정보 수정 API
@product.route('/<product_id>/update', methods=['POST'])
def update(product_id):
    form_data = request.form
    thumbnail_img = request.files.get('thumbnail_img')
    detail_img = request.files.get('detail_img')
    thumbnail_img_url = ""
    detail_img_url = ""
    
    if thumbnail_img:
        thumbnail_img_url = _upload_file(thumbnail_img)
    if detail_img:
        detail_img_url = _upload_file(detail_img)

    Product.update_one(product_id, form_data, thumbnail_img_url, detail_img_url)

    return redirect(url_for('product.get_products'))

def _upload_file(img_file):
    timestamp = str(datetime.now().timestamp())
    filename = timestamp + '_' + secure_filename(img_file.filename)
    image_path = f'./static/uploads'
    os.makedirs(image_path, exist_ok=True)
    img = os.path.join(image_path, filename)
    img_file.save(img)

    return f'./static/uploads' + filename
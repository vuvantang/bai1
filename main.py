from crawl import Crawl
from flask import Flask, render_template, Response, request, redirect, url_for, flash, make_response
from flask_cors import CORS
from config import Config
from models import db, LaptopModel

app = Flask(__name__)
app.secret_key = 'key_bao_mat'

# Load cấu hình kết nối database
app.config.from_object(Config)

# Sử dụng Cors
CORS(app)

# Kết nối database
db.init_app(app)


@app.route('/avg-product')
def avg_brand():
    LaptopModel.trungbinh_trungvi()
    return redirect(url_for('index'))


@app.route('/number-product')
def number_product():
    LaptopModel.number_product()
    return redirect(url_for('index'))


@app.route('/percent-discount')
def percent_discount():
    LaptopModel.min_max_brand()
    return redirect(url_for('index'))


@app.route('/new-price')
def new_price_best_seller():
    LaptopModel.new_price_best_seller()
    return redirect(url_for('index'))

# Route crawl dữ liệu từ trang web gearvn.com


@app.route('/crawl', methods=['GET'])
def crawl_laptop():
    url = 'https://gearvn.com/collections/laptop-gaming-ban-chay'
    laptops = Crawl.get_laptop_from_url(url)
    for laptop in laptops:
        laptop.save()

    # return LaptopModel.serialize_list(laptops)
    return redirect(url_for('index'))


@app.route('/')
def index():
    laptops = LaptopModel.query.all()
    return render_template('index.html', laptops=laptops)


@app.route('/add_laptop', methods=['GET', 'POST'])
@app.route('/edit_laptop/<int:laptop_id>', methods=['GET', 'POST'])
def edit_laptop(laptop_id=None):
    if laptop_id:
        laptop = LaptopModel.query.get(laptop_id)
    else:
        laptop = None

    if not laptop:
        laptop = LaptopModel('', '', 0, 0, 0, False)

    if request.method == 'POST':
        laptop.name = request.form['name']
        laptop.brand = request.form['brand']
        laptop.old_price = request.form['old_price']
        laptop.new_price = request.form['new_price']
        laptop.percent_discount = request.form['percent_discount']
        laptop.best_seller = request.form.get('best_seller') == 'on'

        if not laptop_id:
            db.session.add(laptop)

        db.session.commit()
        flash('Cập nhật thông tin thành công!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_laptop.html', laptop=laptop)


@app.route('/delete_laptop/<int:laptop_id>', methods=['DELETE'])
def delete_laptop(laptop_id):
    laptop = LaptopModel.query.get(laptop_id)
    if laptop:
        db.session.delete(laptop)
        db.session.commit()
        return {'result': 'success'}
    else:
        return {'result': 'failure'}


if __name__ == '__main__':
    with app.app_context():
        # Tạo tất cả bảng nếu chưa tồn tại
        db.create_all()
    app.run(debug=True)

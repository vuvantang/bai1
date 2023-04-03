from crawl import Crawl
from flask import Flask, render_template, Response
from flask_cors import CORS
from config import Config
from models import db, LaptopModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__)

# Load cấu hình kết nối database
app.config.from_object(Config)

# Sử dụng Cors
CORS(app)

# Kết nối database
db.init_app(app)

@app.route('/number-product')
def number_product():

    laptops = LaptopModel.query.all()
    canvas = LaptopModel.number_product(laptops)
    output = io.BytesIO()
    canvas.print_png(output)
    # Truyền dữ liệu ảnh đến trang web
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/percent-discount')
def percent_discount():

    laptops = LaptopModel.query.all()
    canvas = LaptopModel.min_max_brand(laptops)
    output = io.BytesIO()
    canvas.print_png(output)
    # Truyền dữ liệu ảnh đến trang web
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/new-price')
def new_price_best_seller():

    laptops = LaptopModel.query.all()
    canvas = LaptopModel.new_price_best_seller(laptops)
    output = io.BytesIO()
    canvas.print_png(output)
    # Truyền dữ liệu ảnh đến trang web
    return Response(output.getvalue(), mimetype='image/png')

# Route crawl dữ liệu từ trang web gearvn.com
@app.route('/crawl', methods=['GET'])
def crawl_laptop():
    url = 'https://gearvn.com/collections/laptop-gaming-ban-chay'
    laptops = Crawl.get_laptop_from_url(url)
    for laptop in laptops:
        laptop.save()
    
    LaptopModel.avg_price(laptops)
    
    return LaptopModel.serialize_list(laptops)

@app.route('/laptops')
def list_laptops():
    laptops = LaptopModel.query.all()
    return render_template('laptops.html', laptops=laptops)

if __name__ == '__main__':
    with app.app_context():
        # Tạo tất cả bảng nếu chưa tồn tại
        db.create_all()
    app.run(debug=True)

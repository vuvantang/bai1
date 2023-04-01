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

@app.route('/')
def index():
    # Tạo hình ảnh đồ thị
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax.set_title('Example Plot')
    # Tạo đối tượng canvas của hình ảnh đồ thị và chuyển thành dữ liệu ảnh PNG
    canvas = FigureCanvas(fig)
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
    LaptopModel.min_max_brand(laptops)
    
    return LaptopModel.serialize_list(laptops)

if __name__ == '__main__':
    with app.app_context():
        # Tạo tất cả bảng nếu chưa tồn tại
        db.create_all()
    app.run(debug=True)

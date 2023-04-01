from flask_sqlalchemy import SQLAlchemy
import json
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io


db = SQLAlchemy()

class LaptopModel(db.Model):
    __tablename__ = 'LAPTOPBESTSELLER'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    old_price = db.Column(db.Integer, nullable=False)
    new_price = db.Column(db.Integer, nullable=False)
    percent_discount = db.Column(db.Integer, nullable=False)
    best_seller = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, brand, old_price, new_price, percent_discount, best_seller):
        self.name = name
        self.brand = brand
        self.old_price = old_price
        self.new_price = new_price
        self.percent_discount = percent_discount
        self.best_seller = best_seller


    def to_dict(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'old_price': self.old_price,
            'new_price': self.new_price,
            'percent_discount': self.percent_discount,
            'best_seller': self.best_seller
        }

    @classmethod
    def serialize_list(cls, laptops):
        laptop_dicts = [laptop.to_dict() for laptop in laptops]
        return json.dumps(laptop_dicts, default=lambda x: x.__dict__)
    
    def convert_list_object(laptops):
        return [laptop.to_dict() for laptop in laptops]
    

    def save(self):
        laptop = LaptopModel.query.filter(LaptopModel.name == self.name,
                                           LaptopModel.new_price == self.new_price).first()
        if laptop:
            laptop.brand = self.brand
            laptop.old_price = self.old_price
            laptop.new_price = self.new_price
            laptop.percent_discount = self.percent_discount
            laptop.best_seller = self.best_seller
        else:
            db.session.add(self)
        
        db.session.commit()
        return self.id
    

    def avg_price(laptops):

        df = pd.DataFrame(LaptopModel.convert_list_object(laptops))
        mean_old_price_by_brand = df.groupby("brand")["old_price"].mean()
        mean_new_price_by_brand = df.groupby("brand")["new_price"].mean()
        median_old_price_by_brand = df.groupby("brand")["old_price"].median()
        median_new_price_by_brand = df.groupby("brand")["new_price"].median()

        # hiển thị kết quả
        print("Trung bình giá bán cũ với các Brand:")
        print(mean_old_price_by_brand)
        print("\nTrung bình giá bán mới với các Brand:")
        print(mean_new_price_by_brand)
        print("\nTrung vị giá bán cũ với các Brand:")
        print(median_old_price_by_brand)
        print("\nTrung vị giá bán mới với các Brand:")
        print(median_new_price_by_brand)

    def number_product(laptops):
        df = pd.DataFrame(LaptopModel.convert_list_object(laptops))
        # Định dạng lại dữ liệu
        brand_count = df['brand'].value_counts()

        # Hiển thị biểu đồ
        # Vẽ biểu đồ
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.bar(brand_count.index, brand_count.values)

        # Đặt tên cho trục x và trục y
        ax.set_xlabel('Brand')
        ax.set_ylabel('Number of Productss')
        return FigureCanvas(fig)

    def min_max_brand(laptops):
        df = pd.DataFrame(LaptopModel.convert_list_object(laptops))
        # Định dạng lại dữ liệu
        # Định dạng lại dữ liệu
        brand_discount = df.groupby('brand')['percent_discount'].agg(['min', 'max'])

        # Vẽ biểu đồ
        fig, ax = plt.subplots()
        brand_discount.plot(kind='bar', ax=ax)

        # Đặt tên cho trục x và trục y
        ax.set_xlabel('Brand')
        ax.set_ylabel('Percent Discount')
        return FigureCanvas(fig)

    def new_price_best_seller(laptops):
        df = pd.DataFrame(LaptopModel.convert_list_object(laptops))
        # Lọc các sản phẩm là BestSeller
        bestsellers = df[df['best_seller'] == True]

        # Tạo instance của Figure
        fig = plt.figure()

        # Vẽ histogram trên Figure
        plt.hist(bestsellers['new_price'], bins=10)

        # Đặt tên cho trục x và trục y
        plt.xlabel('New Price')
        plt.ylabel('Count')

        return FigureCanvas(fig)

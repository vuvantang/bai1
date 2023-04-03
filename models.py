from flask_sqlalchemy import SQLAlchemy
import json
import pandas as pd
import matplotlib.pyplot as plt


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

    def trungbinh_trungvi():
        df = pd.DataFrame(LaptopModel.convert_list_object(
            LaptopModel.query.all()))

        df['old_price'] = df['old_price'] // 1000
        df['new_price'] = df['new_price'] // 1000

        df_grouped = df.groupby('brand').agg(
            {'old_price': ['mean', 'median'], 'new_price': ['mean', 'median']})

        # Hiển thị biểu đồ
        df_grouped.plot(kind='bar')
        plt.title(
            'Trung bình và trung vị giá cũ và giá mới với các Thương hiệu (x 1000 VND)')
        plt.xlabel('Thương hiệu')
        plt.ylabel('Giá VND')
        plt.show()

    def number_product():
        df = pd.DataFrame(LaptopModel.convert_list_object(
            LaptopModel.query.all()))
        # đếm số lượng sản phẩm của từng brand
        brand_counts = df['brand'].value_counts()

        # trực quan hóa bằng biểu đồ cột
        brand_counts.plot(kind='bar', color='blue')

        # cài đặt tiêu đề và nhãn trục
        plt.title('Số lượng sản phẩm theo Thương hiệu')
        plt.xlabel('Thương hiệu')
        plt.ylabel('Số lượng')

        # hiển thị biểu đồ
        plt.show()

    def min_max_brand():
        df = pd.DataFrame(LaptopModel.convert_list_object(
            LaptopModel.query.all()))

        df['old_price'] = df['old_price'] // 1000
        df['new_price'] = df['new_price'] // 1000

        # Tính mức giảm giá của từng sản phẩm
        df['discount'] = df['old_price'] - df['new_price']

        # Tìm sản phẩm có mức giảm giá cao nhất và thấp nhất của từng Brand
        max_discounts = df.groupby('brand')['discount'].max()
        min_discounts = df.groupby('brand')['discount'].min()
        best_discounts = pd.concat([max_discounts, min_discounts], axis=1)
        best_discounts.columns = ['max_discount', 'min_discount']

        # Vẽ biểu đồ cột
        best_discounts.plot(kind='bar', figsize=(12, 6))
        plt.title(
            'Mức giảm giá cao nhất và thấp nhất của sản phẩm mỗi Brand (x 1000 VND)')
        plt.xlabel('Thương hiệu')
        plt.ylabel('Mức giảm giá (VND)')
        plt.xticks(rotation=45)
        plt.show()

    def new_price_best_seller():
        best_sellers = LaptopModel.query.filter_by(best_seller=True).with_entities(
            LaptopModel.name, LaptopModel.new_price).all()

        # Tạo danh sách tên sản phẩm và giá tương ứng
        product_names = [product[0] for product in best_sellers]
        prices = [product[1] // 1000 for product in best_sellers]

        # Tạo biểu đồ cột
        fig, ax = plt.subplots()
        ax.bar(product_names, prices)

        # Đặt tên cho trục x và trục y
        ax.set_xlabel('Sản phẩm')
        ax.set_ylabel('Giá')

        # Đặt tiêu đề cho biểu đồ
        ax.set_title(
            'Giá mới của các sản phẩm bán chạy (x 1000 VND)')

        # Hiển thị biểu đồ
        plt.show()

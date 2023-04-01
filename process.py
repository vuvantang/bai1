import re

class Process:
    @staticmethod
    def convert_text_to_number(text):
        if text is None:
            return 0.0
        return float(re.sub(r'[^\d.]', '', text))
    
    @staticmethod
    def get_brand_name(product_name):
        if product_name is None:
            return ""
        return product_name.split()[2] if "gaming" in product_name.lower() else product_name.split()[1]
        
    @staticmethod
    def get_product_name(product_name):
        if product_name is None:
            return ""
        words = product_name.split()
        return " ".join(words[3:6]) if "laptop gaming" in product_name.lower() else " ".join(words[2:5])
    
    @staticmethod
    def convert_percent(percent):
        if percent is None:
            return 0
        return abs(int(re.sub(r'[^\d]', '', percent)))

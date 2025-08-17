"""
Product Catalog Management
Handles product data and catalog operations
"""

import json
from pathlib import Path


class ProductCatalog:
    """Manages product catalog for feedback collection"""

    def __init__(self, catalog_file="data/products.json"):
        self.catalog_file = Path(catalog_file)
        self.products = self._load_products()

    def _load_products(self):
        """Load products from file or create default catalog"""
        if self.catalog_file.exists():
            try:
                with open(self.catalog_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Create default product catalog
        return self._create_default_catalog()

    def _create_default_catalog(self):
        """Create default product catalog for demo purposes"""
        default_products = {
            "prod_001": {
                "name": "Wireless Bluetooth Headphones",
                "category": "Electronics",
                "price": 79.99,
                "description": "High-quality wireless headphones with noise cancellation",
                "image": "src/assets/wireless_headphone.jpg",
            },
            "prod_002": {
                "name": "Smartphone Case",
                "category": "Accessories",
                "price": 24.99,
                "description": "Protective case for smartphones with drop protection",
                "image": "src/assets/smartphone_case.jpg",
            },
            "prod_003": {
                "name": "Coffee Maker",
                "category": "Home & Kitchen",
                "price": 149.99,
                "description": "Programmable coffee maker with thermal carafe",
                "image": "src/assets/coffee_maker.jpg",
            },
            "prod_004": {
                "name": "Running Shoes",
                "category": "Sports & Outdoors",
                "price": 89.99,
                "description": "Lightweight running shoes with cushioned sole",
                "image": "src/assets/running_shoes.jpg",
            },
            "prod_005": {
                "name": "Laptop Stand",
                "category": "Office Supplies",
                "price": 39.99,
                "description": "Adjustable laptop stand for ergonomic working",
                "image": "src/assets/laptop_stand.jpg",
            },
            "prod_006": {
                "name": "Water Bottle",
                "category": "Sports & Outdoors",
                "price": 19.99,
                "description": "Insulated stainless steel water bottle",
                "image": "src/assets/water_bottle.jpg",
            },
            "prod_007": {
                "name": "Desk Lamp",
                "category": "Home & Kitchen",
                "price": 34.99,
                "description": "LED desk lamp with adjustable brightness",
                "image": "src/assets/desk_lamp.jpg",
            },
            "prod_008": {
                "name": "Wireless Mouse",
                "category": "Electronics",
                "price": 29.99,
                "description": "Ergonomic wireless mouse with long battery life",
                "image": "src/assets/wireless_mouse.jpg",
            },
            "prod_009": {
                "name": "Backpack",
                "category": "Accessories",
                "price": 59.99,
                "description": "Durable backpack with multiple compartments",
                "image": "src/assets/backpack.jpg",
            },
            "prod_010": {
                "name": "Bluetooth Speaker",
                "category": "Electronics",
                "price": 49.99,
                "description": "Portable Bluetooth speaker with rich sound",
                "image": "src/assets/bluetooth_speaker.jpg",
            },
        }

        # Save default catalog
        self._save_products(default_products)
        return default_products

    def _save_products(self, products):
        """Save products to file"""
        self.catalog_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.catalog_file, "w") as f:
            json.dump(products, f, indent=2)

    def get_products(self):
        """Get all products"""
        return self.products

    def get_product(self, product_id):
        """Get specific product by ID"""
        return self.products.get(product_id)

    def search_products(self, query):
        """Search products by name or description"""
        query = query.lower()
        results = {}

        for product_id, product in self.products.items():
            if (
                query in product["name"].lower()
                or query in product["description"].lower()
            ):
                results[product_id] = product

        return results

    def filter_by_category(self, category):
        """Filter products by category"""
        if category == "All":
            return self.products

        return {
            product_id: product
            for product_id, product in self.products.items()
            if product["category"] == category
        }

    def filter_by_price_range(self, min_price, max_price):
        """Filter products by price range"""
        return {
            product_id: product
            for product_id, product in self.products.items()
            if min_price <= product["price"] <= max_price
        }

    def get_categories(self):
        """Get all unique categories"""
        return list(set(product["category"] for product in self.products.values()))

    def add_product(self, product_id, product_data):
        """Add new product to catalog"""
        self.products[product_id] = product_data
        self._save_products(self.products)

    def update_product(self, product_id, product_data):
        """Update existing product"""
        if product_id in self.products:
            self.products[product_id].update(product_data)
            self._save_products(self.products)
            return True
        return False

    def delete_product(self, product_id):
        """Delete product from catalog"""
        if product_id in self.products:
            del self.products[product_id]
            self._save_products(self.products)
            return True
        return False

    def get_product_stats(self):
        """Get catalog statistics"""
        categories = self.get_categories()
        category_counts = {}

        for category in categories:
            category_counts[category] = len(self.filter_by_category(category))

        prices = [product["price"] for product in self.products.values()]

        return {
            "total_products": len(self.products),
            "categories": len(categories),
            "category_breakdown": category_counts,
            "price_range": {
                "min": min(prices) if prices else 0,
                "max": max(prices) if prices else 0,
                "average": sum(prices) / len(prices) if prices else 0,
            },
        }

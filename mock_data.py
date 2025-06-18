from .db import db
from .models import Product

def add_mock_data():
    if not Product.query.first():  
        products = [
            ("Notebook", "A high-quality notebook", 50, 100, "Stationery","https://m.media-amazon.com/images/I/71E181iSlLL.AC_UF1000,1000_QL80.jpg"),
            ("Pen(pack of 10)", "Smooth writing pen", 100, 200, "Stationery","https://m.media-amazon.com/images/I/61QwNP6HCxL.AC_UF1000,1000_QL80.jpg"),
            ("Pouch", "Multi-purpose storage zipper pouch", 300, 20, "Stationery","https://m.media-amazon.com/images/I/51XXuMDBiHL.AC_UY1100.jpg"),
            ("Acrylic Paint Set", "Artist’s essential color collection", 48, 300, "Stationery","https://m.media-amazon.com/images/I/61Y6sF4glOL.AC_UF1000,1000_QL80.jpg"),
            ("Geomentry", "Math instruments for drawing", 20, 200, "Stationery","https://m.media-amazon.com/images/I/71ACOUbxjuL.AC_UF1000,1000_QL80.jpg"),
            ("Casio", "Efficient Casio scientific calculator", 1,100, "Stationery","https://m.media-amazon.com/images/I/61+56mXx2PL.AC_UF1000,1000_QL80.jpg"),
            ("White Board", "Portable lightweight writing board",1,300, "Stationery","https://m.media-amazon.com/images/I/51vdlHJy2iL.jpg"),
            ("3D Pen", "Heat-based filament drawing tool", 10, 450, "Stationery","https://m.media-amazon.com/images/I/61cHEV0PckL.AC_UF1000,1000_QL80.jpg"),
            ("Resin", "Glossy finish coating resin", 10, 200, "Stationery","https://m.media-amazon.com/images/I/61xLmmeg6AL.AC_UF894,1000_QL80.jpg"),
            ("Double Side Tape", "Sticky on both sides", 20, 200, "Stationery","https://m.media-amazon.com/images/I/51dPOhff6sL.AC_UF1000,1000_QL80.jpg"),
            ("Globe", "Spinning map of world", 10, 200, "Stationery","https://m.media-amazon.com/images/I/81ze-3Pa5BL.jpg"),
            ("Pen(pack of 5)", "Smooth writing pen", 50, 200, "Stationery","https://m.media-amazon.com/images/I/61nu15ZnTdL.AC_UF1000,1000_QL80.jpg"),
            ("Desk Organizer", "Keep your desk tidy", 12.99, 50, "Stationery","https://images-eu.ssl-images-amazon.com/images/I/61qfu6yZ1WL.AC_UL375_SR375,375.jpg"),
            ("Pencil", "Wooden pencil for writing", 0.99, 300, "Stationery","https://m.media-amazon.com/images/I/61ujOZmD35L.jpg"),
            ("Eraser(pack of 5)", "Soft eraser", 50, 150, "Stationery","https://m.media-amazon.com/images/I/81lyj7sgJqL.AC_UF1000,1000_QL80.jpg"),
            ("Ruler(pack of 5)", "Plastic ruler for measurements", 25, 80, "Stationery","https://m.media-amazon.com/images/I/71ypewJijnL.AC_UF1000,1000_QL80.jpg"),
            ("Highlighter (10 colours)", "Neon highlighter pack", 100, 120, "Stationery","https://m.media-amazon.com/images/I/61yQv5EdmhL.AC_UF1000,1000_QL80.jpg"),
            ("Sticky Notes", "Colorful sticky notes for reminders", 50, 200, "Stationery","https://m.media-amazon.com/images/I/71W1h8GTqQL.AC_UF1000,1000_QL80.jpg"),
            ("Planner", "Daily planner for organization", 80, 60, "Stationery","https://m.media-amazon.com/images/I/51967Dq82yL.AC_UF1000,1000_QL80.jpg"),
            ("Oil Paste", "Smooth, blendable coloring medium.", 283, 50, "Stationery","https://m.media-amazon.com/images/I/81uU7wGVxaL.AC_UF1000,1000_QL80.jpg"),
            ("1984", "A dystopian classic about totalitarianism", 290, 30, "Books","https://m.media-amazon.com/images/I/81qZ5kGMQ1L.AC_UF1000,1000_QL80.jpg"),
            ("The Alchemist", "A philosophical story about following dreams", 250, 25, "Books","https://m.media-amazon.com/images/I/71aFt4+OTOL.AC_SL1500.jpg"),
            ("Verity", "A psychological thriller packed with suspense", 340, 18, "Books","https://m.media-amazon.com/images/I/91868k2+gUL.jpg"),
            ("The Silent Patient", "A gripping thriller about a woman's silence", 360, 22, "Books","https://m.media-amazon.com/images/I/81JJPDNlxSL.AC_UF1000,1000_QL80.jpg"),
            ("The Song of Achilles", "A tragic retelling of Greek mythology", 370, 16, "Books","https://m.media-amazon.com/images/I/81Rigi45E2L.AC_UF1000,1000_QL80.jpg"),
            ("Before We Were Strangers", "A nostalgic love story of missed chances", 300, 28, "Books","https://m.media-amazon.com/images/I/81YrOtR8qkL.jpg"),
            ("Kafka on the Shore", "A surreal novel blending dreams and reality", 400, 12, "Books","https://m.media-amazon.com/images/I/61zkNbchZ6L.UF1000,1000_QL80.jpg"),
            ("A Little Life", "An emotional exploration of trauma and friendship", 450, 10, "Books","https://m.media-amazon.com/images/I/7156KqGZemL.UF1000,1000_QL80.jpg"),
        ]


        db.session.bulk_insert_mappings(Product, [
            {
                'name': name,
                'description': description,
                'price': price,
                'stock': stock_quantity,
                'category': category,
                'image_url': image_url
            }
            for name, description, price, stock_quantity, category, image_url in products
        ])

        db.session.commit()

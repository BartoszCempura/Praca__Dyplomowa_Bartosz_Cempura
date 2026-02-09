from backend import create_app, db
from backend.models import *
from datetime import datetime
from sqlalchemy import text

def reset_sequences():
    db.session.execute(text("ALTER SEQUENCE catalog.categories_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE catalog.attributes_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE catalog.products_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE catalog.product_attributes_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE catalog.promotions_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE catalog.attribute_weights_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE commerce.transactions_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE commerce.transaction_products_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE analytics.user_product_interactions_id_seq RESTART WITH 1"))
    #db.session.execute(text("ALTER SEQUENCE commerce.delivery_methods_id_seq RESTART WITH 1"))
    #db.session.execute(text("ALTER SEQUENCE commerce.payment_methods_id_seq RESTART WITH 1"))
    db.session.commit()


def reset_database():
    db.session.query(ProductPromotions).delete()
    db.session.query(ProductAttributes).delete()
    db.session.query(TransactionProducts).delete()
    db.session.query(Transactions).delete()
    db.session.query(Products).delete()
    db.session.query(Promotions).delete()
    db.session.query(Attributes).delete()
    db.session.query(Categories).delete()
    db.session.query(AttributeWeights).delete()
    #db.session.query(PaymentMethods).delete()
    #db.session.query(DeliveryMethods).delete()
    db.session.commit()

def seed_main_categories():
    added_count = 0
    print("Dodawanie kategorii głównych...")
    main_categories = [
        {"name": "Komputery"},
        {"name": "Smartfony i telefony"},   
        {"name": "Tablety"}
    ]
    for data in main_categories:
        istnieje = Categories.query.filter_by(name=data["name"]).first()
        if not istnieje:
            new_main_category = Categories(name=data["name"])
            db.session.add(new_main_category)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych kategorii głównych.")

def seed_sub_categories():
    added_count = 0
    print("Dodawanie podkategorii...")
    sub_categories = [
        {"name": "Laptopy", "parent_id": 1},
        {"name": "Stacjonarne", "parent_id": 1},
        {"name": "AIO", "parent_id": 1},
        {"name": "Monitory", "parent_id": 1},
        {"name": "Myszy", "parent_id": 1},
        {"name": "Klawiatury", "parent_id": 1},
        {"name": "Głośniki", "parent_id": 1},
        {"name": "Słuchawki", "parent_id": 1},
        {"name": "Smartfony", "parent_id": 2},
        {"name": "Kable", "parent_id": 2},
        {"name": "Powerbanki", "parent_id": 2},
        {"name": "Ładowarki", "parent_id": 2},
        {"name": "Czytniki e-book", "parent_id": 3},
        {"name": "Graficzne", "parent_id": 3},
        {"name": "Klasyczne", "parent_id": 3},
        {"name": "Rysiki", "parent_id": 2}
    ]
    for data in sub_categories:
        istnieje = Categories.query.filter_by(**data).first()
        if not istnieje:
            new_sub_category = Categories(name=data["name"], parent_id=data["parent_id"])
            db.session.add(new_sub_category)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych podkategorii.")

def seed_attributes():
    added_count = 0
    print("Dodawanie atrybutów produktów...")
    attributes = [
        {"name": "Procesor"},
        {"name": "RAM"},
        {"name": "Karta graficzna"},
        {"name": "Dysk"},
        {"name": "System operacyjny"},
        {"name": "WiFI"},
        {"name": "Przekątna ekranu"},
        {"name": "Rozdzielczość ekranu"},
        {"name": "Częstotliwość odświeżania"},
        {"name": "Klasa energetyczna"},
        {"name": "Rodzaj matrycy"},
        {"name": "Kolor"},
        {"name": "Producent"},
        {"name": "Rodzaj"},
        {"name": "Typ podłączenia"},
        {"name": "Typ"},
        {"name": "Długość przewodu"},
        {"name": "Pasmo przenoszenia"},
        {"name": "Czułość"},
        {"name": "Zasięg"},
        {"name": "Pojemność akumulatora"},
        {"name": "Rozdzielczość matrycy"},
        {"name": "Sposób ładowania"},
        {"name": "Obszar roboczy"},
        {"name": "Standardy tekstu"},
        {"name": "Moc"},
        {"name": "Szybkie ładowanie"},
    ]
    for data in attributes:
        istnieje = Attributes.query.filter_by(name=data["name"]).first()
        if not istnieje:
            new_attribute = Attributes(name=data["name"])
            db.session.add(new_attribute)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych atrybutów.")

def seed_product_attributes():
    print("Dodawanie atrybutów produktów...")
    product_attributes = [
        # Atrybuty dla laptopów
        {"product_id": 1, "attribute_id": 1, "value": "Intel Core i5 210H"},
        {"product_id": 1, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 1, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5060"},
        {"product_id": 1, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 1, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 1, "attribute_id": 6, "value": "Tak"},
        {"product_id": 1, "attribute_id": 7, "value": "15.6"},
        {"product_id": 1, "attribute_id": 8, "value": "1920 x 1080 px"},
        {"product_id": 1, "attribute_id": 9, "value": "144 Hz"},
        {"product_id": 1, "attribute_id": 12, "value": "Niebieski"},
        {"product_id": 1, "attribute_id": 13, "value": "HP"},

        {"product_id": 2, "attribute_id": 1, "value": "Intel Core i7-240H"},
        {"product_id": 2, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 2, "attribute_id": 3, "value": "Intel UHD Graphics 770"},
        {"product_id": 2, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 2, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 2, "attribute_id": 6, "value": "Tak"},
        {"product_id": 2, "attribute_id": 7, "value": "16.0"},
        {"product_id": 2, "attribute_id": 8, "value": "1920 x 1200 px"},
        {"product_id": 2, "attribute_id": 9, "value": "60 Hz"},
        {"product_id": 2, "attribute_id": 12, "value": "Szary"},
        {"product_id": 2, "attribute_id": 13, "value": "LENOVO"},

        {"product_id": 3, "attribute_id": 1, "value": "AMD Ryzen 7"},
        {"product_id": 3, "attribute_id": 2, "value": "24 GB"},
        {"product_id": 3, "attribute_id": 3, "value": "AMD Radeon 780M"},
        {"product_id": 3, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 3, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 3, "attribute_id": 6, "value": "Tak"},
        {"product_id": 3, "attribute_id": 7, "value": "16.0"},
        {"product_id": 3, "attribute_id": 8, "value": "1920 x 1200 px"},
        {"product_id": 3, "attribute_id": 9, "value": "60 Hz"},
        {"product_id": 3, "attribute_id": 12, "value": "Szary"},
        {"product_id": 3, "attribute_id": 13, "value": "LENOVO"},

        {"product_id": 4, "attribute_id": 1, "value": "Intel Core i7-13620H"},
        {"product_id": 4, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 4, "attribute_id": 3, "value": "Intel UHD Graphics 770"},
        {"product_id": 4, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 4, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 4, "attribute_id": 6, "value": "Tak"},
        {"product_id": 4, "attribute_id": 7, "value": "15.6"},
        {"product_id": 4, "attribute_id": 8, "value": "1920 x 1080 px"},
        {"product_id": 4, "attribute_id": 9, "value": "60 Hz"},
        {"product_id": 4, "attribute_id": 12, "value": "Szary"},
        {"product_id": 4, "attribute_id": 13, "value": "ACER "},

        {"product_id": 5, "attribute_id": 1, "value": "AMD Ryzen 5 7235HS"},
        {"product_id": 5, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 5, "attribute_id": 3, "value": "NVIDIA GeForce RTX 3050"},
        {"product_id": 5, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 5, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 5, "attribute_id": 6, "value": "Tak"},
        {"product_id": 5, "attribute_id": 7, "value": "15.6"},
        {"product_id": 5, "attribute_id": 8, "value": "1920 x 1080 px"},
        {"product_id": 5, "attribute_id": 9, "value": "144 Hz"},
        {"product_id": 5, "attribute_id": 12, "value": "Szary"},
        {"product_id": 5, "attribute_id": 13, "value": "LENOVO"},

        {"product_id": 6, "attribute_id": 1, "value": "Intel Core i7-14650HX"},
        {"product_id": 6, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 6, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5060"},
        {"product_id": 6, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 6, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 6, "attribute_id": 6, "value": "Tak"},
        {"product_id": 6, "attribute_id": 7, "value": "15.6"},
        {"product_id": 6, "attribute_id": 8, "value": "2560 x 1440 px"},
        {"product_id": 6, "attribute_id": 9, "value": "165 Hz"},
        {"product_id": 6, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 6, "attribute_id": 13, "value": "MSI"},

        {"product_id": 7, "attribute_id": 1, "value": "Intel Core i7-240H"},
        {"product_id": 7, "attribute_id": 2, "value": "32 GB"},
        {"product_id": 7, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5060"},
        {"product_id": 7, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 7, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 7, "attribute_id": 6, "value": "Tak"},
        {"product_id": 7, "attribute_id": 7, "value": "16"},
        {"product_id": 7, "attribute_id": 8, "value": "2560 x 1600 px"},
        {"product_id": 7, "attribute_id": 9, "value": "120 Hz"},
        {"product_id": 7, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 7, "attribute_id": 13, "value": "DELL"},

        {"product_id": 8, "attribute_id": 1, "value": "Intel Core i9-14900HX"},
        {"product_id": 8, "attribute_id": 2, "value": "64 GB"},
        {"product_id": 8, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5060"},
        {"product_id": 8, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 8, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 8, "attribute_id": 6, "value": "Tak"},
        {"product_id": 8, "attribute_id": 7, "value": "16"},
        {"product_id": 8, "attribute_id": 8, "value": "2560 x 1600 px"},
        {"product_id": 8, "attribute_id": 9, "value": "240 Hz"},
        {"product_id": 8, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 8, "attribute_id": 13, "value": "HP"},

        {"product_id": 8, "attribute_id": 1, "value": "Intel Core i9-14900HX"},
        {"product_id": 8, "attribute_id": 2, "value": "64 GB"},
        {"product_id": 8, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5060"},
        {"product_id": 8, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 8, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 8, "attribute_id": 6, "value": "Tak"},
        {"product_id": 8, "attribute_id": 7, "value": "16"},
        {"product_id": 8, "attribute_id": 8, "value": "2560 x 1600 px"},
        {"product_id": 8, "attribute_id": 9, "value": "240 Hz"},
        {"product_id": 8, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 8, "attribute_id": 13, "value": "HP"},

        {"product_id": 9, "attribute_id": 1, "value": "Apple M4"},
        {"product_id": 9, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 9, "attribute_id": 3, "value": "Apple M4"},
        {"product_id": 9, "attribute_id": 4, "value": "256 GB"},
        {"product_id": 9, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 9, "attribute_id": 6, "value": "Tak"},
        {"product_id": 9, "attribute_id": 7, "value": "13,6"},
        {"product_id": 9, "attribute_id": 8, "value": "2560 x 1600 px"},
        {"product_id": 9, "attribute_id": 9, "value": "240 Hz"},
        {"product_id": 9, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 9, "attribute_id": 13, "value": "APPLE"},
        # Atrybuty dla komputerów stacjonarnych
        {"product_id": 10, "attribute_id": 1, "value": "Intel Core i5-14600KF"},
        {"product_id": 10, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 10, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5070"},
        {"product_id": 10, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 10, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 10, "attribute_id": 6, "value": "Nie"},
        {"product_id": 10, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 10, "attribute_id": 13, "value": "MAD DOG"},

        {"product_id": 11, "attribute_id": 1, "value": "Intel Core i5-13420H"},
        {"product_id": 11, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 11, "attribute_id": 3, "value": "NVIDIA GeForce RTX 4060"},
        {"product_id": 11, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 11, "attribute_id": 5, "value": "Windows 11 Pro"},
        {"product_id": 11, "attribute_id": 6, "value": "Nie"},
        {"product_id": 11, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 11, "attribute_id": 13, "value": "ACER"},

        {"product_id": 12, "attribute_id": 1, "value": "AMD Ryzen 5 7600"},
        {"product_id": 12, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 12, "attribute_id": 3, "value": "NVIDIA GeForce RTX 4060"},
        {"product_id": 12, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 12, "attribute_id": 5, "value": "Brak"},
        {"product_id": 12, "attribute_id": 6, "value": "Nie"},
        {"product_id": 12, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 12, "attribute_id": 13, "value": "LENOVO"},

        {"product_id": 13, "attribute_id": 1, "value": "Intel Core i7-13700"},
        {"product_id": 13, "attribute_id": 2, "value": "32 GB"},
        {"product_id": 13, "attribute_id": 3, "value": "Intel UHD Graphics 770"},
        {"product_id": 13, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 13, "attribute_id": 5, "value": "Brak"},
        {"product_id": 13, "attribute_id": 6, "value": "Tak"},
        {"product_id": 13, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 13, "attribute_id": 13, "value": "ASUS"},

        {"product_id": 14, "attribute_id": 1, "value": "Intel Core i5-14400F"},
        {"product_id": 14, "attribute_id": 2, "value": "32 GB"},
        {"product_id": 14, "attribute_id": 3, "value": "NVIDIA GeForce RTX 5060 Ti"},
        {"product_id": 14, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 14, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 14, "attribute_id": 6, "value": "Tak"},
        {"product_id": 14, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 14, "attribute_id": 13, "value": "MSI"},

        {"product_id": 15, "attribute_id": 1, "value": "Intel Core i3-14100"},
        {"product_id": 15, "attribute_id": 2, "value": "8 GB"},
        {"product_id": 15, "attribute_id": 3, "value": "Intel UHD Graphics 730"},
        {"product_id": 15, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 15, "attribute_id": 5, "value": "Brak"},
        {"product_id": 15, "attribute_id": 6, "value": "Tak"},
        {"product_id": 15, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 15, "attribute_id": 13, "value": "DELL"},

        {"product_id": 16, "attribute_id": 1, "value": "Intel Core i5-14500T"},
        {"product_id": 16, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 16, "attribute_id": 3, "value": "Intel UHD Graphics 770"},
        {"product_id": 16, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 16, "attribute_id": 5, "value": "Brak"},
        {"product_id": 16, "attribute_id": 6, "value": "Tak"},
        {"product_id": 16, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 16, "attribute_id": 13, "value": "DELL"},

        {"product_id": 17, "attribute_id": 1, "value": "Intel Core i5-1235U"},
        {"product_id": 17, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 17, "attribute_id": 3, "value": "Intel UHD Graphics"},
        {"product_id": 17, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 17, "attribute_id": 5, "value": "Brak"},
        {"product_id": 17, "attribute_id": 6, "value": "Tak"},
        {"product_id": 17, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 17, "attribute_id": 13, "value": "MSI"},

        {"product_id": 18, "attribute_id": 1, "value": "Intel Core i5-120U"},
        {"product_id": 18, "attribute_id": 2, "value": "32 GB"},
        {"product_id": 18, "attribute_id": 3, "value": "Intel UHD Graphics"},
        {"product_id": 18, "attribute_id": 4, "value": "2000 GB"},
        {"product_id": 18, "attribute_id": 5, "value": "Windows 11 Pro"},
        {"product_id": 18, "attribute_id": 6, "value": "Tak"},
        {"product_id": 18, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 18, "attribute_id": 13, "value": "MSI"},
        # Atrybuty dla komputerów AIO
        {"product_id": 19, "attribute_id": 1, "value": "Intel Core i5-13420H"},
        {"product_id": 19, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 19, "attribute_id": 3, "value": "Intel UHD Graphics"},
        {"product_id": 19, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 19, "attribute_id": 5, "value": "Brak"},
        {"product_id": 19, "attribute_id": 6, "value": "Tak"},
        {"product_id": 19, "attribute_id": 7, "value": "23,8"},
        {"product_id": 19, "attribute_id": 8, "value": "1920 × 1080 px"},
        {"product_id": 19, "attribute_id": 9, "value": "60"},
        {"product_id": 19, "attribute_id": 12, "value": "Srebrny"},
        {"product_id": 19, "attribute_id": 13, "value": "LENOVO"},

        {"product_id": 20, "attribute_id": 1, "value": "Intel Core i3-1215U"},
        {"product_id": 20, "attribute_id": 2, "value": "8 GB"},
        {"product_id": 20, "attribute_id": 3, "value": "Intel UHD Graphics"},
        {"product_id": 20, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 20, "attribute_id": 5, "value": "Brak"},
        {"product_id": 20, "attribute_id": 6, "value": "Tak"},
        {"product_id": 20, "attribute_id": 7, "value": "27"},
        {"product_id": 20, "attribute_id": 8, "value": "1920 × 1080 px"},
        {"product_id": 20, "attribute_id": 9, "value": "60"},
        {"product_id": 20, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 20, "attribute_id": 13, "value": "ACER"},

        {"product_id": 21, "attribute_id": 1, "value": "Intel Core Ultra i5-125H"},
        {"product_id": 21, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 21, "attribute_id": 3, "value": "Iris Xe Graphics"},
        {"product_id": 21, "attribute_id": 4, "value": "1000 GB"},
        {"product_id": 21, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 21, "attribute_id": 6, "value": "Tak"},
        {"product_id": 21, "attribute_id": 7, "value": "27"},
        {"product_id": 21, "attribute_id": 8, "value": "2560 × 1440 px"},
        {"product_id": 21, "attribute_id": 9, "value": "60"},
        {"product_id": 21, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 21, "attribute_id": 13, "value": "MSI"},

        {"product_id": 22, "attribute_id": 1, "value": "Intel Core i7-150U"},
        {"product_id": 22, "attribute_id": 2, "value": "16 GB"},
        {"product_id": 22, "attribute_id": 3, "value": "Intel UHD Graphics"},
        {"product_id": 22, "attribute_id": 4, "value": "512 GB"},
        {"product_id": 22, "attribute_id": 5, "value": "Windows 11 Home"},
        {"product_id": 22, "attribute_id": 6, "value": "Tak"},
        {"product_id": 22, "attribute_id": 7, "value": "27"},
        {"product_id": 22, "attribute_id": 8, "value": "1920 × 1080 px"},
        {"product_id": 22, "attribute_id": 9, "value": "60"},
        {"product_id": 22, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 22, "attribute_id": 13, "value": "ASUS"},
        # Atrybuty dla monitorów
        {"product_id": 23, "attribute_id": 7, "value": "27"},
        {"product_id": 23, "attribute_id": 8, "value": "2560 x 1440 px"},
        {"product_id": 23, "attribute_id": 9, "value": "180 Hz"},
        {"product_id": 23, "attribute_id": 10, "value": "E"},
        {"product_id": 23, "attribute_id": 11, "value": "IPS"},
        {"product_id": 23, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 23, "attribute_id": 13, "value": "SAMSUNG"},

        {"product_id": 24, "attribute_id": 7, "value": "27"},
        {"product_id": 24, "attribute_id": 8, "value": "2560 x 1440 px"},
        {"product_id": 24, "attribute_id": 9, "value": "240 Hz"},
        {"product_id": 24, "attribute_id": 10, "value": "F"},
        {"product_id": 24, "attribute_id": 11, "value": "IPS"},
        {"product_id": 24, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 24, "attribute_id": 13, "value": "LENOVO"},

        {"product_id": 25, "attribute_id": 7, "value": "23,8"},
        {"product_id": 25, "attribute_id": 8, "value": "1920 x 1080 px"},
        {"product_id": 25, "attribute_id": 9, "value": "100 Hz"},
        {"product_id": 25, "attribute_id": 10, "value": "D"},
        {"product_id": 25, "attribute_id": 11, "value": "IPS"},
        {"product_id": 25, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 25, "attribute_id": 13, "value": "MSI"},

        {"product_id": 26, "attribute_id": 7, "value": "27"},
        {"product_id": 26, "attribute_id": 8, "value": "2560 x 1440 px"},
        {"product_id": 26, "attribute_id": 9, "value": "180 Hz"},
        {"product_id": 26, "attribute_id": 10, "value": "F"},
        {"product_id": 26, "attribute_id": 11, "value": "IPS"},
        {"product_id": 26, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 26, "attribute_id": 13, "value": "LG"},

        {"product_id": 27, "attribute_id": 7, "value": "27"},
        {"product_id": 27, "attribute_id": 8, "value": "2560 x 1440 px"},
        {"product_id": 27, "attribute_id": 9, "value": "180 Hz"},
        {"product_id": 27, "attribute_id": 10, "value": "F"},
        {"product_id": 27, "attribute_id": 11, "value": "IPS"},
        {"product_id": 27, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 27, "attribute_id": 13, "value": "DELL"},

        {"product_id": 28, "attribute_id": 7, "value": "34"},
        {"product_id": 28, "attribute_id": 8, "value": "3440 x 1440 px"},
        {"product_id": 28, "attribute_id": 9, "value": "175 Hz"},
        {"product_id": 28, "attribute_id": 10, "value": "G"},
        {"product_id": 28, "attribute_id": 11, "value": "QD-OLED"},
        {"product_id": 28, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 28, "attribute_id": 13, "value": "MSI"},

        {"product_id": 29, "attribute_id": 7, "value": "26,5"},
        {"product_id": 29, "attribute_id": 8, "value": "2560 x 1440 px"},
        {"product_id": 29, "attribute_id": 9, "value": "280 Hz"},
        {"product_id": 29, "attribute_id": 10, "value": "G"},
        {"product_id": 29, "attribute_id": 11, "value": "WOLED"},
        {"product_id": 29, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 29, "attribute_id": 13, "value": "LG"},

        {"product_id": 30, "attribute_id": 7, "value": "23,8"},
        {"product_id": 30, "attribute_id": 8, "value": "1920 x 1080 px"},
        {"product_id": 30, "attribute_id": 9, "value": "200 Hz"},
        {"product_id": 30, "attribute_id": 10, "value": "D"},
        {"product_id": 30, "attribute_id": 11, "value": "VA"},
        {"product_id": 30, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 30, "attribute_id": 13, "value": "ACER"},

        {"product_id": 31, "attribute_id": 7, "value": "23,8"},
        {"product_id": 31, "attribute_id": 8, "value": "1920 x 1080 px"},
        {"product_id": 31, "attribute_id": 9, "value": "180 Hz"},
        {"product_id": 31, "attribute_id": 10, "value": "E"},
        {"product_id": 31, "attribute_id": 11, "value": "VA"},
        {"product_id": 31, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 31, "attribute_id": 13, "value": "MSI"},
        # atrybuty dla myszy
        {"product_id": 32, "attribute_id": 12, "value": "Grafitowy"},
        {"product_id": 32, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 32, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 32, "attribute_id": 16, "value": "Optyczny"},
        {"product_id": 32, "attribute_id": 17, "value": "Brak"},
        {"product_id": 32, "attribute_id": 19, "value": "4000 DPI"},
        {"product_id": 32, "attribute_id": 20, "value": "10 m"},
        {"product_id": 32, "attribute_id": 13, "value": "LOGITECH"},

        {"product_id": 33, "attribute_id": 12, "value": "Grafitowy"},
        {"product_id": 33, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 33, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 33, "attribute_id": 16, "value": "Optyczny"},
        {"product_id": 33, "attribute_id": 17, "value": "Brak"},
        {"product_id": 33, "attribute_id": 19, "value": "4000 DPI"},
        {"product_id": 33, "attribute_id": 20, "value": "10 m"},
        {"product_id": 33, "attribute_id": 13, "value": "LOGITECH"},

        {"product_id": 34, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 34, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 34, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 34, "attribute_id": 16, "value": "Laserowy"},
        {"product_id": 34, "attribute_id": 17, "value": "Brak"},
        {"product_id": 34, "attribute_id": 19, "value": "1000 DPI"},
        {"product_id": 34, "attribute_id": 20, "value": "10 m"},
        {"product_id": 34, "attribute_id": 13, "value": "LOGITECH"},

        {"product_id": 35, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 35, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 35, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 35, "attribute_id": 16, "value": "Optyczny"},
        {"product_id": 35, "attribute_id": 17, "value": "1 m USB-C"},
        {"product_id": 35, "attribute_id": 19, "value": "18000 DPI"},
        {"product_id": 35, "attribute_id": 20, "value": "10 m"},
        {"product_id": 35, "attribute_id": 13, "value": "STEELLSERIES"},

        {"product_id": 36, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 36, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 36, "attribute_id": 15, "value": "USB"},
        {"product_id": 36, "attribute_id": 16, "value": "Optyczny"},
        {"product_id": 36, "attribute_id": 17, "value": "2,1 m"},
        {"product_id": 36, "attribute_id": 19, "value": "25600 DPI"},
        {"product_id": 36, "attribute_id": 13, "value": "LOGITECH"},

        {"product_id": 37, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 37, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 37, "attribute_id": 15, "value": "USB"},
        {"product_id": 37, "attribute_id": 16, "value": "Optyczny"},
        {"product_id": 37, "attribute_id": 17, "value": "2 m"},
        {"product_id": 37, "attribute_id": 19, "value": "18000 DPI"},
        {"product_id": 37, "attribute_id": 13, "value": "STEELLSERIES"},

        {"product_id": 38, "attribute_id": 12, "value": "Biały"},
        {"product_id": 38, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 38, "attribute_id": 15, "value": "USB"},
        {"product_id": 38, "attribute_id": 16, "value": "Optyczny"},
        {"product_id": 38, "attribute_id": 17, "value": "1.2 m"},
        {"product_id": 38, "attribute_id": 19, "value": "8500  DPI"},
        {"product_id": 38, "attribute_id": 13, "value": "STEELLSERIES"},
         # atrybuty dla klawiatur
        {"product_id": 38, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 38, "attribute_id": 13, "value": "SILVER MONKEY"},
        {"product_id": 38, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 38, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 38, "attribute_id": 16, "value": "Membranowe"},
        {"product_id": 38, "attribute_id": 17, "value": "Brak"},

        {"product_id": 39, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 39, "attribute_id": 13, "value": "SILVER MONKEY"},
        {"product_id": 39, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 39, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 39, "attribute_id": 16, "value": "Membranowe"},
        {"product_id": 39, "attribute_id": 17, "value": "Brak"},

        {"product_id": 40, "attribute_id": 12, "value": "Biała"},
        {"product_id": 40, "attribute_id": 13, "value": "RAMPAGE"},
        {"product_id": 40, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 40, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 40, "attribute_id": 16, "value": "Mechaniczne"},
        {"product_id": 40, "attribute_id": 17, "value": "1,5 m USB-C"},

        {"product_id": 41, "attribute_id": 12, "value": "Szara"},
        {"product_id": 41, "attribute_id": 13, "value": "ENDORFY"},
        {"product_id": 41, "attribute_id": 14, "value": "Bezprzewodowa"},
        {"product_id": 41, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 41, "attribute_id": 16, "value": "Mechaniczne"},
        {"product_id": 41, "attribute_id": 17, "value": "1,8 m USB-C"},

        {"product_id": 42, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 42, "attribute_id": 13, "value": "DELL"},
        {"product_id": 42, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 42, "attribute_id": 15, "value": "USB"},
        {"product_id": 42, "attribute_id": 16, "value": "Membranowe"},
        {"product_id": 42, "attribute_id": 17, "value": "1,5 m"},

        {"product_id": 43, "attribute_id": 12, "value": "Biały"},
        {"product_id": 43, "attribute_id": 13, "value": "REDRAGON"},
        {"product_id": 43, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 43, "attribute_id": 15, "value": "USB"},
        {"product_id": 43, "attribute_id": 16, "value": "Mechaniczne"},
        {"product_id": 43, "attribute_id": 17, "value": "1,5 m"},

        {"product_id": 44, "attribute_id": 12, "value": "Biało-niebieski"},
        {"product_id": 44, "attribute_id": 13, "value": "REDRAGON"},
        {"product_id": 44, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 44, "attribute_id": 15, "value": "USB-C"},
        {"product_id": 44, "attribute_id": 16, "value": "Mechaniczne"},
        {"product_id": 44, "attribute_id": 17, "value": "2 m"},

        {"product_id": 45, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 45, "attribute_id": 13, "value": "Dell"},
        {"product_id": 45, "attribute_id": 14, "value": "Przewodowa"},
        {"product_id": 45, "attribute_id": 15, "value": "USB"},
        {"product_id": 45, "attribute_id": 16, "value": "Membranowe"},
        {"product_id": 45, "attribute_id": 17, "value": "1,8 m"},
         # atrybuty dla głośników
        {"product_id": 46, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 46, "attribute_id": 13, "value": "CREATIVE"},
        {"product_id": 46, "attribute_id": 14, "value": "2.0"},
        {"product_id": 46, "attribute_id": 15, "value": "USB/MiniJack 3,5 mm"},
        {"product_id": 46, "attribute_id": 17, "value": "0,5 m"},
        {"product_id": 46, "attribute_id": 18, "value": "50-20000 Hz"},

        {"product_id": 47, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 47, "attribute_id": 13, "value": "EDIFIER"},
        {"product_id": 47, "attribute_id": 14, "value": "2.0"},
        {"product_id": 47, "attribute_id": 15, "value": "Bluetooth/RCA"},
        {"product_id": 47, "attribute_id": 17, "value": "1.5 m"},
        {"product_id": 47, "attribute_id": 18, "value": "80-20000 Hz"},

        {"product_id": 48, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 48, "attribute_id": 13, "value": "CREATIVE"},
        {"product_id": 48, "attribute_id": 14, "value": "2.0"},
        {"product_id": 48, "attribute_id": 15, "value": "Bluetooth/USB-C"},
        {"product_id": 48, "attribute_id": 17, "value": "1 m"},
        {"product_id": 48, "attribute_id": 18, "value": "65-20000 Hz"},

        {"product_id": 49, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 49, "attribute_id": 13, "value": "EDIFIER"},
        {"product_id": 49, "attribute_id": 14, "value": "2.0"},
        {"product_id": 49, "attribute_id": 15, "value": "RCA/MiniJack 3,5 mm"},
        {"product_id": 49, "attribute_id": 17, "value": "1.5 m"},
        {"product_id": 49, "attribute_id": 18, "value": "75-18000 Hz"},

        {"product_id": 50, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 50, "attribute_id": 13, "value": "EDIFIER"},
        {"product_id": 50, "attribute_id": 14, "value": "2.1"},
        {"product_id": 50, "attribute_id": 15, "value": "MiniJack 3,5 mm"},
        {"product_id": 50, "attribute_id": 17, "value": "1.5 m"},
        {"product_id": 50, "attribute_id": 18, "value": "150-20000 Hz"},

        {"product_id": 51, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 51, "attribute_id": 13, "value": "EDIFIER"},
        {"product_id": 51, "attribute_id": 14, "value": "2.0"},
        {"product_id": 51, "attribute_id": 15, "value": "Bluetooth/USB-C"},
        {"product_id": 51, "attribute_id": 17, "value": "2 m"},
        {"product_id": 51, "attribute_id": 18, "value": "98-20000 Hz"},

        {"product_id": 52, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 52, "attribute_id": 13, "value": "EDIFIER"},
        {"product_id": 52, "attribute_id": 14, "value": "2.0"},
        {"product_id": 52, "attribute_id": 15, "value": "Bluetooth/USB-C"},
        {"product_id": 52, "attribute_id": 17, "value": "2 m"},
        {"product_id": 52, "attribute_id": 18, "value": "98-20000 Hz"},

        {"product_id": 52, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 52, "attribute_id": 13, "value": "CREATIVE"},
        {"product_id": 52, "attribute_id": 14, "value": "2.1"},
        {"product_id": 52, "attribute_id": 15, "value": "USB/MiniJack 3,5 mm"},
        {"product_id": 52, "attribute_id": 17, "value": "2 m"},
        {"product_id": 52, "attribute_id": 18, "value": "50-20000 Hz"},
        # atrybuty dla słuchawek
        {"product_id": 53, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 53, "attribute_id": 13, "value": "JBL"},
        {"product_id": 53, "attribute_id": 14, "value": "Bezprzewodowe"},
        {"product_id": 53, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 53, "attribute_id": 17, "value": "Brak"},
        {"product_id": 53, "attribute_id": 18, "value": "20-20000 Hz"},
        {"product_id": 53, "attribute_id": 19, "value": "102 dB"},

        {"product_id": 54, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 54, "attribute_id": 13, "value": "JBL"},
        {"product_id": 54, "attribute_id": 14, "value": "Bezprzewodowe"},
        {"product_id": 54, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 54, "attribute_id": 17, "value": "Brak"},
        {"product_id": 54, "attribute_id": 18, "value": "10-40000 Hz"},
        {"product_id": 54, "attribute_id": 19, "value": "122 dB"},

        {"product_id": 55, "attribute_id": 12, "value": "Niebieski"},
        {"product_id": 55, "attribute_id": 13, "value": "FRESH N REBEL"},
        {"product_id": 55, "attribute_id": 14, "value": "Bezprzewodowe"},
        {"product_id": 55, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 55, "attribute_id": 17, "value": "Brak"},
        {"product_id": 55, "attribute_id": 18, "value": "20-20000 Hz"},
        {"product_id": 55, "attribute_id": 19, "value": "100 dB"},

        {"product_id": 56, "attribute_id": 12, "value": "Dreamy Pink"},
        {"product_id": 56, "attribute_id": 13, "value": "FRESH N REBEL"},
        {"product_id": 56, "attribute_id": 14, "value": "Bezprzewodowe"},
        {"product_id": 56, "attribute_id": 15, "value": "Bluetooth"},
        {"product_id": 56, "attribute_id": 17, "value": "Brak"},
        {"product_id": 56, "attribute_id": 18, "value": "20-20000 Hz"},
        {"product_id": 56, "attribute_id": 19, "value": "95 dB"},

        {"product_id": 57, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 57, "attribute_id": 13, "value": "SONY"},
        {"product_id": 57, "attribute_id": 14, "value": "Przewodowe"},
        {"product_id": 57, "attribute_id": 15, "value": "MiniJack 3,5 mm"},
        {"product_id": 57, "attribute_id": 17, "value": "1,2 m"},
        {"product_id": 57, "attribute_id": 18, "value": "12-22000 Hz"},
        {"product_id": 57, "attribute_id": 19, "value": "98 dB"},

        {"product_id": 58, "attribute_id": 12, "value": "Niebieski"},
        {"product_id": 58, "attribute_id": 13, "value": "JBL"},
        {"product_id": 58, "attribute_id": 14, "value": "Przewodowe"},
        {"product_id": 58, "attribute_id": 15, "value": "MiniJack 3,5 mm"},
        {"product_id": 58, "attribute_id": 17, "value": "1,2 m"},
        {"product_id": 58, "attribute_id": 18, "value": "20-20000 Hz"},
        {"product_id": 58, "attribute_id": 19, "value": "98 dB"},

        {"product_id": 59, "attribute_id": 12, "value": "Czarny"},
        {"product_id": 59, "attribute_id": 13, "value": "SONY"},
        {"product_id": 59, "attribute_id": 14, "value": "Przewodowe"},
        {"product_id": 59, "attribute_id": 15, "value": "MiniJack 3,5 mm"},
        {"product_id": 59, "attribute_id": 17, "value": "2,5 m"},
        {"product_id": 59, "attribute_id": 18, "value": "5-80000 Hz"},
        {"product_id": 59, "attribute_id": 19, "value": "100 dB"},

        {"product_id": 60, "attribute_id": 12, "value": "Biały"},
        {"product_id": 60, "attribute_id": 13, "value": "SONY"},
        {"product_id": 60, "attribute_id": 14, "value": "Przewodowe"},
        {"product_id": 60, "attribute_id": 15, "value": "USB"},
        {"product_id": 60, "attribute_id": 17, "value": "1,2 m"},
        {"product_id": 60, "attribute_id": 18, "value": "10-20000 Hz"},
        {"product_id": 60, "attribute_id": 19, "value": "92 dB"}

    ]
    
    for data in product_attributes:
        istnieje = ProductAttributes.query.filter_by(product_id=data["product_id"], attribute_id=data["attribute_id"]).first()
        if not istnieje:
            new_product_attribute = ProductAttributes(product_id=data["product_id"], attribute_id=data["attribute_id"], value=data["value"])
            db.session.add(new_product_attribute)
    db.session.commit()
    print(f"Proces dodawania atrybutów produktów zakończony.")

def seed_products():
    added_count = 0
    print("Dodawanie produktów...")
    products = [
        # Laptopy
        {"name": "HP Victus 15", "category_id": 4, "description": "HP Victus 15 to laptop stworzony dla pasjonatów gier, którzy cenią połączenie mocy i stylu. Sercem maszyny jest procesor Intel Core 5 210H oraz karta graficzna NVIDIA GeForce RTX 5060, co przekłada się na wysoką płynność rozgrywki i fotorealistyczne efekty wizualne. Zaawansowany układ chłodzenia utrzymuje optymalną temperaturę podzespołów, a kamera HD z redukcją szumów sprawia, że komunikacja z drużyną jest zawsze krystalicznie czysta. Dopracowany design i bogata paleta kolorów czynią z Victusa Twoim towarzysza zarówno w pracy, jak i podczas wirtualnej rozrywki.", "Image": "/images/products/Laptopy/Laptop HP Victus 15-FA2039NW.jpg", "quantity": 10, "unit_price": 4499.00},
        {"name": "LENOVO ThinkBook", "category_id": 4, "description": "Procesor Intel Core 7 240H oferuje imponującą wydajność w porównaniu do poprzednich generacji, dzięki 10 rdzeniom i 16 wątkom, co umożliwia płynne działanie aplikacji i multitasking. Wyposażony w pamięć podręczną 24 MB Cache, przyspiesza dostęp do danych i zwiększa efektywność przetwarzania. Maksymalna częstotliwość taktowania 5.2 GHz w trybie Turbo zapewnia wysoką responsywność w wymagających zadaniach, podczas gdy minimalna częstotliwość 1.8 GHz wspiera energooszczędność. Zintegrowany układ graficzny Intel Graphics dostarcza dobrą jakość obrazu dla codziennych zadań multimedialnych.", "Image": "/images/products/Laptopy/Laptop LENOVO ThinkBook.jpg", "quantity": 10, "unit_price": 3299.00},
        {"name": "LENOVO IdeaPad Slim 5", "category_id": 4, "description": "IdeaPad Slim 5 napędzany procesorami AMD Ryzen serii 8000 łączy moc z elegancką, ultrasmukłą obudową o grubości zaledwie 16,9 mm i wadze 1,85 kg. Konstrukcja spełniająca wymagania MIL-STD-810H sprawia, że laptop jest gotowy na codzienne wyzwania – zarówno w domu, jak i w podróży. 16-calowy wyświetlacz WUXGA 16:10 z 90% współczynnikiem powierzchni aktywnej pozwala cieszyć się rozległą przestrzenią wizualną i żywymi kolorami. To sprzęt, który inspiruje do pracy, rozrywki i odkrywania świata w pełnych barwach.", "Image": "/images/products/Laptopy/Laptop LENOVO IdeaPad Slim 5.jpg", "quantity": 10, "unit_price": 3499.00},
        {"name": "ACER Extensa 15", "category_id": 4, "description": "ACER Extensa 15 to sprzęt, który eliminuje opóźnienia i pozwala działać na pełnych obrotach. Dzięki procesorowi Intel Core i7-13620H o częstotliwości 4.9 GHz oraz Intel UHD Graphics zapewnia płynność pracy przy wymagających zadaniach. 16 GB pamięci RAM DDR5 i dysk SSD 512 GB wspierają szybkie przetwarzanie danych i bezproblemową obsługę wielu projektów jednocześnie. Niezależnie od tego, czy analizujesz dane, czy tworzysz prezentacje, ACER Extensa 15 pozwala zaoszczędzić czas i szybciej realizować cele.", "Image": "/images/products/Laptopy/Laptop ACER Extensa 15.jpg", "quantity": 10, "unit_price": 2699.00},
        {"name": "Lenovo LOQ-15", "category_id": 4, "description": "Lenovo LOQ-15 to wydajny laptop gamingowy z procesorem AMD Ryzen 5 7235HS, 16 GB RAM i szybkim dyskiem 512 GB SSD, który zapewnia płynną pracę i krótkie czasy ładowania. Karta graficzna NVIDIA GeForce RTX 3050 oraz 15,6-calowy ekran 144 Hz gwarantują dobrą wydajność w grach i płynny obraz. To solidny wybór zarówno do gamingu, jak i codziennego użytkowania", "Image": "/images/products/Laptopy/Lenovo LOQ 15.jpg", "quantity": 10, "unit_price": 2599.00},
        {"name": "MSI Katana 15 HX", "category_id": 4, "description": "MSI Katana 15 HX to laptop dla gracza, który nie uznaje kompromisów. Oferuje wysoką wydajność, świetną grafikę i zaawansowane chłodzenie. Działa szybko, wygląda stylowo i daje Ci przewagę w każdej grze. Ten model to połączenie mocy, precyzji i nowoczesnego stylu.", "Image": "/images/products/Laptopy/MSI Katana 15 HX.jpg", "quantity": 10, "unit_price": 4899.00},
        {"name": "Dell Alienware 16 Aurora", "category_id": 4, "description": "Alienware 16 Aurora - przygotuj się na niezapomniane doświadczenia w grach. Laptop został stworzony dla graczy, którzy nie akceptują kompromisów, dostarczając niezrównanej wydajności, responsywności i wciągającej rozgrywki. ", "Image": "/images/products/Laptopy/Dell Alienware 16 Aurora.jpg", "quantity": 10, "unit_price": 5999.00},
        {"name": "HP OMEN 16", "category_id": 4, "description": "Poczuj moc gier i kreatywności dzięki laptopowi HP OMEN 16, który łączy najwyższą wydajność z efektownym designem. To idealny wybór zarówno dla graczy, jak i dla profesjonalistów, którzy potrzebują niezawodnej maszyny do grafiki i projektowania. Z procesorem Intel® Core™ i9 i kartą graficzną NVIDIA GeForce RTX 5060, każda gra przybiera nowy wymiar.", "Image": "/images/products/Laptopy/HP OMEN 16.jpg", "quantity": 10, "unit_price": 5499.00},
        {"name": "Apple MacBook Air M4", "category_id": 4, "description": "MacBook Air z czipem M4 śmiga przy każdym zadaniu i zapewnia nawet 18 godzin pracy na baterii◊.Zastrzeżenia prawne. Do tego jest dostępny w czterech przepięknych kolorach, w tym w olśniewającym błękitnym. A ponieważ jest doskonale przenośny, zabierzesz go ze sobą, dokąd chcesz, żeby robić na nim, co tylko zechcesz.", "Image": "/images/products/Laptopy/Apple MacBook Air M4.jpg", "quantity": 10, "unit_price": 4359.00},
        # Stacjonarne
        {"name": "MAD DOG PurePC Edition 4", "category_id": 5, "description": "Nie musisz już wybierać między mocą a niezawodnością – MAD DOG GeForce RTX5070 PurePC Edition 4 łączy jedno i drugie. Każdy komponent został dobrany z myślą o graczach i wymagających użytkownikach, a całość przeszła szereg testów pod kątem wydajności, stabilności, bezpieczeństwa i jakości. To sprzęt, który nie tylko daje frajdę z gry, ale też spokojnie radzi sobie z codziennymi zadaniami.", "Image": "/images/products/Stacjonarne/Komputer MAD DOG PurePC Edition 4.jpg", "quantity": 10, "unit_price": 6499.00},
        {"name": "ACER Nitro N50-656", "category_id": 5, "description": "Acer Nitro N50-656 to wydajny i uniwersalny komputer stacjonarny, który sprawdzi się zarówno w codziennej pracy, jak i w bardziej wymagających zadaniach graficznych czy multimedialnych.", "Image": "/images/products/Stacjonarne/Komputer-ACER-Nitro-N50-656-1.jpg", "quantity": 10, "unit_price": 3149.00},
        {"name": "LENOVO Legion T5", "category_id": 5, "description": "LENOVO Legion T5 30AGB10 to komputer gamingowy stworzony z myślą o graczach, którzy oczekują stabilnej i płynnej pracy nawet w wymagających tytułach. Jego sercem jest procesor AMD Ryzen 5 7600 z sześcioma rdzeniami i dwunastoma wątkami, osiągający maksymalne taktowanie 5,1 GHz. Dzięki dużej pamięci podręcznej 38 MB procesor świetnie radzi sobie zarówno z rozgrywką, jak i zadaniami twórczymi – od streamingu po obróbkę materiałów wideo. Wydajność CPU sprawia, że każda akcja na ekranie jest natychmiastowa, a przełączanie pomiędzy aplikacjami nie zakłóca płynności pracy.", "Image": "/images/products/Stacjonarne/Komputer LENOVO Legion T5.jpg", "quantity": 10, "unit_price": 5699.00},
        {"name": "ASUS ExpertCenter D500ME", "category_id": 5, "description": "ASUS ExpertCenter D500ME to komputer biznesowy nowej generacji, który idealnie łączy w sobie styl, funkcjonalność i wydajność. Jego kompaktowa konstrukcja, o 37% mniejsza niż tradycyjne komputery typu tower, pozwala na maksymalne wykorzystanie przestrzeni roboczej w biurze. Dzięki smukłemu i eleganckiemu designowi urządzenie doskonale wpisuje się w każde środowisko biurowe.", "Image": "/images/products/Stacjonarne/ASUS ExpertCenter D500ME.jpg", "quantity": 10, "unit_price": 3699.00},
        {"name": "MSI MAG Infinite S3", "category_id": 5, "description": "MSI MAG Infinite S3 to potężny komputer stacjonarny zaprojektowany z myślą o fanach gier, którzy oczekują znakomitej wydajności w mainstreamowym gamingu. Dzięki nowoczesnym podzespołom i wydajnej karcie graficznej RTX 5060 Ti, umożliwia płynne granie w najnowsze tytuły nawet w najwyższych ustawieniach graficznych. Bez względu na to, czy rywalizujesz z innymi graczami, czy odkrywasz ogromne światy w grach RPG, ten komputer sprosta Twoim oczekiwaniom.", "Image": "/images/products/Stacjonarne/MSI MAG Infinite S3.jpg", "quantity": 10, "unit_price": 5999.00},
        {"name": "Dell Tower", "category_id": 5, "description": "Dell Tower to komputer stacjonarny, który łączy wysoką wydajność z kompaktową konstrukcją, idealnie sprawdzając się zarówno w biurze, jak i w domu. Zastosowane podzespoły zapewniają płynną obsługę codziennych zadań, od pracy z dokumentami po korzystanie z zaawansowanych aplikacji.", "Image": "/images/products/Stacjonarne/Dell Tower.jpg", "quantity": 10, "unit_price": 2449.00},
        {"name": "Dell Pro Micro", "category_id": 5, "description": "Dell Pro Micro korzysta z wydajnych procesorów Intel Core, które zapewniają płynną i stabilną pracę. Sprawnie obsłuży codzienne zadania biurowe, aplikacje biznesowe i systemy sprzedażowe. Niezależnie od tego, czy korzystasz z arkuszy kalkulacyjnych, przeglądasz dane czy obsługujesz klientów – możesz liczyć na szybki czas reakcji i wysoką kulturę pracy.", "Image": "/images/products/Stacjonarne/Dell Pro Micro.jpg", "quantity": 10, "unit_price": 3699.00},
        {"name": "MSI Cubi 5", "category_id": 5, "description": "MSI Cubi 5 to miniaturowy komputer PC, który oferuje Ci niespotykaną dotąd swobodę i wszechstronność. Dzięki jego niezwykłej portabilności możesz z łatwością przenosić go między domem a pracą, ciesząc się dostępem do swoich danych gdziekolwiek jesteś. Urządzenie to w pełni spełnia Twoje oczekiwania zarówno jako potężny mini PC, jak i niezawodne urządzenie do przechowywania danych.", "Image": "/images/products/Stacjonarne/MSI Cubi 5.jpg", "quantity": 10, "unit_price": 2299.00},
        {"name": "MSI Cubi NUC", "category_id": 5, "description": "MSI Cubi NUC to idealne rozwiązanie dla tych, którzy szukają kompaktowego i wydajnego komputera do codziennego użytku. Dzięki wysokiej mocy obliczeniowej procesora Intel Core 5-120U oraz dużej ilości pamięci RAM, urządzenie radzi sobie z wieloma zadaniami jednocześnie. Dodatkowo, elegancki design sprawia, że komputer doskonale wkomponuje się w każde wnętrze.", "Image": "/images/products/Stacjonarne/MSI Cubi NUC.jpg", "quantity": 10, "unit_price": 5199.00},
        # AIO
        {"name": "LENOVO IdeaCentre 3", "category_id": 6, "description": "Intel Core i5-13420H i Intel UHD Graphics zapewniają szybkie działanie i doskonałą jakość grafiki. Dysk SSD 512 GB gwarantuje błyskawiczne uruchamianie aplikacji i przechowywanie dużych plików, a 16 GB pamięci RAM DDR5 zapewnia płynność multitaskingu i efektywność pracy. Ciesz się bezproblemowym działaniem aplikacji, grami i codziennymi zadaniami dzięki połączeniu dużej mocy obliczeniowej i szybkiej pamięci.", "Image": "/images/products/AIO/Komputer LENOVO IdeaCentre 3.jpg", "quantity": 10, "unit_price": 3399.00},
        {"name": "ACER Aspire C27-2E13U", "category_id": 6, "description": "ACER Aspire C27-2E13U to komputer typu All-in-One, który upraszcza codzienność, łącząc ekran i jednostkę centralną w jednej, smukłej konstrukcji. Dzięki temu zyskujesz więcej przestrzeni roboczej bez plątaniny kabli i zbędnych urządzeń. Obudowa mieści wszystko, czego potrzeba do płynnej pracy i rozrywki – wystarczy jedno gniazdko, by uruchomić całość.", "Image": "/images/products/AIO/Komputer ACER Aspire C27-2E13U .jpg", "quantity": 10, "unit_price": 2649.00},
        {"name": "MSI Modern AM273QP", "category_id": 6, "description": "Komputer MSI Modern AM273QP AI 1UM-078EU z ekranem o przekątnej 27 cali i rozdzielczości 2560 x 1440 pikseli, wyposażony w procesor Intel Core Ultra 5-125H, pamięć RAM DDR5 o wielkości 16GB. Dysk twardy SSD o pojemności 1TB. Zainstalowany system operacyjny to Windows 11 Professional.", "Image": "/images/products/AIO/Komputer MSI Modern AM273QP.jpg", "quantity": 10, "unit_price": 4499.00},
        {"name": "ASUS A5702WVARK-BPE014W", "category_id": 6, "description": "Komputer All-in-One wyposażony jest w procesor Intel Core 7 150U o częstotliwości taktowania do 1.2 - 5.4 GHz, pamięć RAM DDR5 wielkości 16 GB oraz dysk SSD o pojemności 512 GB.", "Image": "/images/products/AIO/Komputer ASUS A5702WVARK-BPE014W.jpg", "quantity": 10, "unit_price": 3999.00},
        # Monitory
        {"name": "Samsung Odyssey  G5", "category_id": 7, "description": "Monitor Samsung Odyssey G5 model gamingowy z matrycą Fast IPS i rozdzielczością QHD, zapewniający ostry i szczegółowy obraz. Częstotliwość odświeżania 180 Hz oraz czas reakcji 1 ms gwarantują płynną rozgrywkę bez opóźnień. Obsługa AMD FreeSync i NVIDIA G-Sync Compatible eliminuje tearing i poprawia komfort grania.", "Image": "/images/products/Monitory/Samsung Odyssey G5.jpg", "quantity": 10, "unit_price": 749.00},
        {"name": "Lenovo Legion 27Q -10", "category_id": 7, "description": "Ciesz się płynną akcją i głębokim zanurzeniem w rozgrywkę dzięki częstotliwości odświeżania 240 Hz, czasowi reakcji 0,5 ms MPRT (Moving Picture Response Time) oraz kompatybilności z NVIDIA® G‑SYNC®. Duży ekran 27 w rozdzielczości QHD (Quad High Definition) zapewnia wyjątkową ostrość i klarowność obrazu przez co monitor Legion 27Q‑10 idealnie nadaje się do szybkich, intensywnych gier.", "Image": "/images/products/Monitory/Lenovo Legion 27Q -10.jpg", "quantity": 10, "unit_price": 799.00},
        {"name": "MSI PRO MP242L", "category_id": 7, "description": "Monitor MSI PRO MP242L to idealne rozwiązanie dla osób pracujących zdalnie oraz dla tych, którzy doceniają wysoką jakość obrazu w domowym biurze. Dzięki matrycy IPS o przekątnej 23,8 cala i rozdzielczości Full HD, każde zadanie staje się przyjemnością. Dodatkowo, dzięki matowym właściwościom ekranu oraz technologii ochrony oczu, możesz cieszyć się wygodną pracą przez wiele godzin.", "Image": "/images/products/Monitory/MSI PRO MP242L.jpg", "quantity": 10, "unit_price": 269.00},
        {"name": "LG UltraGear 27GS75Q-B", "category_id": 7, "description": "LG UltraGear 27GS75Q-B to 27-calowy monitor gamingowy z matrycą IPS i rozdzielczością QHD, oferujący bardzo ostry i szczegółowy obraz. Wysoka częstotliwość odświeżania 180 Hz oraz czas reakcji 1 ms zapewniają płynną i dynamiczną rozgrywkę. Obsługa AMD FreeSync i NVIDIA G-Sync Compatible eliminuje zacięcia i rozrywanie obrazu.", "Image": "/images/products/Monitory/LG UltraGear 27GS75Q-B.jpg", "quantity": 10, "unit_price": 799.00},
        {"name": "Dell Alienware AW2725DM", "category_id": 7, "description": "Dell Alienware AW2725DM to 27-calowy monitor gamingowy QHD, który został stworzony z myślą o graczach oczekujących najwyższej jakości obrazu i pełnej płynności. Dzięki panelowi Fast IPS i rozdzielczości 2560 × 1440 każdy szczegół na ekranie jest wyraźny i realistyczny. To idealny wybór do dynamicznych tytułów i gier z otwartym światem, gdzie liczy się zarówno szybkość reakcji, jak i dokładność obrazu.", "Image": "/images/products/Monitory/Lenovo Legion 27Q -10.jpg", "quantity": 10, "unit_price": 749.00},
        {"name": "MSI MAG 341CQP", "category_id": 7, "description": "Zyskaj dodatkową przewagę nad przeciwnikiem za sprawą gamingowego monitora MSI MAG 341CQP. Daj się porwać niezwykłej dynamice i wiernie oddanym kolorom. Zyskaj też dodatkowy oręż w walce w postaci błyskawicznej reakcji matrycy. Jej szybkość wyświetlania sprawia, że obraz jest płynniejszy, co da Ci więcej czasu na reakcję i umożliwi dokładniejsze celowanie.", "Image": "/images/products/Monitory/MSI MAG 341CQP QD-OLED.jpg", "quantity": 10, "unit_price": 2799.00},
        {"name": "LG UltraGear 27GX700A-B Tandem", "category_id": 7, "description": "Monitor LG UltraGear 27GX700A-B WOLED to idealne rozwiązanie dla graczy, którzy oczekują najwyższej jakości obrazu oraz szybkości reakcji. Dzięki technologii WOLED, każdy detal jest wyraźny, a kolory nasycone, co przeniesie Cię do serca akcji. Wysoka częstotliwość odświeżania oraz krótki czas reakcji sprawiają, że każda gra staje się płynna i przyjemna", "Image": "/images/products/Monitory/LG UltraGear 27GX700A-B Tandem.jpg", "quantity": 10, "unit_price": 2699.00},
        {"name": "Acer Nitro KG241YX3", "category_id": 7, "description": "Acer Nitro KG241YX3 to monitor stworzony z myślą o wymagających graczach, którzy oczekują najwyższej jakości obrazu i płynności rozgrywki. Dzięki częstotliwości odświeżania wynoszącej aż 200 Hz oraz czasowi reakcji zaledwie 0,5 ms, każde ujęcie będzie niezwykle ostre i przejrzyste. Przygotuj się na wciągające doświadczenie wizualne z technologią FreeSync™ Premium, która eliminuję zacięcia i przerywania obrazu.", "Image": "/images/products/Monitory/Acer Nitro KG241YX3.jpg", "quantity": 10, "unit_price": 389.00},
        {"name": "MSI MAG 244C", "category_id": 7, "description": "MSI MAG 244C to monitor gamingowy, który zapewnia wyjątkową płynność obrazu i pełne zanurzenie w rozgrywce. Zakrzywiony ekran 1500R dostosowuje się do naturalnego pola widzenia, co poprawia komfort i immersję. Częstotliwość odświeżania 180 Hz oraz czas reakcji 1 ms (MPRT) gwarantują błyskawiczną reakcję ekranu na każdą akcję.", "Image": "/images/products/Monitory/MSI MAG 244C.jpg", "quantity": 10, "unit_price": 619.00},
         # Myszy
        {"name": "Logitech M650", "category_id": 8, "description": "Uzyskaj inteligentne przewijanie, wyższy komfort i większą wydajność. Mysz M650 kółko SmartWheel, które zapewnia precyzję lub szybkość w momencie, gdy tego potrzebujesz. Prezentowany model charakteryzuje się standardowym rozmiarem i jest przeznaczony dla osób praworęcznych. ", "Image": "/images/products/Myszy/Logitech M650 Grafitowa.jpg", "quantity": 10, "unit_price": 169.00},
        {"name": "Logitech LIFT", "category_id": 8, "description": "Nauka o ergonomii stanowi integralną część procesu tworzenia nowej myszy przez projektantów i inżynierów Logitech. Myszy z serii Ergo zapewniają bardziej naturalną postawę, doskonałe właściwości ergonomiczne, mniejsze obciążenie ruchowe lub mięśniowe oraz efektowne kształty.", "Image": "/images/products/Myszy/Logitech LIFT.jpg", "quantity": 10, "unit_price": 269.00},
        {"name": "Logitech M705 Marathon", "category_id": 8, "description": "Zapomnij o niewygodach, kosztach i trudach dla środowiska naturalnego związanych z częstymi zmianami baterii. Trzy lata zasilania. Wystarczy podłączyć niewielki odbiornik Logitech Unifying i zapomnieć o nim. Możesz dodać nawet więcej urządzeń. Podłącz. Zapomnij. Dodaj kolejne. Superszybkie przewijanie. Po jednym ruchu kółka już nigdy nie wrócisz do normalnego kółka przewijania.", "Image": "/images/products/Myszy/Logitech M705 Marathon.jpg", "quantity": 10, "unit_price": 159.00},
        {"name": "SteelSeries Aerox 3", "category_id": 8, "description": "Odnieś zwycięstwo z niezwykle lekką i zoptymalizowana pod kątem najszybszych przesunięć myszką SteelSeries Aerox 3 Wireless. Akcesorium może działać w dwóch trybach: za pomocą technologii Bluetooth lub dołączonego do zestawu odbiornika, co pozwoli na dopasowanie myszy do Twoich potrzeb i preferencji.", "Image": "/images/products/Myszy/SteelSeries Aerox 3.jpg", "quantity": 10, "unit_price": 349.00},
        {"name": "Logitech G502 HERO", "category_id": 8, "description": "Myszka gamingowa Logitech G502 HERO to potężna mysz do gier, która oferuje cały zestaw funkcji dla graczy. Zaawansowany czujnik optyczny zapewniający maksymalną precyzję śledzenia ruchów, podświetlenie RGB z możliwością dostosowania, niestandardowe profile gier i ciężarki z możliwością zmiany pozycji. To wszystko sprawia, że Mysz do gier G502 HERO jest odpowiednim narzędziem, aby podjąć wyzwanie.", "Image": "/images/products/Myszy/Logitech G502 HERO.jpg", "quantity": 10, "unit_price": 195.00},
        {"name": "SteelSeries Aerox 5", "category_id": 8, "description": "Aerox 5 to ultralekka i ergonomiczna mysz do gier, która waży zaledwie 66 g. Wykonana w najnowocześniejszej technologii zapewnia większą zwinność i wszechstronność. Jest zoptymalizowana pod kątem najszybszych przesunięć. Dzięki czemu możesz pokonać konkurencję pociągnięciem spustu. Ślizgacze teflonowe gwarantują bardziej płynne przesunięcia i większa kontrola dla super szybkich ruchów myszy. ", "Image": "/images/products/Myszy/SteelSeries Aerox 5.jpg", "quantity": 10, "unit_price": 269.00},
        {"name": "SteelSeries Rival 3 Gen 2", "category_id": 8, "description": "SteelSeries Rival 3 Gen 2 to mysz zaprojektowana dla graczy, którzy liczą na szybkość, precyzję i trwałość. Ultraszybka reakcja kliknięcia na poziomie 1,35 ms sprawia, że każda akcja w grze jest błyskawiczna. Sensor TrueMove Core 8500 DPI umożliwia perfekcyjne śledzenie ruchu bez opóźnień. Trwałe przełączniki i podświetlenie RGB dopełniają całości, tworząc sprzęt gotowy na każdą walkę. Jeśli chcesz zyskać przewagę i wyraźnie ją poczuć – to mysz stworzona dla Ciebie.", "Image": "/images/products/Myszy/SteelSeries Rival 3 Gen 2.jpg", "quantity": 10, "unit_price": 109.00},
        # Klawiatury
        {"name": "Silver Monkey K90m", "category_id": 9, "description": "Silver Monkey K90m połączysz bezprzewodowo z trzema urządzeniami, a dedykowane przyciski przełączą Cię między nimi w mgnieniu oka. Używaj ulubionych skrótów i steruj multimediami niezależnie od systemu, na którym pracujesz. Dzięki kompaktowej konstrukcji i przemyślanemu układowi klawiszy każdą z tych funkcji masz teraz w zasięgu ręki.", "Image": "/images/products/Klawiatury/Silver Monkey K90m.jpg", "quantity": 10, "unit_price": 89.00},
        {"name": "Silver Monkey Alu", "category_id": 9, "description": "Klawiatura Silver Monkey Alu Keys Premium Backlight Black to idealne rozwiązanie dla każdego, kto ceni wygodę i styl. Model ten oferuje niski profil klawiszy, dzięki czemu praca na niej jest komfortowa i przyjemna. Aluminiowa konstrukcja nadaje jej niepowtarzalnego wyglądu i świadczy o wysokiej jakości wykonania. Ponadto wbudowane podświetlenie oraz wskaźnik naładowania baterii gwarantują funkcjonalność w każdych warunkach.", "Image": "/images/products/Klawiatury/Silver Monkey Alu.jpg", "quantity": 10, "unit_price": 259.00},
        {"name": "Rampage Quell Pro", "category_id": 9, "description": "Rampage Quell Pro to zaawansowana mechaniczna klawiatura stworzona z myślą o profesjonalnych graczach oraz użytkownikach domowych. Jej ochrona przed zatarciem i wielofunkcyjne możliwości sprawiają, że jest idealnym narzędziem zarówno do gier, jak i do codziennej pracy. Dzięki zastosowaniu technologii Hot-Swap, zmiana przełączników stała się niezwykle prosta, a przy tym ergonomiczną przyjemnością.", "Image": "/images/products/Klawiatury/Rampage Quell Pro.jpg", "quantity": 10, "unit_price": 269.00},
        {"name": "ENDORFY Thock V2 TKL", "category_id": 9, "description": "Bezprzewodowa klawiatura ENDORFY Thock V2 TKL Wireless to idealny wybór dla zapalonych graczy, którzy cenią sobie wygodę oraz precyzję. Dzięki mechanizmom ENDORFY Yellow, możesz cieszyć się szybkim i komfortowym pisaniem. Jej elegancki design w kolorze szarym oraz wielokolorowe podświetlenie RGB sprawią, że Twoje stanowisko gamingowe zyska nowy wymiar estetyki.", "Image": "/images/products/Klawiatury/ENDORFY Thock V2 TKL.jpg", "quantity": 10, "unit_price": 319.00},
        {"name": "Dell KB216-B QuietKey", "category_id": 9, "description": "Dell KB216-B QuietKey to wyjątkowa klawiatura pod względem prostoty, jak i wygody użytkowania. Zapewnij sobie odpowiedni komfort pracy w biurze lub w domowym zaciszu. Elegancka konstrukcja świetnie wpasuje się w przestrzeń na Twoim biurku. Zadbaj o odpowiednią ergonomię podczas spędzania długich godzin przed komputerem. Wybierz Dell KB216-B QuietKey i zwiększ swoją produktywność.", "Image": "/images/products/Klawiatury/Dell KB216-B QuietKey.jpg", "quantity": 10, "unit_price": 65.00},
        {"name": "Redragon Antonium PRO", "category_id": 9, "description": "Klawiatura Redragon Antonium PRO K728AK-RGB-PRO to wyjątkowy wybór dla entuzjastów gier oraz pracy w domowym biurze. Dzięki mechanicznych przełącznikom Redragon Lion L, oferuje nie tylko precyzyjne kliknięcia, ale także dużą wytrzymałość. Wysokiej jakości podświetlenie RGB sprawia, że każde nałożenie na klawisze dodaje charakteru każdemu stanowisku pracy czy gry.", "Image": "/images/products/Klawiatury/Redragon Antonium PRO.jpg", "quantity": 10, "unit_price": 259.00},
        {"name": "Redragon StarBlade", "category_id": 9, "description": "Redragon StarBlade to idealne połączenie komfortu i personalizacji. Dzięki technologii Gasket Mount, każdy klawisz działa cicho i miękko, zapewniając wygodę podczas długotrwałego użytkowania. Funkcja hot-swap pozwala łatwo wymieniać przełączniki bez lutowania, dopasowując klawiaturę do Twoich potrzeb. Programowalne makra i zaawansowane podświetlenie RGB z możliwością pełnej personalizacji dodają funkcjonalności, a jasnoniebiesko-biała obudowa nadaje jej nowoczesny wygląd.", "Image": "/images/products/Klawiatury/Redragon StarBlade.jpg", "quantity": 10, "unit_price": 179.00},
        {"name": "Dell Smartcard Keyboard", "category_id": 9, "description": "Odpowiednio zaprojektowana klawiatura potrafi odmienić pracę w czystą przyjemność. Właśnie to zyskasz, wybierając Dell Smartcard KB813. Szybka reakcja oraz cicha praca klawiszy zapewnią Ci wyjątkowy komfort podczas korzystania z komputera. Wytrzymała konstrukcja i trwałe nadruki na przyciskach pozwolą Ci cieszyć się z zakupionego sprzętu przez długo.", "Image": "/images/products/Klawiatury/Dell Smartcard Keyboard.jpg", "quantity": 10, "unit_price": 199.00},
        # Głośniki
        {"name": "Creative 2.0 Pebble", "category_id": 10, "description": "Zainspirowany japońskim skalnym ogrodem zen, zaokrąglony i gładki kształt Creative Pebble, sprawia, że ten system głośników 2.0 swoim wyglądem doskonale pasuje do wystroju nowoczesnego domu i biura. Ulepszające brzmienie muzyki przetworniki skierowane pod kątem 45 stopni oraz wygodne zasilanie za pomocą pojedynczego kabla USB.", "Image": "/images/products/Głośniki/Creative 2.0 Pebble.jpg", "quantity": 10, "unit_price": 79.00},
        {"name": "Edifier R1855DB", "category_id": 10, "description": "Kompaktowe głośniki Edifier 2.0 R1855DB przywracają tradycyjne wzornictwo i łączą je z najnowszymi technologiami. Edifier R1855DB to system głośników aktywnych 2.0, ustawionych pod kątem 10 stopni w obudowie MDF, aby precyzyjnie kierować dźwięk bezpośrednio w Twoją stronę. To rozwiązanie pozwala na wyraźne odzwierciedlenie dźwięku przy jednoczesnej redukcji zniekształceń. ", "Image": "/images/products/Głośniki/Edifier R1855DB.jpg", "quantity": 10, "unit_price": 589.00},
        {"name": "Creative Sound Blaster GS3", "category_id": 10, "description": "Kompaktowy głośnik Sound Blaster GS3 to krok naprzód w stosunku do wbudowanych głośników komputera stacjonarnego lub laptopa. Oferuje on wciągającą scenę dźwiękową z wyraźnymi basami, które nie ustępują jego rozmiarom. Twoje wrażenia dźwiękowe ożyją również dzięki technologii SuperWide™ - zaprojektowanej z myślą o najlepszych wrażeniach podczas oglądania filmów i grania.", "Image": "/images/products/Głośniki/Creative Sound Blaster GS3.jpg", "quantity": 10, "unit_price": 199.00},
        {"name": "Edifier 2.0 R1100", "category_id": 10, "description": "Głośniki Edifier R1100 to propozycja dla wszystkich, którzy szukają głośników zapewniających wysoką jakość dźwięku w atrakcyjnej cenie. Będą idealne zarówno dla nastolatków, jak i dla osób, które po prostu lubią słuchać muzyki i cenią sobie czystość dźwięku.", "Image": "/images/products/Głośniki/Edifier 2.0 R1100.jpg", "quantity": 10, "unit_price": 289.00},
        {"name": "Edifier 2.1 M1360", "category_id": 10, "description": "Głośniki Edifier M1360 to nowoczesny i elegancki zestaw w rozsądnej cenie. Jest to system gwarantujący wysoką jakość odtwarzanego dźwięku. Głośniki komputerowe Edifier sprawdzą się zarówno podłączone do komputera, jak i we współpracy z innymi odtwarzaczami muzyki.", "Image": "/images/products/Głośniki/Edifier 2.1 M1360.jpg", "quantity": 10, "unit_price": 179.00},
        {"name": "Edifier Głośniki 2.0 HECATE G2000", "category_id": 10, "description": "Edifier G2000 to uniwersalny sprzęt, który oferuje szereg różnych zastosowań. Układ dźwiękowy jest wykonany przy użyciu precyzyjnego algorytmu, odpowiadającego za dostosowanie ustawień EQ. Bezprzewodowe głośniki z systemem Stereo Subwoofer służą do odtwarzania dźwięków o wyjątkowo niskich częstotliwościach.", "Image": "/images/products/Głośniki/Edifier Głośniki 2.0 HECATE G2000.jpg", "quantity": 10, "unit_price": 261.00},
        {"name": "Creative Pebble Plus", "category_id": 10, "description": "Pomimo swoich niewielkich rozmiarów, Creative Pebble Plus to głośniki o niezwykle dużej mocy. Proste, wykonane z dbałością o szczegóły urządzenie idealnie łączy w sobie minimalizm i wysokie osiągi, wtapiając się w miejsce użytkowania. Co ważne, wymagają do pracy wyłącznie podłączenia do portu USB 2.0. A jeżeli zechcesz skorzystać z trybu High Gain i pełnej mocy wyjściowej 8W RMS, podłącz je do zewnętrznego zasilacza 5V/2A.", "Image": "/images/products/Głośniki/Creative Pebble Plus.jpg", "quantity": 10, "unit_price": 129.00},
        # Słuchawki
        {"name": "JBL Tune 520BT", "category_id": 11, "description": "Słuchawki JBL Tune 520BT w czarnym kolorze oferują legendarny dźwięk JBL Pure Bass, znany z największych scen i sal koncertowych na całym świecie. Ta technologia zapewnia głębokie, potężne basy, które w pełni oddają emocje i energię Twojej ulubionej muzyki. Niezależnie od tego, czy słuchasz rocka, hip-hopu czy elektroniki, słuchawki JBL Tune 520BT zapewniają brzmienie, które przeniesie Cię w sam środek muzycznego doświadczenia.", "Image": "/images/products/Słuchawki/JBL Tune 520BT.jpg", "quantity": 10, "unit_price": 139.00},
        {"name": "JBL Tour One M3 ANC", "category_id": 11, "description": "Odkryj nowe możliwości bezprzewodowego audio dzięki słuchawkom JBL Tour One M3 ANC. Zapewniają one nieskomplikowaną łączność i niezrównaną jakość dźwięku, idealne do słuchania muzyki, oglądania filmów oraz prowadzenia rozmów. Ich nowoczesny design łączy elegancję z funkcjonalnością, co czyni je idealnym wyborem zarówno do użytku codziennego, jak i podczas podróży.", "Image": "/images/products/Słuchawki/JBL Tour One M3 ANC.jpg", "quantity": 10, "unit_price": 1089.00},
        {"name": "Fresh N Rebel Clam Fuse ANC True", "category_id": 11, "description": "Słuchawki bezprzewodowe Fresh N Rebel Clam Fuse w niebieskim kolorze to kwintesencja muzycznego doświadczenia, które łączy w sobie zbalansowany dźwięk idealny dla każdego gatunku muzycznego z zaawansowaną technologią hybrydowej aktywnej redukcji szumów (ANC). Pozwoli Ci to cieszyć się ulubionymi utworami bez zakłóceń zewnętrznych. Zyskasz też możliwość szybkiego przejścia do trybu dźwięków otoczenia dla bezpiecznej podróży.", "Image": "/images/products/Słuchawki/Fresh N Rebel Clam Fuse ANC True.jpg", "quantity": 10, "unit_price": 279.00},
        {"name": "Fresh N Rebel Clam Blaze ENC", "category_id": 11, "description": "Nauszne słuchawki bezprzewodowe Fresh N Rebel Clam Blaze we fioletowym kolorze łączą w sobie wysoką jakość dźwięku z atrakcyjnym, minimalistycznym designem. Dzięki intuicyjnemu interfejsowi, w tym fizycznym przyciskom sterowania i pokrętłu regulacji głośności, sterowanie muzyką i połączeniami telefonicznymi jest niezwykle proste i wygodne. Słuchawki oferują bogate i zbalansowane brzmienie, które doskonale sprawdza się przy różnych stylach muzycznych.", "Image": "/images/products/Słuchawki/Fresh N Rebel Clam Blaze ENC.jpg", "quantity": 10, "unit_price": 279.00},
        {"name": "Sony MDR-ZX110", "category_id": 11, "description": "Oferta dotyczy słuchawek Sony MDR-ZX110B w kolorze czarnym przedstawionych na poniższym zdjęciu. Na pozostałych grafikach poglądowych mogą wystąpić różnice kolorystyczne, gdyż mają one jedynie ukazać poszczególne funkcjonalności produktu.", "Image": "/images/products/Słuchawki/Sony MDR-ZX110.jpg", "quantity": 10, "unit_price": 60.00},
        {"name": "JBL T500", "category_id": 11, "description": "Od teraz nie musisz już zdejmować słuchawek nauszny JBL T500, a dodatkowo masz wolne ręce, gdy telefonujesz. Przycisk kontrolny oraz wbudowany mikrofon zapewniają sprawne przejście w tryb rozmowy bez konieczności trzymania telefonu. Słuchawki T500 umożliwiają także łączenie się z Siri lub Google Now bez sięgania po urządzenie mobilne, do którego są podłączone. Aktywuj asystenta głosowaego, korzystając z przycisku na pilocie i korzystaj jeszcze wygodniej.", "Image": "/images/products/Słuchawki/JBL T500.jpg", "quantity": 10, "unit_price": 99.00},
        {"name": "Sony MDR-MV1", "category_id": 11, "description": "Słuchawki Studio Monitor MDR-MV1 z otwartym tyłem umożliwiają uzyskanie przestrzennego dźwięku stereo w szerokim zakresie częstotliwości i realistycznej sceny dźwiękowej. Dzięki neutralnej charakterystyce akustycznej i wysokiej rozdzielczości wszystkie dźwięki są odtwarzane z dużą wiernością. Słuchawek tych możesz komfortowo używać przez wiele godzin pracy. Są lekkie i wygodne.", "Image": "/images/products/Słuchawki/Sony MDR-MV1.jpg", "quantity": 10, "unit_price": 2079.00},
        {"name": "Sony H3 INZONE", "category_id": 11, "description": "Gamingowy zestaw słuchawkowy Sony H3 INZONE został wyposażony w technologię 360 Spatial Sound for Gaming. Pozwoli ona usłyszeć Twoich przeciwników, zanim oni zobaczą Ciebie. Szerokie i miękkie poduszki pałąka oraz gładkie nylonowe nauszniki zapewnią Ci pełen komfort podczas grania w ulubione tytuły. ", "Image": "/images/products/Słuchawki/Sony H3 INZONE.jpg", "quantity": 10, "unit_price": 299.00},
    ]

    for data in products:
        istnieje = Products.query.filter_by(name=data["name"]).first()
        if not istnieje:
            new_product = Products(name=data["name"], category_id=data["category_id"], description=data["description"], image=data["Image"], unit_price=data["unit_price"], quantity=data["quantity"])
            db.session.add(new_product)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych produktów.")

def seed_attribute_weights():
    added_count = 0
    print("Dodawanie wag atrybutów...")
    attributes_weights = [
        # wagi dla Laptopów: procesor, RAM, Karta graficzna, Dysk, System operacyjny, Wifi, Przekątna ekranu, Rozdzielczość ekranu, Częstotliwość odświeżania, Kolor, Producent 
        # istotna mobilnosć i wydajność
        {"attribute_id": 1, "category_id": 4, "weight": 0.20},
        {"attribute_id": 2, "category_id": 4, "weight": 0.20},
        {"attribute_id": 3, "category_id": 4, "weight": 0.15},
        {"attribute_id": 4, "category_id": 4, "weight": 0.15},
        {"attribute_id": 5, "category_id": 4, "weight": 0.05},
        {"attribute_id": 6, "category_id": 4, "weight": 0.05},
        {"attribute_id": 7, "category_id": 4, "weight": 0.05},
        {"attribute_id": 8, "category_id": 4, "weight": 0.05},
        {"attribute_id": 9, "category_id": 4, "weight": 0.05},
        {"attribute_id": 12, "category_id": 4, "weight": 0.03},
        {"attribute_id": 13, "category_id": 4, "weight": 0.02},

        # wagi dla Stacjonarnych: procesor, RAM, Karta graficzna, Dysk, System operacyjny, Wifi, Kolor, Producent 
        # njważniejszy jest performance
        {"attribute_id": 1, "category_id": 5, "weight": 0.23},
        {"attribute_id": 2, "category_id": 5, "weight": 0.20},
        {"attribute_id": 3, "category_id": 5, "weight": 0.23},
        {"attribute_id": 4, "category_id": 5, "weight": 0.18},
        {"attribute_id": 5, "category_id": 5, "weight": 0.05},
        {"attribute_id": 6, "category_id": 5, "weight": 0.06},
        {"attribute_id": 12, "category_id": 5, "weight": 0.03},
        {"attribute_id": 13, "category_id": 5, "weight": 0.02},

        # wagi dla AIO: procesor, RAM, Karta graficzna, Dysk, System operacyjny, Wifi, Przekątna ekranu, Rozdzielczość ekranu, Częstotliwość odświeżania, Kolor, Producent  
        # urządzenia są traktowane jako "technologiczny mebel", zazwyczaj nie do gamingu
        {"attribute_id": 1, "category_id": 6, "weight": 0.20},
        {"attribute_id": 2, "category_id": 6, "weight": 0.20},
        {"attribute_id": 3, "category_id": 6, "weight": 0.12},
        {"attribute_id": 4, "category_id": 6, "weight": 0.15},
        {"attribute_id": 5, "category_id": 6, "weight": 0.05},
        {"attribute_id": 6, "category_id": 6, "weight": 0.05},
        {"attribute_id": 7, "category_id": 6, "weight": 0.07},
        {"attribute_id": 8, "category_id": 6, "weight": 0.07},
        {"attribute_id": 9, "category_id": 6, "weight": 0.04},
        {"attribute_id": 12, "category_id": 6, "weight": 0.03},
        {"attribute_id": 13, "category_id": 6, "weight": 0.02},

        # wagi dla Monitorów: Przekątna ekranu, Rozdzielczość ekranu, Częstotliwość odświeżania, Klasa energetyczna, Typ matrycy, kolor, marka
        # najważniejsza jakość obrazu
        {"attribute_id": 7, "category_id": 7, "weight": 0.18},
        {"attribute_id": 8, "category_id": 7, "weight": 0.22},
        {"attribute_id": 9, "category_id": 7, "weight": 0.20},
        {"attribute_id": 10, "category_id": 7, "weight": 0.08},
        {"attribute_id": 11, "category_id": 7, "weight": 0.20},
        {"attribute_id": 12, "category_id": 7, "weight": 0.05},
        {"attribute_id": 13, "category_id": 7, "weight": 0.07},

        # wagi dla myszy: kolor, producent, Rodzaj, typ podłączenia, typ, długośc przewodu, Czułość, Zasięg
        # najważniejsza precyzja i typ
        {"attribute_id": 12, "category_id": 8, "weight": 0.04},
        {"attribute_id": 13, "category_id": 8, "weight": 0.06},
        {"attribute_id": 14, "category_id": 8, "weight": 0.18},
        {"attribute_id": 15, "category_id": 8, "weight": 0.12},
        {"attribute_id": 16, "category_id": 8, "weight": 0.17},
        {"attribute_id": 17, "category_id": 8, "weight": 0.08},
        {"attribute_id": 19, "category_id": 8, "weight": 0.25},
        {"attribute_id": 20, "category_id": 8, "weight": 0.10},
        
        # wagi dla klawiatur: kolor, producent, rodzaj, typ podłączenia, typ, długośc przewodu
        # najważniejsze jest typ i rodzaj
        {"attribute_id": 12, "category_id": 9, "weight": 0.10},
        {"attribute_id": 13, "category_id": 9, "weight": 0.10},
        {"attribute_id": 14, "category_id": 9, "weight": 0.25},
        {"attribute_id": 15, "category_id": 9, "weight": 0.15},
        {"attribute_id": 16, "category_id": 9, "weight": 0.30},
        {"attribute_id": 17, "category_id": 9, "weight": 0.10},

        # wagi dla głośników: kolor, producent, rodzaj, typ podłączenia, długośc przewodu, pasmo przenoszenia
        # najważniejsze jest pasmo przenoszenia
        {"attribute_id": 12, "category_id": 10, "weight": 0.05},
        {"attribute_id": 13, "category_id": 10, "weight": 0.07},
        {"attribute_id": 14, "category_id": 10, "weight": 0.25},
        {"attribute_id": 15, "category_id": 10, "weight": 0.20},
        {"attribute_id": 17, "category_id": 10, "weight": 0.08},
        {"attribute_id": 18, "category_id": 10, "weight": 0.35},

        # wagi dla suchawek: kolor, producent, rodzaj, typ podłączenia, długośc przewodu, pasmo przenoszenia , czułość
        # najważniejsze jest pasmo przenosenia i czułość
        {"attribute_id": 12, "category_id": 11, "weight": 0.05},
        {"attribute_id": 13, "category_id": 11, "weight": 0.10},
        {"attribute_id": 14, "category_id": 11, "weight": 0.15},
        {"attribute_id": 15, "category_id": 11, "weight": 0.10},
        {"attribute_id": 17, "category_id": 11, "weight": 0.05},
        {"attribute_id": 18, "category_id": 11, "weight": 0.30},
        {"attribute_id": 19, "category_id": 11, "weight": 0.25},
       
    ]

    for data in attributes_weights:
        istnieje = AttributeWeights.query.filter_by(attribute_id=data["attribute_id"], category_id=data["category_id"]).first()
        if not istnieje:
            new_attribute_weight = AttributeWeights(attribute_id=data["attribute_id"], category_id=data["category_id"], weight=data["weight"])
            db.session.add(new_attribute_weight)
            added_count += 1
    db.session.commit()
    print(f"Ustawiono {added_count} nowych wag atrybutów.")

def seed_delivery_methods(): ## nie używane obecnie
    added_count = 0
    print("Dodawanie metod dostawy...")
    delivery_methods = [
        {"name": "Kurier", "fee": 9.99, "estimated_delivery_days": 2},
        {"name": "Odbiór w sklapie", "fee": 0.00, "estimated_delivery_days": 0},
    ]

    for data in delivery_methods:
        istnieje = DeliveryMethods.query.filter_by(name=data["name"]).first()
        if not istnieje:
            new_delivery_method = DeliveryMethods(name=data["name"], fee=data["fee"], estimated_delivery_days=data["estimated_delivery_days"])
            db.session.add(new_delivery_method)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych metod dostawy.")

def seed_payment_methods(): ## nie używane obecnie
    added_count = 0
    print("Dodawanie metod płatności...")
    payment_methods = [
        {"name": "Apple Pay", "Image": "/images/Payments/Apple_Pay_logo.png", "fee": 0.00},
        {"name": "Google Pay", "Image": "/images/Payments/Google_Pay_Logo.svg", "fee": 0.00},
        {"name": "Karta płatnicza online", "Image": "/images/Payments/visa_MasterCard.png", "fee": 0.00},
        {"name": "Przelew tradycyjny", "Image": "/images/Payments/Przelew_tradycyjny.png", "fee": 0.00}
    ]

    for data in payment_methods:
        istnieje = PaymentMethods.query.filter_by(name=data["name"]).first()
        if not istnieje:
            new_payment_method = PaymentMethods(name=data["name"], image=data["Image"], fee=data["fee"])
            db.session.add(new_payment_method)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych metod płatności.")  

def seed_promotions():
    added_count = 0
    print("Dodawanie promocji...")
    promotions = [
        {"name": "Wietrzenie magazynów", "discount_percent": 25, "start_date": "2025-11-25T00:00:00", "end_date": "2026-11-25T23:59:59"},
    ]

    for data in promotions:
        istnieje = Promotions.query.filter_by(name=data["name"]).first()
        if not istnieje:
            new_promotion = Promotions(name=data["name"], discount_percent=data["discount_percent"], start_date=data["start_date"], end_date=data["end_date"])
            db.session.add(new_promotion)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych promocji.")

def seed_product_in_promoton():
    added_count = 0
    print("Dodawanie produktów do promocji...")
    
    products_in_promotion = [
        {"product_id": 22, "promotion_id": 1},
        {"product_id": 28, "promotion_id": 1},
        {"product_id": 33, "promotion_id": 1},
        {"product_id": 16, "promotion_id": 1},
        {"product_id": 41, "promotion_id": 1},
        {"product_id": 7, "promotion_id": 1},
        {"product_id": 55, "promotion_id": 1},
        {"product_id": 35, "promotion_id": 1},
        {"product_id": 3, "promotion_id": 1},
    ]

    for product_data in products_in_promotion:
        product = Products.query.filter_by(id=product_data["product_id"]).first()
        promotion = Promotions.query.filter_by(id=product_data["promotion_id"]).first()
        if product and promotion:
            istnieje = ProductPromotions.query.filter_by(product_id=product.id, promotion_id=promotion.id).first()
            if not istnieje:
                new_product_in_promotion = ProductPromotions(product_id=product.id, promotion_id=promotion.id)
                db.session.add(new_product_in_promotion)
                added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} produktów do promocji.")

def seed_transacion_products(): ## nie używane obecnie
    added_count = 0
    print("Dodawanie produktów do transakcji...")

    transaction_products = [ 
        {"transaction_id": 1, "product_id": 4, "quantity": 1, "unit_price": 2699.00},
        {"transaction_id": 1, "product_id": 6, "quantity": 1, "unit_price": 4899.00}
    ]
    for data in transaction_products:
        istnieje = TransactionProducts.query.filter_by(transaction_id=data["transaction_id"], product_id=data["product_id"]).first()
        if not istnieje:
            new_transaction_product = TransactionProducts(transaction_id=data["transaction_id"], product_id=data["product_id"], quantity=data["quantity"], unit_price=data["unit_price"])
            db.session.add(new_transaction_product)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} produktów do transakcji.")

def seed_transactions(): ## nie używane obecnie
    added_count = 0
    print("Dodawanie transakcji...")
    transactions = [
        {"user_id": 1, "total_transaction_value": 7607.99, "billing_address_id": 46, "shipping_address_id": 46, "status": TransactionStatus.Pending, "delivery_method_id": 1, "payment_method_id": 1, "delivery_deadline": "2026-02-03", "created_at": "2026-02-01 23:39:25.202989+01", "updated_at": "2026-02-01 23:39:25.202989+01", "billing_address_data": {}, "shipping_address_data": {}},
    ]

    for data in transactions:
        istnieje = Transactions.query.filter_by(user_id=data["user_id"], created_at=data["created_at"]).first()
        if not istnieje:
            new_transaction = Transactions(user_id=data["user_id"], total_transaction_value=data["total_amount"], billing_address_id=data["billing_address_id"], shipping_address_id=data["shipping_address_id"], status=data["status"], delivery_method_id=data["delivery_method_id"], payment_method_id=data["payment_method_id"], delivery_deadline=data["delivery_deadline"], created_at=data["created_at"], updated_at=data["updated_at"], billing_address_data=data["billing_address_data"], shipping_address_data=data["shipping_address_data"])
            db.session.add(new_transaction)
            added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} nowych transakcji.")

def seed_product_interactions():
    added_count = 0
    print("Dodawanie interakcji z produktami...")
    
    products_in_promotion = [
        {"user_id": None, "product_id": 22, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 10:32:33.679189+01"},
        {"user_id": None, "product_id": 1, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 10:32:41.933702+01"},
        {"user_id": None, "product_id": 22, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 10:33:40.418613+01"},
        {"user_id": None, "product_id": 35, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 10:39:48.550745+01"},
        {"user_id": None, "product_id": 28, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 10:46:09.074711+01"},
        {"user_id": None, "product_id": 1, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 11:08:10.599418+01"},
        {"user_id": None, "product_id": 22, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 11:09:00.482689+01"},
        {"user_id": None, "product_id": 1, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 11:18:54.693258+01"},
        {"user_id": None, "product_id": 8, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 11:24:39.321644+01"},
        {"user_id": None, "product_id": 5, "type": "View", "session_id": "abe8f4e0-934f-4783-a171-50ebafbd2c2b", "created_at": "2026-02-02 12:07:33.868652+01"},

        {"user_id": 1, "product_id": 40, "type": "AddToCart", "session_id": "268fb041-2274-4140-8fb7-0f74b8bddf61", "created_at": "2026-02-02 14:31:45.317954+01"},
        {"user_id": 1, "product_id": 33, "type": "View", "session_id": "38719846-fa91-47d4-9f54-73a77853c8cc", "created_at": "2026-02-02 15:27:35.893453+01"},
        {"user_id": 1, "product_id": 23, "type": "View", "session_id": "b7c0093d-d97a-45e7-af3e-14b81b15ac96", "created_at": "2026-02-03 11:15:45.558588+01"},
        {"user_id": 1, "product_id": 29, "type": "View", "session_id": "b7c0093d-d97a-45e7-af3e-14b81b15ac96", "created_at": "2026-02-03 11:15:50.5046+01"},
        {"user_id": 1, "product_id": 26, "type": "View", "session_id": "b7c0093d-d97a-45e7-af3e-14b81b15ac96", "created_at": "2026-02-03 11:15:59.348804+01"},
        {"user_id": 1, "product_id": 27, "type": "View", "session_id": "b7c0093d-d97a-45e7-af3e-14b81b15ac96", "created_at": "2026-02-03 11:16:06.863314+01"},
        {"user_id": 1, "product_id": 26, "type": "View", "session_id": "b7c0093d-d97a-45e7-af3e-14b81b15ac96", "created_at": "2026-02-03 11:16:08.94276+01"},
        {"user_id": 1, "product_id": 40, "type": "Purchase", "session_id": "93b7fe2f-3f31-4242-9f8a-b7a2d4b106af", "created_at": "2026-02-03 13:30:08.223679+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "a876e53c-5862-48ef-9069-43535560ae0a", "created_at": "2026-02-03 14:22:06.919686+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "a876e53c-5862-48ef-9069-43535560ae0a", "created_at": "2026-02-03 14:26:02.319026+01"},

        {"user_id": 1, "product_id": 28, "type": "View", "session_id": "a876e53c-5862-48ef-9069-43535560ae0a", "created_at": "2026-02-03 14:44:36.078306+01"},
        {"user_id": 1, "product_id": 28, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 18:27:00.842361+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 18:27:45.770403+01"},
        {"user_id": 1, "product_id": 3, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 18:27:51.253583+01"},
        {"user_id": 1, "product_id": 8, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 19:12:21.082532+01"},
        {"user_id": 1, "product_id": 55, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 19:13:36.083971+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 19:25:53.37808+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "d73b56f1-4650-496f-a6b2-dedac84f5a57", "created_at": "2026-02-03 19:27:29.97806+01"},
        {"user_id": 1, "product_id": 28, "type": "View", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 06:21:10.822898+01"},
        {"user_id": 1, "product_id": 58, "type": "View", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 06:21:30.603943+01"},

        {"user_id": 1, "product_id": 58, "type": "AddToCart", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 06:21:36.5568+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 06:39:13.539336+01"},
        {"user_id": 1, "product_id": 58, "type": "View", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 06:40:51.048238+01"},
        {"user_id": 1, "product_id": 58, "type": "AddToWishlist", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 06:41:03.758736+01"},
        {"user_id": None, "product_id": 28, "type": "View", "session_id": "4af49a36-99dd-465f-bb80-1f34a5d6826c", "created_at": "2026-02-05 09:47:06.093696+01"},
        {"user_id": None, "product_id": 28, "type": "View", "session_id": "8eb679c8-d4fd-4f3e-92e6-1357553a8128", "created_at": "2026-02-05 09:47:15.45636+01"},
        {"user_id": 1, "product_id": 28, "type": "AddToCart", "session_id": "8eb679c8-d4fd-4f3e-92e6-1357553a8128", "created_at": "2026-02-05 09:47:31.507679+01"},
        {"user_id": 1, "product_id": 28, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:47:36.335046+01"},
        {"user_id": 1, "product_id": 1, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:47:59.461735+01"},
        {"user_id": 1, "product_id": 6, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:49:02.628984+01"},

        {"user_id": 1, "product_id": 1, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:49:14.822859+01"},
        {"user_id": 1, "product_id": 6, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:49:20.946398+01"},
        {"user_id": 1, "product_id": 1, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:49:23.625258+01"},
        {"user_id": 1, "product_id": 6, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:49:26.482301+01"},
        {"user_id": 1, "product_id": 1, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 09:49:28.634313+01"},
        {"user_id": None, "product_id": 40, "type": "View", "session_id": "02502a90-bbc3-413d-90d2-c87ecb782dcc", "created_at": "2026-02-05 13:36:10.653283+01"},
        {"user_id": 1, "product_id": 58, "type": "AddToCart", "session_id": "37c88041-dbdb-498f-8630-99d113c37544", "created_at": "2026-02-05 14:52:08.82993+01"},
        {"user_id": 1, "product_id": 6, "type": "AddToCart", "session_id": "bbb9d543-eb97-4070-9440-e2f74b9c29b2", "created_at": "2026-02-05 21:31:26.347305+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "f66f20fe-8a04-467e-9c43-6f57f92093ce", "created_at": "2026-02-05 21:36:14.580037+01"},
        {"user_id": 1, "product_id": 11, "type": "View", "session_id": "f66f20fe-8a04-467e-9c43-6f57f92093ce", "created_at": "2026-02-05 21:41:17.010271+01"},

        {"user_id": None, "product_id": 40, "type": "View", "session_id": "f66f20fe-8a04-467e-9c43-6f57f92093ce", "created_at": "2026-02-05 21:46:23.635688+01"},
        {"user_id": 1, "product_id": 28, "type": "View", "session_id": "02adfad1-b985-4449-bd6c-19c239a3326b", "created_at": "2026-02-05 21:49:41.787289+01"},
        {"user_id": 1, "product_id": 40, "type": "View", "session_id": "43697a31-8545-40a0-900e-e69463c9de6a", "created_at": "2026-02-05 21:49:45.12311+01"},
        {"user_id": 1, "product_id": 58, "type": "View", "session_id": "43697a31-8545-40a0-900e-e69463c9de6a", "created_at": "2026-02-05 21:49:52.850183+01"},
        {"user_id": 2, "product_id": 11, "type": "View", "session_id": "43697a31-8545-40a0-900e-e69463c9de6a", "created_at": "2026-02-06 12:10:30.823328+01"},
        {"user_id": 2, "product_id": 11, "type": "AddToCart", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:10:32.1019+01"},
        {"user_id": 2, "product_id": 28, "type": "View", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:10:41.30344+01"},
        {"user_id": 2, "product_id": 28, "type": "AddToCart", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:10:42.333798+01"},
        {"user_id": 2, "product_id": 36, "type": "View", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:10:52.954963+01"},
        {"user_id": 2, "product_id": 36, "type": "AddToCart", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:10:54.55803+01"},

        {"user_id": 2, "product_id": 46, "type": "View", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:00.121218+01"},
        {"user_id": 2, "product_id": 46, "type": "AddToCart", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:00.967451+01"},
        {"user_id": 2, "product_id": 52, "type": "View", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:05.96448+01"},
        {"user_id": 2, "product_id": 52, "type": "AddToCart", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:07.16088+01"},
        {"user_id": 2, "product_id": 11, "type": "Purchase", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:56.940616+01"},
        {"user_id": 2, "product_id": 28, "type": "Purchase", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:56.949837+01"},
        {"user_id": 2, "product_id": 36, "type": "Purchase", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:56.95289+01"},
        {"user_id": 2, "product_id": 46, "type": "Purchase", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:56.956427+01"},
        {"user_id": 2, "product_id": 52, "type": "Purchase", "session_id": "cc66baf9-c027-481b-80de-857b7af0bbf5", "created_at": "2026-02-06 12:11:57.035784+01"},
        {"user_id": 1, "product_id": 11, "type": "View", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:35:22.214722+01"},

        {"user_id": 1, "product_id": 11, "type": "AddToCart", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:35:24.119032+01"},
        {"user_id": 1, "product_id": 46, "type": "AddToCart", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:35:29.484796+01"},
        {"user_id": 1, "product_id": 52, "type": "AddToCart", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:35:34.944413+01"},
        {"user_id": 1, "product_id": 11, "type": "Purchase", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:36:17.366683+01"},
        {"user_id": 1, "product_id": 52, "type": "Purchase", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:36:17.373953+01"},
        {"user_id": 1, "product_id": 46, "type": "Purchase", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:36:17.378131+01"},
        {"user_id": 1, "product_id": 52, "type": "Purchase", "session_id": "18bffbdf-e85f-4652-b445-8b34876c874f", "created_at": "2026-02-08 20:36:17.373953+01"},
        {"user_id": 2, "product_id": 58, "type": "AddToCart", "session_id": "d0cabffd-f7a2-45e2-9aab-cda5fca14b88", "created_at": "2026-02-09 10:43:51.932104+01"},
        {"user_id": 1, "product_id": 58, "type": "View", "session_id": "475ec301-2f6f-41a9-a120-c979367a47c3", "created_at": "2026-02-09 10:44:31.475709+01"},
        {"user_id": 1, "product_id": 58, "type": "AddToCart", "session_id": "475ec301-2f6f-41a9-a120-c979367a47c3", "created_at": "2026-02-09 10:44:33.288834+01"},

       {"user_id": 2, "product_id": 58, "type": "View", "session_id": "41076b83-1b93-41fd-9933-3ddf695a90e0", "created_at": "2026-02-09 10:48:55.982848+01"},
        {"user_id": 2, "product_id": 58, "type": "AddToCart", "session_id": "41076b83-1b93-41fd-9933-3ddf695a90e0", "created_at": "2026-02-09 10:48:57.349284+01"},
        {"user_id": 2, "product_id": 58, "type": "Purchase", "session_id": "098aa619-7d81-4024-b126-3e16c39096ba", "created_at": "2026-02-09 12:01:31.710334+01"},
        {"user_id": 2, "product_id": 5, "type": "View", "session_id": "098aa619-7d81-4024-b126-3e16c39096ba", "created_at": "2026-02-09 12:09:51.543363+01"},
        {"user_id": 2, "product_id": 5, "type": "AddToCart", "session_id": "098aa619-7d81-4024-b126-3e16c39096ba", "created_at": "2026-02-09 12:09:52.697905+01"},
        {"user_id": 2, "product_id": 58, "type": "Purchase", "session_id": "098aa619-7d81-4024-b126-3e16c39096ba", "created_at": "2026-02-09 12:01:31.710334+01"},
        {"user_id": 2, "product_id": 5, "type": "Purchase", "session_id": "098aa619-7d81-4024-b126-3e16c39096ba", "created_at": "2026-02-09 12:25:58.985618+01"},
        {"user_id": None, "product_id": 43, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:55:57.378796+01"},
        {"user_id": None, "product_id": 13, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:56:22.847139+01"},
        {"user_id": None, "product_id": 26, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:56:38.201824+01"},

        {"user_id": None, "product_id": 17, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:56:51.665143+01"},
        {"user_id": None, "product_id": 20, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:57:03.586971+01"},
        {"user_id": None, "product_id": 4, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:57:19.549344+01"},
        {"user_id": None, "product_id": 7, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:57:29.389426+01"},
        {"user_id": None, "product_id": 54, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:57:42.132529+01"},
        {"user_id": None, "product_id": 61, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:57:55.849374+01"},
        {"user_id": None, "product_id": 56, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:58:07.436551+01"},
        {"user_id": None, "product_id": 59, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:58:14.553151+01"},
        {"user_id": None, "product_id": 46, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:58:27.251438+01"},
        {"user_id": None, "product_id": 32, "type": "View", "session_id": "2802c929-d7eb-4d67-acfb-f0d081a436e1", "created_at": "2026-02-09 13:58:38.063414+01"}
    ]

    for product_data in products_in_promotion:
        product = Products.query.filter_by(id=product_data["product_id"]).first()
        promotion = Promotions.query.filter_by(id=product_data["promotion_id"]).first()
        if product and promotion:
            istnieje = ProductPromotions.query.filter_by(product_id=product.id, promotion_id=promotion.id).first()
            if not istnieje:
                new_product_in_promotion = ProductPromotions(product_id=product.id, promotion_id=promotion.id)
                db.session.add(new_product_in_promotion)
                added_count += 1
    db.session.commit()
    print(f"Dodano {added_count} produktów do promocji.")

def seed_database():
    app = create_app()  # Utwórz instancję aplikacji
    
    with app.app_context():
        print("Czyszczenie bazy danych...")
        reset_database()
        reset_sequences()

        seed_main_categories()
        seed_sub_categories()
        seed_attributes()
        seed_products()
        seed_product_attributes()
        seed_attribute_weights()
        #seed_delivery_methods()
        #seed_payment_methods()
        seed_promotions()
        seed_product_in_promoton()
        #print("Uzupełnianie historycznyhc danych transakcji...")
        #seed_transactions()
        #seed_transacion_products()

if __name__ == "__main__":
    seed_database()


"""
        {"name": "", "category_id": 6, "description": "", "Image": "/images/products/Słuchawki/", "quantity": 10, "unit_price": },
        SELECT pg_get_serial_sequence('catalog.attribute_weights', 'id')
"""
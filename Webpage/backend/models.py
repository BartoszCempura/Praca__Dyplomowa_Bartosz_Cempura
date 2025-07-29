# tutaj będziemy przechowywać modele naszych baz danych
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from backend import db
import enum
import re
from sqlalchemy import CheckConstraint, func, Numeric

"""____________________________________________________________________________________________________________________"""

""" Modele dla api user_management
    - User: model reprezentujący użytkownika
    - UserAddress: model reprezentujący adres dostawy użytkownika
    - AddressType: enum reprezentujący typ adresu"""

class User(db.Model): # model reprezentujący użytkownika w bazie danych
    __tablename__ = 'users'
    __table_args__ = {'schema': 'user_management'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    role = db.Column(db.String(50), nullable=False, default='user') # domyślnie każdy użytkownik jest zwykłym użytkownikiem

    def to_json(self): # metoda do konwersji obiektu użytkownika na słownik JSON
        return {
            "id": self.id,
            "login": self.login,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "role": self.role
        }
    

    def set_password(self, password): # metoda do ustawiania hasła użytkownika
        self.password = generate_password_hash(password)
        self.updated_at = datetime.now(timezone.utc)

    def check_password(self, password): # metoda do sprawdzania hasła użytkownika
        return check_password_hash(self.password, password)

    # te metody są powiązane ale nie wymagają istnienia instancji klasy
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Sprawdzenie podstawowego fomatu email
        # Pozwala na znaki alfanumeryczne, kropki, podkreślniki i myślniki przed '@'
        # domena musi mieć co najmniej jedną kropkę i dwa znaki po niej
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        pattern = r'^[0-9]{3} [0-9]{3} [0-9]{3}$'
        # Sprawdzenie podstawowego formatu numeru telefonu
        # Pozwala na format 123-45-67-89 z trzema cyframi, myślnikiem i dwiema cyframi
        # Można dostosować do innych formatów, jeśli to konieczne
        return re.match(pattern, phone) is not None



class AddressType(enum.Enum):
    shipping = 'shipping'
    billing = 'billing'
    default = 'default'
    other = 'other'

class UserAddress(db.Model): # model reprezentujący adres dostawy użytkownika w bazie danych
    __tablename__ = 'users_addresses'
    __table_args__ = {'schema': 'user_management'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_management.users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    nip = db.Column(db.String(50), nullable=True)  
    street_name = db.Column(db.String(255), nullable=False)
    building_number = db.Column(db.String(10), nullable=False)
    flat_number = db.Column(db.Integer, nullable=True)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    type = db.Column(
        db.Enum(AddressType, name='address_type', schema='user_management'),
        nullable=False,
        default=AddressType.shipping
    )

    # Rejestracja relacji dla SQLAlchemy
    # Umożliwia dostęp do adresów użytkownika poprzez atrybut 'addresses'
    user = db.relationship('User', backref=db.backref('addresses', lazy=True, cascade='all, delete-orphan'))
    
    def to_json(self): # metoda do konwersji obiektu adresu na słownik JSON
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "company_name": self.company_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "nip": self.nip,
            "street_name": self.street_name,
            "building_number": self.building_number,
            "flat_number": self.flat_number,
            "zip_code": self.zip_code,
            "city": self.city,
            "type": self.type.value
        }
    # metody powiązane ale nie wymagają istnienia instancji klasy
    @staticmethod
    def validate_nip(nip):
        pattern = r'^[0-9]{3}-[0-9]{6}-[0-9]{1}$'
        # pattern 3 liczby, myślnik, 6 liczb, myślnik, 1 liczba
        return re.match(pattern, nip) is not None

    @staticmethod
    def validate_zip_code(zip_code):
        pattern = r'^[0-9]{2}-[0-9]{3}$'
        return re.match(pattern, zip_code) is not None

"""____________________________________________________________________________________________________________________"""

"""Modele dla api catalog 
    - Categories: model reprezentujący kategorię w bazie danych
    - Attributes: model reprezentujący atrybut, cechy produktu"""

class Categories(db.Model): # model reprezentujący kategorię w bazie danych
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'catalog'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('catalog.categories.id'), nullable=True) # kategorie z null to kategorie główne ładowane podczas uruchomienia strony
    # kategorie które mają parent_id to kategorie podrzędne i będą ładowane po najechaniu na przycisk kategorii głównej
    isused = db.Column(db.Boolean, default=True) # czy kategoria jest używana w produktach

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "isused": self.isused  # dla tego modelu musze przekazywać wartośc json jako true albo false
        }
    
class Attributes(db.Model): # model reprezentujący atrybut w bazie danych
    __tablename__ = 'attributes'
    __table_args__ = {'schema': 'catalog'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Products(db.Model): # model reprezentujący produkt w bazie danych
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
        CheckConstraint('unit_price >= 0', name='check_unit_price_non_negative'),
        {'schema': 'catalog'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('catalog.categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)  # URL do zdjęcia produktu
    quantity = db.Column(db.Integer, nullable=False, default=0)  # Ilość dostępna w magazynie
    unit_price = db.Column(Numeric(10, 2), nullable=False) # cena ja jednostkę z pominięciem promocji. SQLAlchemy zamiast Decimal stosuje dla walut Numeric
    # Numeric(10, 2) oznacza maksymalnie 10 cyfr, z czego 2 po przecinku
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_json(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    

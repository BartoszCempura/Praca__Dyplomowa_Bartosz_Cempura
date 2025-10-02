# tutaj będziemy przechowywać modele naszych baz danych
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from backend import db
import enum
import re
from sqlalchemy import CheckConstraint, UniqueConstraint, func, Numeric, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from slugify import slugify

"""____________________________________________________________________________________________________________________"""

""" Modele dla api user_management
    - User: model reprezentujący użytkownika
    - UserAddress: model reprezentujący adres dostawy użytkownika
    - AddressType: enum reprezentujący typ adresu"""

class User(db.Model): # model reprezentujący użytkownika w bazie danych
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint(r"email  ~* '^[^@]+@[^@]+.[^@]+$'", name='users_email_check'),
        CheckConstraint(r"phone_number ~ '^[0-9]{3} [0-9]{3} [0-9]{3}$'", name='users_phone_number_check'),
        {'schema': 'user_management'}
    )
    
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
    Shipping = 'Shipping'
    Billing = 'Billing'
    Default = 'Default'
    Other = 'Other'

class UserAddress(db.Model): # model reprezentujący adres dostawy użytkownika w bazie danych
    __tablename__ = 'users_addresses'
    __table_args__ = (
        CheckConstraint(r"zip_code  ~ '^[0-9]{2}-[0-9]{3}$'", name='users_addresses_zip_code_check'),
        CheckConstraint(r"nip ~ '^[0-9]{3}-[0-9]{6}-[0-9]{1}$'", name='users_addresses_nip_check'),
        {'schema': 'user_management'}
    )
    
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
        default=AddressType.Shipping
    )

    # Rejestracja relacji dla SQLAlchemy
    # Umożliwia dostęp do adresów użytkownika poprzez atrybut 'addresses'
    ## user = db.relationship('User', backref=db.backref('addresses', lazy=True, cascade='all, delete-orphan')) - pozwala na bardziej obiektowe podejście
    # umożliwia dostęp do użytkownika poprzez atrybut 'user' np user.adresses 
    
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
    - Categories: model reprezentujący kategorię produktu w bazie danych
    - Attributes: model reprezentujący atrybuty i cechy produktu
    - Products: model reprezentujący produkt w bazie danych
    - ProductAttributes: model reprezentujący połączenie atrybut i produktu w bazie danych
    - AttributeWeights: model reprezentujący wagę atrydutu dla danego produktu 
    - ProductAccessories: model reprezentujący przypisanie produktu z kategorii akcesoriuim do produktu i propozycje sklepu
    - Promotions: model reprezentujący ofertę promocyjną 
    - ProductPromotions: model reprezentujący tabelę słownikową łączącą produkty z promocją
    """


class Categories(db.Model): # model reprezentujący kategorię w bazie danych
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'catalog'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('catalog.categories.id'), nullable=True) # kategorie z null to kategorie główne ładowane podczas uruchomienia strony
    # kategorie które mają parent_id to kategorie podrzędne i będą ładowane po najechaniu na przycisk kategorii głównej
    slug = db.Column(db.String(255), unique=True, nullable=False) # unikalny identyfikator kategorii, używany w URL
    isused = db.Column(db.Boolean, default=True) # czy kategoria jest używana w produktach

    def __init__(self, name, parent_id=None, isused=True): #pozwala na tworzenie instancji kategorii z nazwą, opcjonalnym parent_id i isuused z zadeklarowanymi wartościami za wczasu. Dodatkowo slugify name do unikalnego identyfikatora
        self.name = name
        self.slug = slugify(name)
        self.parent_id = parent_id
        self.isused = isused

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,       
            "parent_id": self.parent_id,
            "slug": self.slug,
            "isused": self.isused  # jak chce zmienić musze przekazać wartość false
        }
    
    @staticmethod
    def validate_category_id(category_id):
        category = Categories.query.get(category_id)

        if not category: # jeśli kategoria nie istnieje
            return False  

        if category.parent_id is None or category.isused is False:  # jeśli kategoria jest główna lub nie jest używana
            return False

        return True  


    
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
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)  # URL do zdjęcia produktu
    quantity = db.Column(db.Integer, nullable=False, default=0)  # Ilość dostępna w magazynie
    unit_price = db.Column(Numeric(10, 2), nullable=False, default=0) # cena ja jednostkę z pominięciem promocji. SQLAlchemy zamiast Decimal stosuje dla walut Numeric
    # Numeric(10, 2) oznacza maksymalnie 10 cyfr, z czego 2 po przecinku
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    category = db.relationship('Categories', foreign_keys=[category_id])

    def to_json(self):
        return {
            "id": self.id,
            "category_name": self.category.name,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_json_user_view(self):
        return {
            "name": self.name,
            "image": self.image,
            "unit_price": self.unit_price
        }

    def price_including_promotion(self):
        now = datetime.now(timezone.utc)

        check_if_promotion_apply = ProductPromotions.query.join(
            Promotions, 
            ProductPromotions.promotion_id == Promotions.id).filter(
                ProductPromotions.product_id == self.id,
                Promotions.start_date <= now,
                Promotions.end_date >= now
            ).first()
        
        if check_if_promotion_apply:
            promotion = Promotions.query.get(check_if_promotion_apply.promotion_id)
            discount = promotion.discount_percent / 100
            return self.unit_price * (1 - discount)
        
        return self.unit_price


class ProductAttributes(db.Model): # model reprezentujący atrybut w bazie danych
    __tablename__ = 'product_attributes'
    __table_args__ = (
        UniqueConstraint('product_id', 'attribute_id', name='product_attributes_product_id_attribute_id_unique'),
        {'schema': 'catalog'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey('catalog.attributes.id', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "attribute_id": self.attribute_id,
            "value": self.value
        }



class AttributeWeights(db.Model):
    __tablename__ = 'attribute_weights'
    __table_args__ = (
        UniqueConstraint('category_id', 'attribute_id', name='attribute_weights_category_id_attribute_id_unique'),
        {'schema': 'catalog'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('catalog.attributes.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('catalog.categories.id', ondelete='CASCADE'), nullable=False)
    weight = db.Column(Numeric(3, 2), nullable=False, default=1.00)

    def to_json(self):
        return {
            "id": self.id,
            "attribute_id": self.attribute_id,
            "category_id": self.category_id,          
            "weight": self.weight
        }
    
class ProductAccessories(db.Model):
    __tablename__ = 'product_accessories'
    __table_args__ = (
        UniqueConstraint('product_id', 'accessory_product_id', name='product_accessories_product_id_accessory_product_id_unique'),
        {'schema': 'catalog'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    accessory_product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    weight = db.Column(Numeric(3, 2), nullable=False, default=0.01)

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "accessory_product_id": self.accessory_product_id,          
            "weight": self.weight
        }
    

class Promotions(db.Model):
    __tablename__ = 'promotions'
    __table_args__ = (
        CheckConstraint('discount_percent > 0 and discount_percent <= 100', name='promotions_discount_percent_check'),
        CheckConstraint('start_date < end_date', name='promotions_start_before_end'),
        {'schema': 'catalog'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    discount_percent = db.Column(Numeric(5, 2), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "discount_percent": float(self.discount_percent), ## avoid json serialization
            "start_date": self.start_date,
            "end_date": self.end_date
        }

    @staticmethod
    def validate_discount(discount_percent):
        try:
            value = float(discount_percent) # zabespieczenie przed wprowadzeniem string z json, parsowanie na float
            return 0 < value <= 100
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_promotion_live(start_date, end_date):
        try:
            start = datetime.fromisoformat(start_date)  # zabespieczenie przed wprowadzeniem string z json, parsowanie na datetime
            end = datetime.fromisoformat(end_date)
            return start < end
        except Exception:
            return False
        
class ProductPromotions(db.Model):
    __tablename__ = 'product_promotions'
    __table_args__ = (
        db.PrimaryKeyConstraint('product_id', 'promotion_id'),
        {'schema': 'catalog'}
    )

    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('catalog.promotions.id', ondelete='CASCADE'), nullable=False)

    product = db.relationship('Products', foreign_keys=[product_id])


    def to_json(self):
        return {
            "product_id": self.product_id,
            "promotion_id": self.promotion_id 
        }
    
    def to_json_user_view(self):
        return {
            "nazwa": self.product.name,
            "cena": self.product.price_including_promotion()
        }
    # dodaj wgląd dla użytkownika. Ma zwracać tylko nazwe i cenę produktu uwzględniając promocje

"""____________________________________________________________________________________________________________________"""

"""Modele dla api commerce 
    - DeliveryMethods: model reprezentujący obsługiwane przez sklep metody dostawy
    - PaymentMethods: model reprezentujący obsługiwane przez sklep metody płatności
    - Carts: model reprezentujący koszyk użytkownika i jego wartość
    - CartProducts: model reprezentujący związek produkt i koszyk
    - Transactions: model reprezentujący zatwierdzone transakcję użytkownika
    - TransactionProducts: kopia CartProducts dla zatwierdzonych transakcji, w celu przechowywania informacji o produktach będących jej przedmiotem
    - Wishlist: tabela przechowująca informacje u ulubionych produktach dla klienta
    """


class DeliveryMethods(db.Model):
    __tablename__ = 'delivery_methods'
    __table_args__ = ({'schema': 'commerce'})


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    fee = db.Column(Numeric(10, 2), nullable=False, default=0.00)
    estimated_delivery_days = db.Column(db.Integer, nullable=False, default=3)
    is_active = db.Column(db.Boolean, nullable=False, default=True) # istotne aby nie usówać metody , ponieważ może to zaszkodzić danym transakcji z użyciem tej metody płatności
    

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "fee": self.fee,
            "estimated_delivery_days": self.estimated_delivery_days,
            "is_active": self.is_active
        }
    
    @staticmethod
    def delivery_date(method):
        now = datetime.now(timezone.utc)
        return now +  timedelta(days=method.estimated_delivery_days) if method else None
    
    
class PaymentMethods (db.Model):
    __tablename__ = 'payment_methods'
    __table_args__ = ({'schema': 'commerce'})

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    fee = db.Column(Numeric(10, 2), nullable=False, default=0.00)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image, # url do pliku z ikona metody
            "fee": self.fee,
            "is_active": self.is_active
        }
    
    
class Carts (db.Model):
    __tablename__ = 'carts'
    __table_args__ = (
        CheckConstraint('total_products_cost >= 0', name='carts_total_products_cost_check'),
        {'schema': 'commerce'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_management.users.id', ondelete='CASCADE'), nullable=False)
    total_products_cost = db.Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_products_cost": self.total_products_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    
class CartProducts (db.Model):
    __tablename__ = 'cart_products'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='cart_products_quantity_check'),
        UniqueConstraint('cart_id', 'product_id', name='cart_products_cart_id_product_id_unique'),
        {'schema': 'commerce'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('commerce.carts.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price_with_discount = db.Column(Numeric(10, 2), nullable=False)

    product = db.relationship('Products', foreign_keys=[product_id])
    
    def to_json(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price_with_discount": self.unit_price_with_discount
        }
    
    def to_json_user_view(self):
        return {
            "name": self.product.name,
            "image": self.product.image,
            "quantity": self.quantity,
            "unit_price_with_discount": self.unit_price_with_discount
        }
    
    @staticmethod
    def validate_quantity(quantity):
        try:
            quantity = int(quantity) # zabespieczenie przed wprowadzeniem string
            if quantity < 1: # quantity musi być przynajmniej 1
                return None
            return quantity
        except (TypeError, ValueError):
            return None
        
        

class TransactionStatus(enum.Enum):
    Pending = 'Pending'
    Shipped = 'Shipped'
    Completed = 'Completed'
    Cancelled = 'Cancelled'
        
class Transactions (db.Model):
    __tablename__ = 'transactions'
    __table_args__ = ({'schema': 'commerce'})

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_management.users.id', ondelete='CASCADE'), nullable=False)
    total_transaction_value = db.Column(Numeric(10, 2), nullable=False, default=0.00)
    billing_address_id = db.Column(db.Integer, db.ForeignKey('user_management.users_addresses.id', ondelete='SET NULL'), nullable=True)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('user_management.users_addresses.id', ondelete='SET NULL'), nullable=True)
    billing_address_data = db.Column(JSONB, nullable=False) # rozwiązanie przehowuje słownik z adresem wykożystanym w tranzakcji. W celach historycznych i audytowych
    shipping_address_data = db.Column(JSONB, nullable=False) ## /\
    status = db.Column(
        db.Enum(TransactionStatus, name='transaction_status', schema='commerce'),
        nullable=False,
        default=TransactionStatus.Pending
    )
    delivery_method_id = db.Column(db.Integer, db.ForeignKey('commerce.delivery_methods.id', ondelete='CASCADE'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('commerce.payment_methods.id', ondelete='CASCADE'), nullable=False)
    delivery_deadline = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    shipping_address = db.relationship('UserAddress', foreign_keys=[shipping_address_id])
    delivery_method = db.relationship('DeliveryMethods', foreign_keys=[delivery_method_id])
    payment_method = db.relationship('PaymentMethods', foreign_keys=[payment_method_id])

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_transaction_value": self.total_transaction_value,
            "billing_address_id": self.billing_address_id,
            "billing_address_data": self.billing_address_data,
            "shipping_address_id": self.shipping_address_id,          
            "shipping_address_data": self.shipping_address_data,
            "status": self.status.value,
            "delivery_method_id": self.delivery_method_id, # ze względu na typ kolumny Date, będzie tu przechowywana data dostawy bez uwzględnienia godzin, minut i sekund
            "payment_method_id": self.payment_method_id,
            "delivery_deadline": self.delivery_deadline,
            "notes": self.notes,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
    
    def to_json_user_view(self):
        return {
            "Transaction_id": self.id,
            "total_transaction_value": self.total_transaction_value,
            "status": self.status.value,
            "delivery_deadline": self.delivery_deadline.isoformat(),
            "shipping_address": self.shipping_address_data,         
            "payment_method": self.payment_method.name,
            "delivery_method": self.delivery_method.name,
            "date_of_order": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }



class TransactionProducts (db.Model):
    __tablename__ = 'transaction_products'
    __table_args__ = (
        UniqueConstraint('transaction_id', 'product_id', name='transaction_products_transaction_id_product_id_unique'),
        {'schema': 'commerce'})

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('commerce.transactions.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price_with_discount  = db.Column(Numeric(10, 2), nullable=False)

    product = db.relationship('Products', foreign_keys=[product_id])

    def to_json(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price_with_discount": self.unit_price_with_discount
        }

    def to_json_user_view(self):
        return {
            "product_name": self.product.name,
            "quantity": self.quantity,
            "unit_price_with_discount": self.unit_price_with_discount
        }

class Wishlists (db.Model):
    __tablename__ = 'wishlists'
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'product_id'),
        {'schema': 'commerce'}
    )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_management.users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)

    product = db.relationship('Products', foreign_keys=[product_id])

    def to_json(self):
        return {
            "product": self.product.to_json_user_view() if self.product else None
        }

"""____________________________________________________________________________________________________________________"""

"""Modele dla api analytics 
    - UserProductInteractions: model przechowujący interakcje użytkowników z danym produktem na stronie
    - ProductReviews: model przechowujący recenzje produktów
    """



class UserProductInteractions (db.Model):
    __tablename__ = 'user_product_interactions'
    __table_args__ = (
        Index("idx_check_if_new_session", "user_id", "created_at"),
        {'schema': 'analytics'}
        )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_management.users.id', ondelete='SET NULL'), nullable=True)
    anonymous_id = db.Column(db.String(36), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    session_id = db.Column(UUID(as_uuid=True), nullable=False, server_default=func.gen_random_uuid())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "type": self.type,
            "session_id": str(self.session_id),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    

class ProductReviews (db.Model):
    __tablename__ = 'product_reviews'
    __table_args__ = (
        UniqueConstraint('product_id', 'user_id', name='product_reviews_product_id_user_id_unique'),
        CheckConstraint('rating between 1.0 and 5.0', name='rating_value_check'),
        {'schema': 'analytics'}
        )


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_management.users.id', ondelete='SET NULL'), nullable=True)
    rating = db.Column(db.Numeric(2, 1), nullable=False)
    review = db.Column(db.Text, nullable=True)
    is_verified_purchase = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = db.relationship('User', foreign_keys=[user_id])

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "review": self.review,
            "is_verified_purchase": self.is_verified_purchase,
            "is_approved": self.is_approved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_json_user_view(self):
        return {
            "user": self.user.login,
            "rating": self.rating,
            "review": self.review
        }

class ProductRecommendations(db.Model):
    __tablename__ = 'product_recommendations'
    __table_args__ = (
        UniqueConstraint('product_id', 'recommended_product_id', name='product_recommendations_unique'),
        Index('index_id_product_id', 'product_id'),
        {'schema': 'analytics'}
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    recommended_product_id = db.Column(db.Integer, db.ForeignKey('catalog.products.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Numeric(4, 2), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "recommended_product_id": self.recommended_product_id,
            "score": float(self.score)
        }

"""models for version 2.0"""
from app import db


class User(db.Model):
    """Class representing users"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(50))
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(50))
    orders = db.relationship('Orders', backref='order')

    def save(self):
        """Commits user instance to the database"""
        db.session.add(self)
        db.session.commit()


class Meals(db.Model):
    """Class representing meals"""

    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    menu = db.relationship("Menu", backref="meal")
    order = db.relationship("Orders", backref="Meal_order")

    def save(self):
        """Commits meal instance to the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Meals.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Menu(db.Model):
    """Class representing menu"""

    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))

    def save(self):
        """Commits menu instance to the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Menu.query.all()


class Orders(db.Model):
    """Class representing orders"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    meals = db.Column(db.Integer, db.ForeignKey('meal.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save(self):
        """Commits save instance to the database"""
        db.session.add(self)
        db.session.commit()

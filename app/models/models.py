"""classes for test objects"""
from flask import jsonify


class User(object):
    """user class"""

    def __init__(self):
        self.users = {}

    def create_user(self, args):
        args["admin"] = False
        args["id"] = str(len(self.users) + 1)
        self.users[args["id"]] = args

    def promote_user(self, id):
        """Promote a user to admin for privileged access"""
        for user_id in self.users:
            if id == user_id:
                self.users[id]["admin"] = True
                return True
        return False


class Meals(object):
    """Meals class"""

    def __init__(self):
        self.all_meals = {}

    def create_meal(self, args):
        args["id"] = str(len(self.all_meals) + 1)
        args["name"] = args["name"].strip()
        self.all_meals[args["id"]] = args

    def get_all_meals(self):
        """get all meals"""
        return self.all_meals

from app.v1.meals import meal_instance


class Menu(object):
    """menu class"""

    def __init__(self):
        self.all_meals = meal_instance.all_meals
        self.menu = {}

    def create_menu(self, args):
        """Check if meal exists in meals dict and add to menu"""
        for mealId in self.all_meals:
            for id in args:
                if args[id]["name"] == self.all_meals[mealId]["name"]:
                    self.menu[mealId] = self.all_meals[mealId]

    def get_menu(self):
        """get the menu"""
        return self.menu

from app.v1.menu import menu_instance


class Orders(object):

    def __init__(self):
        self.menu = menu_instance.menu
        self.orders = {}

    def create_order(self, args):
        """Create an order if the meal item exists in the menu"""
        for menuId in self.menu:
            for id in args:
                if args[id]["name"] == self.menu[menuId]["name"]:
                    self.orders[menuId] = self.menu[menuId]

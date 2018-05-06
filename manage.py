"""Manager to keep track of all commands"""
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models.modelsV2 import User, Meals, Menu, Orders

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def createsuperadmin():
    """Create a super admin first"""
    username = os.getenv('DEFAULT_ADMIN_USERNAME')
    password = os.getenv('DEFAULT_ADMIN_PASSWORD')
    full_name = os.getenv('DEFAULT_ADMIN_FULL_NAME')
    admin = os.getenv('DEFAULT_ADMIN_ROLE')
    email = os.getenv('DEFAULT_ADMIN_EMAIL')

    user = User(username=username, password=password,
                full_name=full_name, admin=admin, email=email)
    user.save()
    print("Message: Admin Created")


if __name__ == '__main__':
    manager.run()

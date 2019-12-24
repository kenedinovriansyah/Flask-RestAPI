from app import Servers
from flask_script import Server, Manager
from flask_migrate import MigrateCommand, Migrate
from flask_restplus import Api
from app.serializer.extension import db

app = Servers.create_app()
app.app_context().push()

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('runserver',Server())
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
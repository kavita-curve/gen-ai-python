import os
import unittest

# from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup
# from flask_script import Manager

from app.main import create_app, db

app = create_app(os.getenv('CURRENT_ENV') or 'dev')
app.app_context().push()

cli = FlaskGroup(app)

# manager = Manager(app)

# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)

# @manager.command
# def run():
#     app.run()

@cli.command('test')
# @click.argument('test_case', default='test*.py')
def test(test_case='test*.py'):
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()

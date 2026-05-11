from backend import create_app
app = create_app()
print('SQLALCHEMY_DATABASE_URI=', app.config['SQLALCHEMY_DATABASE_URI'])
print('DATABASE_URL=', app.config['DATABASE_URL'])
import os
path = app.config['DATABASE_URL'].replace('sqlite:///', '')
print('db_path=', path)
print('exists=', os.path.exists(path))
print('dir_exists=', os.path.exists(os.path.dirname(path)))

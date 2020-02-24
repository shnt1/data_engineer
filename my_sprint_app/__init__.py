from .app import create_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


APP = create_app()
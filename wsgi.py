import sys
import os

# Add the flask_app directory to the path so python can find app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'flask_app')))

# Change the current working directory to flask_app so Flask can find templates and static files correctly
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), 'flask_app')))

from app import app

if __name__ == "__main__":
    app.run()

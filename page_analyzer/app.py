import os
from flask import Flask
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

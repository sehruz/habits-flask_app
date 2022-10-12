from flask import Flask
from route import pages
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def create_app():
    app=Flask(__name__)
    
    client=MongoClient(os.environ.get('MONGODB_URI'))
    app.db=client.microblog


    app.register_blueprint(pages)

    return app


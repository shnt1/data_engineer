"""OpenAQ Air Quality Dashboard with Flask."""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import json
from flask import Response
from flask import request
import requests
from flask_cors import CORS
from flask import jsonify
import os
from flask import json
from flask import Response
from flask_cors import CORS
from flask_api import FlaskAPI
import os
from flask import Flask, render_template, url_for, json
import pandas as pd




def create_app():
    APP = Flask(__name__)
    CORS(APP)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salty (2).db'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy(APP)
    

    class User(DB.Model):

        id = DB.Column(DB.Integer, primary_key=True)
        rank = DB.Column(DB.Integer, nullable=False)
        user = DB.Column(DB.String(25))
        salt_score = DB.Column(DB.Float, nullable=False)
        saltiest_comment = DB.Column(DB.String(100))

        def __repr__(self):
            return '<rank:{}, user:{}, salt_score{}, saltiest_comment{}>'.format(self.rank, self.user, self.salt_score, self.saltiest_comment)





# create default path for app to list top 10 most recent entries in openaq
    @APP.route('/')
    def root():
        records = User.query.all()
        return render_template('home.html',
                               title='Top 100 Saltiest Hackers',
                               records=records)



    @APP.route('/showjson')
    def showjson():
        salty = pd.read_json('my_sprint_app/salty.json')
        to_json = salty.to_json()
        return to_json

    @APP.route("/getJsonFromFile/<filename>", methods=['GET'])
    def get_json_response(filename):
        labels_dict = {}
        response_dict = {}
        try:
            with open(filename, 'r') as labels:
                labels_dict = json.load(labels)
            response_dict[STATUS] = "true"
            response_dict["labels_mapping"] = labels_dict
            js_dump = json.dumps(response_dict)
            resp = Response(js_dump,status=200,
                            mimetype='application/json')
        except FileNotFoundError as err:
            response_dict = {'error': 'file not found in server'}
            js_dump = json.dumps(response_dict)
            resp = Response(js_dump,status=500,
                            mimetype='application/json')
        except RuntimeError as err:
            response_dict = {'error': 'error occured on server side. Please try again'}
            js_dump = json.dumps(response_dict)
            resp = Response(js_dump, status=500,
                            mimetype='application/json')
        return resp

    
    return APP

"""OpenAQ Air Quality Dashboard with Flask."""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import json
from flask import Response
from flask import request
from flask_cors import CORS
from flask_api import FlaskAPI
import requests
import FlaskJSON


def create_app():
    APP = Flask(__name__)
    json = FlaskJSON(APP)
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

    @APP.route("/uploadFiles", methods=['POST', 'GET'])

    def upload_file():
        """upload file to the server"""
        response_dict = {}
        error_files = ""
        new_filename = ""

        try:
            new_filename = request.form['FILE_NAME']
            received_files = request.files.getlist(FILES_RECEIVED)
            for each_file in received_files:
                each_file_name = each_file.filename
                try:
                    each_file.save(os.path.join(".", new_filename + each_file.filename.replace(" ", "")))
                except RuntimeError as err:
                    print("\nError in saving file: %s :: %s", each_file.filename, err)
                    error_files = error_files + "," + each_file.filename

            response_dict[STATUS] = "true"
            response_dict[ERROR_FILES_LIST] = error_files
            js_dump = json.dumps(response_dict)
            resp = Response(js_dump, status=200, mimetype='application/json')

        except RuntimeError as err:
            response_dict = {'error': 'error occured on server side. Please try again'}
            js_dump = json.dumps(response_dict)
            resp = Response(js_dump, status=500, mimetype='application/json')
        return resp

# create another route that user may type in to get list of top offenders
    @APP.route('/getJsonFromFile/<filename>', methods=['GET', 'POST'])
    def get_json_response(filename):
        labels_dict = {}
        response_dict = {}
        try:
            with open(filename, 'r') as labels:
                labels_dict = json.load(labels)

                response_dict[STATUS] = "true"
                response_dict["labels_mapping"] = labels_dict
                js_dump = json.dumps(response_dict)
                resp = Response(js_dump, status=200,
                                mimetype='application/json')

        except FileNotFoundError as err:
            response_dict = {'error': 'file not found in server'}
            js_dump = json.dumps(response_dict)
            resp = Response(js_dump, status=500,
                            mimetype='application/json')

        except RuntimeError as err:
            response_dict = {'error': 'error occured on server side. Please try again'}
            js_dump = json.dumps(resonse_dict)
            resp = Response(js_dump, status=500, 
                            mimetype='application/json')

        return resp

          


# create route that displays the cities and stats
    @APP.route('/test_api',methods=['GET','POST'])            
    def test_api():                                           
        uploaded_file = request.files['salty.json']
        data = json.load(request.files['data'])
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join('path/where/to/save', filename))
        print(data)
        return 'success'

    # create route to get most recent data from openaq
    @APP.route('/refresh')
    def refresh():
        # drop current data
        DB.drop_all()
        # create new db for new data
        DB.create_all()
        # pull data to be entered into new db
        data = utc_and_pm()
        for i in data:
            record = Record(datetime=i[0], value=i[1])
            DB.session.add(record)
    # commit changes

        data2 = get_city()
        for i in data2:
            record = City(city=i)
            DB.session.add(record)

        DB.session.commit()

        return root()
    return APP

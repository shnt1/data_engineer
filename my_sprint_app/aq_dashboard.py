"""OpenAQ Air Quality Dashboard with Flask."""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .openaq import OpenAQ
import requests

def create_app():
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy(APP)
    API = OpenAQ()

    class Record(DB.Model):

        id = DB.Column(DB.Integer, primary_key=True)
        datetime = DB.Column(DB.String(25))
        value = DB.Column(DB.Float, nullable=False)

        def __repr__(self):
            return '<datetime:{}, value:{}>'.format(self.datetime, self.value)


    class City(DB.Model):
        id = DB.Column(DB.Integer, primary_key=True)
        city = DB.Column(DB.String(25))

        def __repr__(self):
            return '<City:{}'.format(self.city)


# function for getting utc_pm for Los Angeles
    def utc_and_pm(city='Los Angeles', parameter='pm25'):
        status, body = API.measurements(city=city, parameter=parameter)
        values = []
    # print(status, body)
        for result in body['results']:
            date_utc = result['date']['utc']
            value = result['value']
            values.append((date_utc, value))
        return values


    def get_city():
        status, resp = API.cities()
        city_values = []
        for result in resp['results']:
            city = result['city']
            city_values.append(city)
        return city_values


# create default path for app to list top 10 most recent entries in openaq
    @APP.route('/')
    def root():
        records = Record.query.all()
        return render_template('home.html', title='First 100 responses from OpenAq Database', records=records)


# create another route that user may type in to get list of top offenders
    @APP.route('/topoffend')
    def topten():
        records = Record.query.filter(Record.value >= 10.0).all()
        return render_template('topoffend.html',
                               title='Top Offenders', records=records)


# create route that displays the cities and stats
    @APP.route('/cities')
    def cities():
        records = City.query.all()
        return render_template('cities.html', title='cities', records=records)


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

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
API = OpenAQ()


class Record(DB.Model):

    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<datetime:{}, value:{}>'.format(self.datetime, self.value)


class City(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(25))

    def __repr__(self):
        return '<City:{}'.format(self.city)


# function for getting utc_pm for Los Angeles
def utc_and_pm(city='Los Angeles', parameter='pm25'):
    status, body = API.measurements(city=city, parameter=parameter)
    values = []
    # print(status, body)
    for result in body['results']:
        date_utc = result['date']['utc']
        value = result['value']
        values.append((date_utc, value))
    return values


def get_city():
    status, resp = API.cities()
    city_values = []
    for result in resp['results']:
        city = result['city']
        city_values.append(city)
    return city_values


# create default path for app to list top 10 most recent entries in openaq
@APP.route('/')
def root():
    records = Record.query.all()
    return render_template('home.html', title='First 100 responses from OpenAq Database', records=records)


# create another route that user may type in to get list of top offenders
@APP.route('/topoffend')
def topten():
    records = Record.query.filter(Record.value >= 10.0).all()
    return render_template('topoffend.html',
                           title='Top Offenders', records=records)


# create route that displays the cities and stats
@APP.route('/cities')
def cities():
    records = City.query.all()
    return render_template('cities.html', title='cities', records=records)


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

from flask import render_template, flash, redirect, url_for, request
from flask import (
    Blueprint, session, jsonify, g)
from app import app, db
from pyorm.databases.mysql import MysqlDatabase

db = MysqlDatabase()


def getDBconnection():
    return db.connect(host=g.endpoint,
                      user=g.username, password=g.password).cursor()


@app.route('/db/mysql/connect', methods=['POST', 'GET'])
def MySqlconnect():
    g.endpoint = request.get_json()['Endpoint']
    g.database = request.get_json()['DatabaseName']
    g.username = request.get_json()['Username']
    g.password = request.get_json()['Password']
    if 'conn' not in g:
        conn = getDBconnection()
        conn.execute("CREATE DATABASE {}".format(g.database))
        conn.close()

    else:
        return jsonify({'result': 'OK', 'response': 'database instance already present'})
    return jsonify({'result': "OK"})


@app.route('/db/mysql/create', methods=['POST'])
def MySqlcreate():
    print("create: ", request.get_json())
    conn = getDBconnection()
    conn.execute('use {}'.format(g.database))
    conn.execute('CREATE TABLE IF NOT EXIST Person ( \
                            PersonId int Not Null primary key, \
                            UserName varchar(255), \
                            LastName varchar(255),\
                            FirstName varchar(255), \
                            Address varchar(255),\
                            City varchar(255 )) ')

    return jsonify({'result': "successfully created"})


@ app.route('/db/mysql/insert', methods=['POST'])
def MySqlinsert():
    print("inserted: ", request.get_json())
    return jsonify({'result': "successfully inserted"})


@ app.route('/db/mysql/update', methods=['POST'])
def MySqlupdate():
    print("updated: ", request.get_json())
    return jsonify({'result': "successfully updated"})


@ app.route('/db/mysql/delete', methods=['POST'])
def MySqldelete():
    print("deleted: ", request.get_json())
    return jsonify({'result': "successfully deleted"})

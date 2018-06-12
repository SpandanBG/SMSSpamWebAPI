#!/usr/bin/python3
import rethinkdb as r
import json

r.connect().repl()
config = {}

def init():
    global config
    with open('config.json', 'r') as f:
        config = json.load(f)
    config = config['db']
    return

def createUser():
    cnt = 0
    try:
        r.db('rethinkdb').table('users').insert({
            'id': config['user'],
            'password': config['password'],
        }).run()
        cnt += 1
    except Exception as e:
        print(e)
    print("Users created %d" % cnt)
    return

def createDB():
    cnt = 0
    try:
        r.db_create(config['db']).run()
        r.db(config['db']).grant(config['user'], {'read': True, 'write': True, 'config': True}).run()
        cnt += 1
    except Exception as e:
        print(e)
    print("Database create %d" % cnt)
    return

def createTables():
    cnt = 0
    try:
        for table in config['tables']:
            r.db(config['db']).table_create(table).run()
            cnt += 1
    except Exception as e:
        print(e)
    print("Tables created %d" % cnt)
    return

if __name__ == "__main__":
    print("--- Starting Setup ---")
    init()
    createUser()
    createDB()
    createTables()
    print("--- All done ---")
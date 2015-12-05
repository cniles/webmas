from threading import Lock
import json
import sys

_STORE_NAME = '.store'

# create a new lock for the store file
store_mutex = Lock()

def write_setting(prop, data):
    store_mutex.acquire()
    try:
        store = {}
        f = None
        try:
            f = open(_STORE_NAME, 'r')
            store = json.load(f)
        except IOError:
            print "IOError occured!"
        finally:
            if f:
                f.close()
        
        store[prop] = data

        f = open(_STORE_NAME, 'w')
        json.dump(store, f)
        f.close()
    except:
        print "Unexpected error: ", sys.exc_info()[0]
    finally:
        store_mutex.release()

def read_setting(prop):
    return all()[prop]

# Returns a copy of the store data
def all():
    store_mutex.acquire()
    store = {}
    try:
        f = None
        try:
            f = open(_STORE_NAME, 'r')
            store = json.load(f)
        finally:
            if f:
                f.close()
    finally:
        store_mutex.release()
            
    return store

    
    

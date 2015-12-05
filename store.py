from threading import Lock
import json
import sys

_STORE_NAME = '.store'

# create a new lock for the store file
store_mutex = Lock()

def _get_store():
    store = {}
    f = None
    try:
        f = open(_STORE_NAME, 'r')
        store = json.load(f)
    except IOError:
        print "IOError"
    finally:
        if f:
            f.close()
    return store

def _set_store(store):
    f = open(_STORE_NAME, 'w')
    json.dump(store, f)
    f.close()

def write_setting(prop, data):
    store_mutex.acquire()
    try:
        store = _get_store()
        store[prop] = data
        _set_store(store)
    except:
        print "Unexpected error: ", sys.exc_info()[0]
    finally:
        store_mutex.release()

# Returns a copy of the store data
def all():
    store_mutex.acquire()
    store = {}
    try:
        store = _get_store()
    finally:
        store_mutex.release()
            
    return store

def read_setting(prop):
    store = all()
    if prop in store.keys():
        return store[prop]
    return None

# Adds an item to a list-property    
def add_to_list(prop, item):
    store_mutex.acquire()
    print "Acquired mutex"
    try:
        store = _get_store()
        print "Got store", store
        if prop in store:
            l = store[prop]
            print "Got list", l
            if isinstance(l, list):
                l.append(item)
                print "Added item", l
                store[prop] = l
                print "Reset list"
            else:
                store[prop] = [item]
        else:
            store[prop] = [item]
        _set_store(store)
        print "Returning true"
        return True
    finally:
        store_mutex.release()
        print "Mutex released"
    return False
    

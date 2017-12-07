import sqlite3

def dump_db(*args):
    try:
        db = sqlite3.connect('data/netdata')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
    except exception as e:
        raise e
    try:
        cursor.execute('''SELECT id, env, mask, name, network, owner, size, state, vlan FROM networks''')
        networks = [dict(zip(row.keys(), row)) for row in cursor.fetchall()]
        return networks
    except exception as e:
        raise e
    finally:
        db.close()

def dup_check(*args): # exception handling broken
    pass
#     try:
#         db = sqlite3.connect('data/netdata')
#         db.row_factory = sqlite3.Row
#         cursor = db.cursor()
#     except exception as e:
#         raise e
#     try:
#         cursor.execute('''SELECT name=? FROM networks WHERE env=? AND size=?''', (name, env, size))
#         dupcheck = cursor.fetchone()
#         if dupcheck[0] != 0:
#             raise ValueError('A duplicate network name was found.')
#     except:
#         raise
#     finally:
#         db.close()

def mod_db(action, name, owner, res_index):
    try:
        db = sqlite3.connect('data/netdata')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
    except exception as e:
        raise e
    try:
        if action == 'add':
            cursor.execute('''UPDATE networks SET name=?, state=?, owner=? WHERE id=? ''', (name, 'ASSIGNED', owner, res_index))
            db.commit()
            print('\t''Network: {}'.format(res_index))
        else:
            # action == 'delete'
            cursor.execute('''UPDATE networks SET name=?, state=?, owner=? WHERE id=? ''', ('UNASSIGNED', 'UNASSIGNED', 'UNASSIGNED', res_index))
            db.commit()
            print('\t''Network: {}'.format(res_index))
    except exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def search_db(action, size, name, env, index):
    try:
        db = sqlite3.connect('data/netdata')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
    except exception as e:
        raise e
    try:
        if action == 'add':
            # dup_check(db, cursor, size, name, env)
            cursor.execute('''SELECT id, env, mask, name, network, owner, size, state, vlan FROM networks WHERE state='UNASSIGNED' AND env=? AND size=?''', (env, size))
            record_raw = cursor.fetchone()
            record = dict(zip(record_raw.keys(), record_raw))
            print('\t''Network: {}'.format(record['id']))
            return record
        else:
            cursor.execute('''SELECT id, env, mask, name, network, owner, size, state, vlan FROM networks WHERE id=?''', (index,))
            record_raw = cursor.fetchone()
            record = dict(zip(record_raw.keys(), record_raw))
            print('\t''Network: {}'.format(record['id']))
            return record
    except exception as e:
        raise e
    finally:
        db.close()

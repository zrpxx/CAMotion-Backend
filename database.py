import pymysql
import hashlib
import datetime, time
import traceback


def login(username, password):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        dt = datetime.datetime.now()
        dt_now = dt.strftime('%Y-%m-%d %H:%M:%S')

        # SQL 插入语句
        sql = 'update users set last_login=%s where username=%s;'
        cursor.execute(sql, [dt_now, username])
        db.commit()

        sql = 'select * from users where username="%s";' % username
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        if results:
            for row in results:
                id = row[0]
                name = row[1]
                pas = row[2]
                salt = row[3]
                role = row[4]
                last_login = row[5]
                banned = row[6]

            print("pas:" + password)
            print("md5:" + hashlib.md5((pas + salt).encode('utf8')).hexdigest())

            # if hashlib.md5((pas + salt).encode('utf8')).hexdigest() == password:
            if pas == password:
                result = {
                    "status": "Success",
                    "user_id": id
                }
                return result
            else:
                result = {
                    "status": "Failed",
                    "message": "Wrong password"
                }
                return result
        else:
            result = {
                "status": "Failed",
                "message": "No user"
            }
            return result

    except pymysql.err.IntegrityError:
        print("Duplicate username")
        result = {
            "status": "Failed",
            "message": "Duplicate username"
        }
        return result

    except pymysql.err.DataError:
        print("Data too long")
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result

    except pymysql.err.ProgrammingError:
        print("Cursor closed")
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result

    except pymysql.err.OperationalError:
        print("Unknown column " + username)
        result = {
            "status": "Failed",
            "message": "Unknown column " + username
        }
        return result

    except TypeError:
        print("'NoneType' has no length")
        result = {
            "status": "Failed",
            "message": "'NoneType' has no length"
        }
        return result
    except ValueError:
        print("'ModelField' object is not iterable")
        result = {
            "status": "Failed",
            "message": "'ModelField' object is not iterable"
        }
        return result

    except UnboundLocalError:
        print("local variable referenced before assignment")
        result = {
            "status": "Failed",
            "message": "local variable referenced before assignment"
        }
        return result

    except:
        traceback.print_exc()
        f = open("exceptionLog.txt", 'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        db.rollback()

    finally:
        db.close()


def register(username, password):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        dt = datetime.datetime.now()
        dt_now = dt.strftime('%Y-%m-%d %H:%M:%S')

        # SQL 插入语句
        sql = 'insert into users(username, password, last_login, salt) values(%s, %s, %s, %s);'

        cursor.execute(sql, [username, password, dt_now, time.time()])
        db.commit()

        sql = 'select * from users where username="%s";' % username
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        for row in results:
            id = row[0]
            name = row[1]
            pas = row[2]
            salt = row[3]
            role = row[4]
            last_login = row[5]
            banned = row[6]

        result = {
            "status": "Success",
            "user_id": id
        }
        return result

    except pymysql.err.IntegrityError:
        print("Duplicate username")
        result = {
            "status": "Failed",
            "message": "Duplicate username"
        }
        return result
    except pymysql.err.DataError:
        print("Data too long")
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.ProgrammingError:
        print("Cursor closed")
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result
    except pymysql.err.OperationalError:
        print("Unknown column " + username)
        result = {
            "status": "Failed",
            "message": "Unknown column " + username
        }
        return result
    except TypeError:
        print("'NoneType' has no length")
        result = {
            "status": "Failed",
            "message": "'NoneType' has no length"
        }
        return result
    except ValueError:
        print("'ModelField' object is not iterable")
        result = {
            "status": "Failed",
            "message": "'ModelField' object is not iterable"
        }
        return result
    except UnboundLocalError:
        print("local variable referenced before assignment")
        result = {
            "status": "Failed",
            "message": "local variable referenced before assignment"
        }
        return result
    except:
        traceback.print_exc()
        f = open("exceptionLog.txt", 'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        db.rollback()
    finally:
        db.close()


def get_user_cameras(user_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from cams where uid="%d";' % user_id
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        cameras = []
        for row in results:
            id = row[0]
            name = row[1]
            url = row[2]

            cameras.append({"id": id,
                            "name": name,
                            "url": url,
                            "working": True
                            })

    except pymysql.err.ProgrammingError:
        print("Cursor closed")
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result

    return cameras


def get_user_log(user_id: int, camera_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from logs where id="%d" and cid="%d";' % (user_id, camera_id)

        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        logs = []
        for row in results:
            id = row[0]
            info = row[1]
            time = row[2].strftime('%Y-%m-%d %H:%M:%S')
            attachment = row[3]

            logs.append({"id": camera_id,
                         "info": info,
                         "time": time,
                         "attachment": attachment
                         })

    except pymysql.err.ProgrammingError:
        print("Cursor closed")
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result

    return logs


# def modify_password(username, password, modified_password):
#     try:
#         db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
#                              charset='utf8')
#
#         cursor = db.cursor()
#
#         # SQL 插入语句
#         sql = 'insert into users(username, password, last_login, salt) values(%s, %s, %s, %s);'
#
#         cursor.execute(sql, [username, password, dt_now, time.time()])
#         db.commit()
#
#         sql = 'select * from users where username="%s";' % username
#         cursor.execute(sql)
#         results = cursor.fetchall()
#         cursor.close()

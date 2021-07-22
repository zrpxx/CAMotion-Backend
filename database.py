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
    finally:
        db.close()

    return cameras


def get_user_log(user_id: int, camera_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from cams where id="%d" and uid="%d";' % (camera_id, user_id)
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            sql = 'select * from logs where cid="%d";' % camera_id
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            logs = []
            if results:

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
            else:
                result = {
                    "status": "Failed",
                    "message": "No logs"
                }
                return result
        else:
            result = {
                "status": "Failed",
                "message": "Camera don't belong to the user"
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

    return logs


def modify_password(username, password, modified_password):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from users where username="%s";' % username
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            for row in results:
                id = row[0]
                name = row[1]
                pas = row[2]
                salt = row[3]
                role = row[4]
                last_login = row[5]
                banned = row[6]

            if pas == password:
                print(modified_password)
                if modified_password:
                    sql = 'update users set password=%s where username=%s;'
                    cursor.execute(sql, [modified_password, username])
                    db.commit()
                    result = {
                        "status": "Success",
                        "user_id": id,
                        "new_pass": modified_password
                    }
                    return result
                else:
                    result = {
                        "status": "Failed",
                        "message": "New password can not be empty"
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

        cursor.close()

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.ProgrammingError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Unknown column " + username
        }
        return result
    except TypeError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "'NoneType' has no length"
        }
        return result
    except ValueError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "'ModelField' object is not iterable"
        }
        return result
    except UnboundLocalError:
        traceback.print_exc()
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


def create_log(camera_id, info, attachment):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        dt = datetime.datetime.now()
        dt_now = dt.strftime('%Y-%m-%d %H:%M:%S')

        sql = 'select * from cams where id=%d;' % camera_id
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            sql = 'insert into logs(info, time, attachment, cid ) values(%s, %s, %s, %s);'
            cursor.execute(sql, [info, dt_now, attachment, camera_id])
            db.commit()

            sql = 'select * from logs where cid=%d;' % camera_id
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

            logs = []
            for row in results:
                id = row[0]
                info = row[1]
                time = row[2]
                attachment = row[3]
                cid = row[4]

                logs.append({
                    "log_id": id,
                    "info": info
                })

            result = {
                "status": "Success",
                "logs": logs
            }
            return result
        else:
            result = {
                "status": "Failed",
                "message": "Camera not exists"
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.ProgrammingError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": traceback
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
        }
        return result
    except TypeError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "TypeError"
        }
        return result
    except ValueError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "'ModelField' object is not iterable"
        }
        return result
    except UnboundLocalError:
        traceback.print_exc()
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


def create_cam(user_id, name, url):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()

        sql = 'select * from users where id=%d;' % user_id
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            sql = 'insert into cams(name, url, uid) values(%s, %s, %s);'
            cursor.execute(sql, [name, url, user_id])
            db.commit()

            sql = 'select * from cams where name="%s";' % name
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

            for row in results:
                print(row)
                id = row[0]
                name = row[1]
                url = row[2]
                area = row[3]
                algo_type = row[4]
                working = row[5]
                uid = row[6]

            result = {
                "status": "Success",
                "cid": id,
                "uid": user_id,
                "name": name
            }
            return result
        else:
            result = {
                "status": "Failed",
                "message": "User not exists"
            }
            return result
    except pymysql.err.ProgrammingError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "ProgrammingError"
        }
        return result

    except pymysql.err.IntegrityError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Name duplicate"
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
import json
import string

import pymysql
import hashlib
import datetime
import time
import traceback
import response
import redis
import random


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

            if not banned:
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
                    "message": "User banned"
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

        if username and password:
            # SQL 插入语句
            sql = 'insert into users(username, password, register_time, salt) values(%s, %s, %s, %s);'

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
        else:
            result = {
                "status": "Failed",
                "message": "empty information"
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
            rtmp_url = row[2]
            flv_url = row[4]

            cameras.append({"id": id,
                            "name": name,
                            "rtmp_url": rtmp_url,
                            "flv_url": flv_url,
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


def get_camera_log(camera_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
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
                images_url = row[5]

                logs.append({"id": camera_id,
                             "info": info,
                             "time": time,
                             "attachment": attachment,
                             "images": images_url
                             })
        else:
            result = {
                "status": "Failed",
                "message": "No logs"
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


def get_user_log(user_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from cams where uid="%d";' % user_id
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            logs = []
            for row in results:
                camera_id = row[0]
                sql = 'select * from logs where cid="%d";' % camera_id
                cursor.execute(sql)
                result_each_camera = cursor.fetchall()
                if result_each_camera:
                    for row_each in result_each_camera:
                        info = row_each[1]
                        time = row_each[2].strftime('%Y-%m-%d %H:%M:%S')
                        delete_img = row_each[3]
                        images_url = row_each[5]

                        logs.append({"id": camera_id,
                                     "info": info,
                                     "time": time,
                                     "delete_img_url": delete_img,
                                     "images": images_url
                                     })

            cursor.close()
        else:
            result = {
                "status": "Failed",
                "message": "No camera belongs to user " + user_id
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

    if not logs:
        result = {
            "status": "Failed",
            "message": "No logs"
        }
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


def create_log(camera_id, info, delete_url, url):
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
            sql = 'insert into logs(info, time, cid, delete_img, img_url ) values(%s, %s, %s, %s, %s);'
            cursor.execute(sql, [info, dt_now, camera_id, delete_url, url])
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
                delete_img = row[3]
                img_url = row[5]

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
            "message": "OperationalError"
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


def create_cam(user_id, name):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        dt = datetime.datetime.now()
        dt_now = dt.strftime('%Y-%m-%d %H:%M:%S')

        sql = 'select * from users where id=%d;' % user_id
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            sql = 'insert into cams(name, uid, create_time) values(%s, %s, %s);'
            cursor.execute(sql, [name, user_id, dt_now])
            db.commit()

            sql = 'select * from cams where name="%s";' % name
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                # print(row)
                id = row[0]
                name = row[1]
                rtmp_url = row[2]
                area = row[3]
                flv_url = row[4]
                working = row[5]
                uid = row[6]
                create_time = row[6]

            channelkey = response.get_channelkey(user_id, id)

            if channelkey != "Failed":
                sql = 'update cams set rtmp_url="%s", flv_url="%s" where id=%s;' % (
                    "rtmp://zrp.cool:1935/live/%s" % channelkey, "http://zrp.cool:7001/live/%s_%s.flv" % (user_id, id),
                    id)
                cursor.execute(sql)
                db.commit()
                cursor.close()

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
                    "message": "Cannot connect to server"
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


def delete_cam(id, cid):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()

        sql = 'select * from cams where uid=%d;' % id
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            cursor = db.cursor()
            sql = 'delete from logs where cid=%d;' % cid
            cursor.execute(sql)
            db.commit()

            sql = 'delete from cams where id=%d;' % cid
            cursor.execute(sql)
            db.commit()
            cursor.close()

            result = {"status": "Success"}
            return result

        else:
            result = {
                "status": "Failed",
                "message": "Cannot found the camera"
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def get_user_info(uid):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()

        sql = 'select * from users where id="%s";' % uid
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

            result = {
                "status": "Success",
                "id": id,
                "name": name,
                "role": role,
                "last_login": last_login,
                "banned": banned
            }
            return result

        else:
            result = {
                "status": "Failed",
                "message": "User not exists"
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def buy_vip(uid):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()

        sql = 'select * from users where id=%s;' % uid
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            sql = 'update users set role=%s where id=%s;'
            cursor.execute(sql, [1, uid])
            db.commit()
            cursor.close()

            result = {
                "status": "Success",
                "role": 1,
            }
            return result

        else:
            result = {
                "status": "Failed",
                "message": "User not exists"
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def create_report(uid, info):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()

        sql = 'select * from users where id=%s;' % uid
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            sql = 'insert into report(uid, info) values(%s, %s);'

            cursor.execute(sql, [uid, info])
            db.commit()
            cursor.close()

            result = {
                "status": "Success",
                "info": info,
            }
            return result

        else:
            result = {
                "status": "Failed",
                "message": "User not exists"
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def change_report_status(repo_id, status):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from report where id="%s";' % repo_id
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            old_status = results[0][3]
            print(old_status)
            if old_status != status:
                sql = 'update report set done=%d where id=%d;' % (status, repo_id)
                cursor.execute(sql)
                db.commit()
                cursor.close()
                result = {
                    "status": "Success",
                }
            else:
                result = {
                    "status": "Failed",
                    "message": "The status is same with new status"
                }
            return result
        else:
            result = {
                "status": "Failed",
                "message": "Don't have the report " + repo_id
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def get_undo_repo():
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from report where done=0;'
        cursor.execute(sql)
        results = cursor.fetchall()
        reports = []
        if results:
            for row in results:
                id = row[0]
                info = row[1]
                uid = row[2]
                reports.append({"id": id,
                                "info": info,
                                "uid": uid,
                                "status": 0
                                })
            return reports
        else:
            result = {
                "status": "Failed",
                "message": "All report are done"
            }
            return result

    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def get_report(user_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion",
                             port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = 'select * from report where uid="%d";' % user_id
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            report = []
            for row in results:
                info = row[1]
                report.append({
                    "info": info
                })
            return report

        else:
            result = {
                "message": "Cannot found user"
            }
            return result
    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": traceback
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


def delete_all_cam(uid):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion",
                             port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from users where id="%d";' % uid
        cursor.execute(sql)
        results_user = cursor.fetchall()
        if results_user:

            cursor = db.cursor()
            sql = 'select * from cams where uid="%d";' % uid
            cursor.execute(sql)
            results = cursor.fetchall()

            if results:
                for row in results:
                    cid = row[0]
                    cursor = db.cursor()
                    sql = 'select * from logs where cid=%d;' % cid
                    cursor.execute(sql)
                    results_per_camera = cursor.fetchall()
                    if results_per_camera:
                        sql = 'delete from logs where cid=%d;' % cid
                        cursor.execute(sql)
                        db.commit()

                sql = 'delete from cams where uid=%d;' % uid
                cursor.execute(sql)
                db.commit()
                cursor.close()
                result = {
                    "status": "Success",
                }

            else:
                result = {
                    "status": "Failed",
                    "message": "Cannot found the user's camera"
                }
        else:
            result = {
                "status": "Failed",
                "message": "Cannot found the user"
            }
        return result


    except pymysql.err.DataError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "Data too long"
        }
        return result
    except pymysql.err.OperationalError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "OperationalError"
        }
        return result
    except IndexError:
        traceback.print_exc()
        result = {
            "status": "Failed",
            "message": "IndexError"
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


def get_url(user_id: int, camera_id: int):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from cams where uid="%d" and id="%d";' % (user_id, camera_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        if results:
            channelkey = response.get_channelkey(user_id=user_id, camera_id=camera_id)
            # video.push_video(channelkey)
            result = {
                "status": "Success",
                "url": "rtmp://stream.zrp.cool:1935/live/%s" % channelkey
            }
        else:
            result = {
                "status": "Failed",
                "message": "No camera"
            }

    except pymysql.err.ProgrammingError:
        print("Cursor closed")
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result
    finally:
        db.close()

    return result


def get_dashboard_info():
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select count(*) from users'
        cursor.execute(sql)
        db.commit()
        result_users = cursor.fetchall()
        for row in result_users:
            users = row[0]

        sql = 'select count(*) from users where role = 1'
        cursor.execute(sql)
        db.commit()
        result_vips = cursor.fetchall()
        for row in result_vips:
            vips = row[0]

        sql = 'select count(*) from cams'
        cursor.execute(sql)
        db.commit()
        result_cams = cursor.fetchall()
        for row in result_cams:
            cams = row[0]

        sql = 'select count(*) from logs'
        cursor.execute(sql)
        db.commit()
        result_alerts = cursor.fetchall()
        for row in result_alerts:
            alerts = row[0]

        sql = 'select a.click_date,ifnull(b.count,0) as count\
        from (\
            SELECT curdate() as click_date\
            union all\
            SELECT date_sub(curdate(), interval 1 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 2 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 3 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 4 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 5 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 6 day) as click_date\
        ) a left join (\
          select date(register_time) as datetime, count(*) as count\
          from users\
          group by date(register_time)\
        ) b on a.click_date = b.datetime'
        cursor.execute(sql)
        db.commit()
        result_register_7 = cursor.fetchall()
        users_sum = []
        for row in result_register_7:
            users_num = row[1]
            users_sum.append(users_num)

        sql = 'select a.click_date,ifnull(b.count,0) as count\
        from (\
            SELECT curdate() as click_date\
            union all\
            SELECT date_sub(curdate(), interval 1 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 2 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 3 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 4 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 5 day) as click_date\
            union all\
            SELECT date_sub(curdate(), interval 6 day) as click_date\
        ) a left join (\
          select date(create_time) as datetime, count(*) as count\
          from cams\
          group by date(create_time)\
        ) b on a.click_date = b.datetime ORDER BY a.click_date DESC'
        cursor.execute(sql)
        db.commit()
        result_cams_7 = cursor.fetchall()
        cams_sum = []
        for row in result_cams_7:
            cams_num = row[1]
            cams_sum.append(cams_num)

        sql = 'select a.click_date,ifnull(b.count,0) as count\
            from (\
                SELECT curdate() as click_date\
                union all\
                SELECT date_sub(curdate(), interval 1 day) as click_date\
                union all\
                SELECT date_sub(curdate(), interval 2 day) as click_date\
                union all\
                SELECT date_sub(curdate(), interval 3 day) as click_date\
                union all\
                SELECT date_sub(curdate(), interval 4 day) as click_date\
                union all\
                SELECT date_sub(curdate(), interval 5 day) as click_date\
                union all\
                SELECT date_sub(curdate(), interval 6 day) as click_date\
            ) a left join (\
              select date(time) as datetime, count(*) as count\
              from logs\
              group by date(time)\
            ) b on a.click_date = b.datetime ORDER BY a.click_date DESC'
        cursor.execute(sql)
        db.commit()
        result_alerts_7 = cursor.fetchall()
        alert_sum = []
        for row in result_alerts_7:
            alert_num = row[1]
            alert_sum.append(alert_num)

        result = {
            "status": "Success",
            "user_count": users,
            "vip_count": vips,
            "cam_count": cams,
            "alert_count": alerts,
            "recent_register": users_sum,
            "recent_cam_add": cams_sum,
            "recent_alert": alert_sum
        }
        return result

    except:
        db.rollback()
    finally:
        db.close()


def generate_connection_code(cam_id, user_id):
    try:
        db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
                             charset='utf8')

        cursor = db.cursor()
        sql = 'select * from cams where uid="%d" and id="%d";' % (user_id, cam_id)
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            url_result = get_url(user_id, cam_id)
            if url_result['status'] == 'Success':
                url = url_result['url']
                print("url: ", url)

                sql = 'select * from users where id="%d";' % user_id
                cursor.execute(sql)
                results = cursor.fetchall()

                email = ''
                if results[0][9]:
                    email = results[0][9]

                r = redis.StrictRedis(host='home.zrp.cool', port=56379, db=0, password='1Qazxdr5')
                ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 6))
                while r.exists(ran_str):
                    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 6))

                value = json.dumps({
                    'user_id': user_id,
                    'email': email,
                    'cam_id': cam_id,
                    'url': url
                })
                print(value)
                r.set(ran_str, value, ex=120)
                r.close()

                return {
                    "status": "Success",
                    "code": ran_str
                }

    except pymysql.err.ProgrammingError:
        print("Cursor closed")
        result = {
            "status": "Failed",
            "message": "Cursor closed"
        }
        return result
    finally:
        db.close()


def get_connection_config(code):
    try:
        r = redis.StrictRedis(host='home.zrp.cool', port=56379, db=0, password='1Qazxdr5')
        if r.exists(code):
            value = json.loads(r.get(code))
            print(value)
            r.close()

            return {
                "status": "Success",
                "config": value
            }
        else:
            return {
                "status": "Failed",
                "message": "Code doesn't exist"
            }
    except Exception as e:
        print(str(e))

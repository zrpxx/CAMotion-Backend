# import pymysql
# import datetime
# import time
#
# def register(username, password):
#     db = pymysql.connect(host="zrp.cool", user="CAMotion", passwd="M4RpMGAKFhBBARGx", db="CAMotion", port=3306,
#                              charset='utf8')
#     curosr = db.cursor()
#     dt = datetime.datetime.now()
#     dt_now = dt.strftime('%Y-%m-%d %H-%M-%S')
#     sql = 'insert into users(username, password, last_login, salt) values(%s, %s, %s, %s);'
#     curosr.execute(sql, [username, password, dt_now, time.time()])
#     db.commit()
#
#     print(new_id)
#     for id in new_id:
#         if new_id:
#             print(new_id)
#             result = {
#                 "status": "Success",
#                 "user_id": id[0]
#             }
#         else:
#             result = {
#                 "status": "Failed",
#                 "message": "failed"
#             }
#
#     db.close()
#     return result

#!/var/www/tele_bot/venv/bin/python3
from time import sleep
import sys
import threading

from flask import Flask, request, redirect, url_for, render_template, session
from flask import Response
# from flaskext.mysql import MySQL
from flask_sslify import SSLify
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from comFunctions import *
from connectSQL import *
# -----------------------------------------------------------------------

app = Flask(__name__)
# sslify = SSLify(app)

# app.config['MYSQL_DATABASE_HOST'] = hostDB
# # app.config['MYSQL_DATABASE_PORT']= 3307
# app.config['MYSQL_DATABASE_USER'] = userDB
# app.config['MYSQL_DATABASE_PASSWORD'] = passDB
# app.config['MYSQL_DATABASE_DB'] = dataDB
# # app.config['MYSQL_DATABASE_CHARSET']='utf-8'
app.secret_key = 'asdf123qwywetyrtysdf'

# mysql = MySQL()
# mysql.init_app(app)
# conn = mysql.connect()
# curs = conn.cursor()
# print("Connect DB successful!")

usertable = {}
paraTable = []
# ----------------------get status bot -------------------


# def getStatusBot():
#     try:
#         sql_dis = "SELECT status FROM admin_manager WHERE user_name = 'admin' ;"
#         rows_status = sqlselect(sql_dis)
#         if rows_status:
#             if rows_status[0][0]:
#                 return True
#             else:
#                 return False
#     except Exception as e:
#         print("Get status failed", e)

# --------------------------------------------------------------


# def sqlselect(sql=str):
#     global conn
#     try:
#         conn = mysql.connect()
#         curs = conn.cursor()
#         curs.execute(sql)
#         rows = curs.fetchall()
#         # print(rows)
#         return rows
#     except Exception as e:
#         print("Error sqlselect: ", sql)
# -------------------------------------------------------------


@app.route('/disablebot', methods=['GET'])
def disableBot():
    try:
        sql_dis = "UPDATE admin_manager SET status = '0' WHERE user_name = 'admin';"
        curs.execute(sql_dis)
        conn.commit()
    except Exception as e:
        print('Error to set bot status')
    return redirect(url_for('dashboard'))
# --------------------------------------------------------------------------------------


@app.route('/enablebot', methods=['GET'])
def enableBot():
    try:
        sql_dis = "UPDATE admin_manager SET status = '1' WHERE user_name = 'admin';"
        curs.execute(sql_dis)
        conn.commit()
    except Exception as e:
        print('Error to set bot status')
    return redirect(url_for('dashboard'))
# --------------------------------------------------------------------------------------------------


@app.route('/logout', methods=['GET'])
def getLogout():
    session.pop('username')
    return redirect(url_for('getLogin'))
# --------------------------------------------------------------------------------------------------


@app.route('/login', methods=['GET'])
def getLogin():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')
# --------------------------------------------------------------------------------------------------


@app.route('/login', methods=['POST'])
def postLogin():
    try:
        errors = []
        _username = request.form.get('inputUsername', None)
        _pass = request.form.get('inputPassword', None)
        # sql0 = "SELECT  FROM alert_list WHERE permission = 'admin' ; "
        if _username == 'admin':
            sql_checkpass = "SELECT password FROM admin_manager WHERE user_name = 'admin';"
            rows_pass = sqlselect(sql_checkpass)
            if rows_pass:
                dbpass = rows_pass[0][0]
                if check_password_hash(dbpass, _pass):
                    session['username'] = _username
                    return redirect(url_for('dashboard'))
                else:
                    errors.append('User name/password not correct!')
                    return render_template('login.html', errors=errors)
        else:
            errors.append('User name/password not correct!')
            return render_template('login.html', errors=errors)
    except Exception as e:
        print('Error : ', e)
# -------------------------------------------------------------------------------------------------


@app.route('/getchangepass', methods=['GET'])
def getChangepass():
    return render_template('change_pass.html')
# -------------------------------------------------------------------------------------------------


@app.route('/postchangepass', methods=['POST'])
def postChangepass():
    try:
        errors = []
        oldpass = request.form.get('inputOldpass', None)
        newpass = request.form.get('inputNewpass', None)
        newpass1 = request.form.get('inputNewpass1', None)
        sql_oldpass = "SELECT password FROM admin_manager;"
        rows_oldpass = sqlselect(sql_oldpass)
        if rows_oldpass:
            dbpass = rows_oldpass[0][0]
            if check_password_hash(dbpass, oldpass):
                if newpass == newpass1:
                    hashedpass = generate_password_hash(newpass)
                    sql_chanpass = f"UPDATE admin_manager SET password = '{hashedpass}' WHERE user_name = 'admin';"
                    print(sql_chanpass)
                    curs.execute(sql_chanpass)
                    conn.commit()
                    # login again
                    session.pop('username')

                    errors.append("success")
                else:
                    errors.append("New password and retype")
                    errors.append("not match")
            else:
                errors.append("Old password not correct")
                errors.append("Try again !")
    except Exception as e:
        print("Change pass failed ", e)
    return render_template('change_pass.html', errors=errors)
# --------------------------------------------------------------------------------------------------
# handle command change permission users


@app.route('/change_u', methods=['POST'])
def change_u():
    global usertable
    # check which checkbox is checked => create a list which 'value' checked
    try:
        l_check_u = request.form.getlist('chk')
        l_text = request.form.getlist('text')
        l_datetime = request.form.getlist('extime')
    except Exception as e:
        print('Error : ', e)
    print('value request : ', l_check_u)
    print('text request : ', l_text)
    print('time request : ', l_datetime)
    # save values permission to database
    # save comments to database
    for i in usertable:
        if i in l_check_u:
            user_permi = 1
        else:
            user_permi = 0
        # using id number to index comment
        user_comm = l_text[usertable[i]['id']]
        user_datetime = l_datetime[usertable[i]['id']]
        sql1 = "UPDATE alert_list SET permission='{}',comment ='{}',expiration='{}' WHERE user_id={} ;".format(
            user_permi, user_comm, user_datetime, i)
        try:
            curs.execute(sql1)
            conn.commit()
        except Exception as e:
            print('Error update user table:',e)
    return redirect(url_for('dashboard'))
# --------------------------------------------------------------------
# handle commad change parameters on message to user


@app.route('/change_p', methods=['POST'])
def change_p():
    # check which checkbox is checked => create a list which 'value' checked
    try:
        l_check_p = request.form.getlist('chk_p')
    except Exception as e:
        print('Error : ', e)
    print('value request : ', l_check_p)

    for i in paraTable:
        if i[1] in l_check_p:
            sql1 = "UPDATE para_manager SET on_message = True WHERE parameter = '{}' ;".format(
                i[1])
            print(sql1)
            curs.execute(sql1)
            conn.commit()
        else:
            sql1 = "UPDATE para_manager SET on_message = False WHERE parameter = '{}' ;".format(
                i[1])
            print(sql1)
            curs.execute(sql1)
            conn.commit()

    return redirect(url_for('dashboard'))
# -------------------------------------------------------------------
# handle change time values config


@app.route('/change_t', methods=['POST'])
def change_t():
    try:
        timecycle = request.form['timecycle']
        timereq = request.form['timereq']
    except Exception as e:
        print('Error : ', e)

    if is_number(timecycle) and is_number(timereq):
        if float(timecycle) > 0 and float(timereq) > 0:
            sql3 = "UPDATE para_manager SET value = {} WHERE parameter = 'Time_cycle';".format(
                timecycle)
            sql4 = "UPDATE para_manager SET value = {} WHERE parameter = 'Time_req';".format(
                timereq)
            print(sql3)
            curs.execute(sql3)
            conn.commit()
            curs.execute(sql4)
            conn.commit()
    return redirect(url_for('dashboard'))
# --------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def dashboard():
    if 'username' in session:
        # get the name of parameters
        l_varReq = []
        sql0 = 'SELECT parameter,on_message,value FROM para_manager;'
        rows0 = sqlselect(sql0)
        if rows0:
            for i in rows0:
                l_varReq.append(i[0])

        # get the value of the time between cycles
        l_time_cycle = rows0[-2]
        time_cycle = l_time_cycle[2]
        # get the value of the time between requests
        l_time_req = rows0[-1]
        time_req = l_time_req[2]
        # delete the last 2 parameters (time_cycle + time_req)
        del l_varReq[-2:]
        # using list para to request values
        # list paraTable is
        paraTable.clear()
        sql2 = "SELECT `{}` FROM climate WHERE id = (SELECT MAX(id) FROM climate);".format(
            "`,`".join(l_varReq))
        rows2 = sqlselect(sql2)
        varPara = ''
        if len(rows2) > 0:
            for i in range(len(rows2[0])):
                varPara = rows2[0][i]
                # add symbol to temperature and humidity
                if l_varReq[i][:11] == 'Temperature':
                    varPara = str(varPara) + ' *C'
                if l_varReq[i][:8] == 'Humidity':
                    varPara = str(varPara) + ' %'
                # convert time values
                if l_varReq[i][-4:] == 'Time':
                    varPara = convSec2HMS(varPara)
                # convert status from camera
                if l_varReq[i] == 'Status':
                    varPara = getProgStatus(varPara)
                paraTable.append(
                    [i, l_varReq[i], varPara, rows0[i][1]]
                )

        # values user list
        sql1 = "SELECT * FROM alert_list;"
        rows1 = sqlselect(sql1)
        usertable.clear()
        if rows1[0] != 0:
            for i in range(len(rows1)):
                user_id = rows1[i][0]

                # to dispaly datetime on webpage have to change its format to "2020-10-09T22:10"
                # add letter 'T' between date and time
                var_time = str(rows1[i][5])
                var_time = var_time.replace(" ", "T")
                usertable[user_id] = {
                    'id': i,
                    'user_name': rows1[i][2],
                    'time_create': rows1[i][1],
                    'expiration': var_time,
                    'permission': rows1[i][3],
                    'comment': rows1[i][4]
                }
        # print('usertable :',usertable)
        b_status = getStatusBot()
        print('usertable: ', usertable)
        return render_template('dashboard.html', usertable=usertable,
                               paraTable=paraTable,
                               time_cycle=time_cycle,
                               time_req=time_req,
                               b_status=b_status
                               )  # status_url = '/logout',
    else:
        return redirect(url_for('getLogin'))
# ---------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

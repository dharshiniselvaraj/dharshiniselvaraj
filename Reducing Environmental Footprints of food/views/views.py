from flask import make_response,Flask, flash, redirect, render_template, request, url_for, session
from app import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        role=request.form['role']
        sql="SELECT * FROM login_table WHERE username=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='name must contain only characters and numbers!'
        else:
            sql = "SELECT count(*) FROM login_table"
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.execute(stmt)
            length = ibm_db.fetch_assoc(stmt)
            print(length)

            insert_sql = "INSERT INTO login_table VALUES (?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)

            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,username)
            ibm_db.bind_param(prep_stmt,4,password)
            ibm_db.bind_param(prep_stmt,5,length['1']+1)
            ibm_db.bind_param(prep_stmt,6,role)
            ibm_db.execute(prep_stmt)
            #msg = 'You have Successfully registered!'

            return render_template('signin.html',msg=msg)

    return render_template('register.html',msg=msg)

@app.route('/signin' ,methods=['GET','POST'])
def signin():
    global userid
    msg=''
    
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT *FROM login_table WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['USERID'] = account['USERID']
            msg = 'Logged in Successfully!'

            return redirect(url_for("home"))
        else :
            msg = 'Incorrect username/password!'
            return render_template('signin.html',msg = msg)
        
    return render_template('signin.html',msg=msg)

@app.route('/Donations', methods=['GET','POST'])
def Donations():
    print('admin')
    sql = "SELECT * FROM login_table WHERE USERID =" + str(session['USERID'])
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)
    assign = ibm_db.fetch_tuple(stmt)
    print(assign)
    list=[]
    while assign!=False:
        list.append(assign)
        assign = ibm_db.fetch_tuple(stmt)
    print(list)

    sql1="SELECT *FROM donation_table"
    stmt1=ibm_db.prepare(conn,sql1)
    ibm_db.execute(stmt1)
    donation = ibm_db.fetch_tuple(stmt1)
    print(donation)
    user1=[]
    while donation!= False:
        user1.append(donation)
        donation = ibm_db.fetch_tuple(stmt1)
    print(user1)
    return render_template("donation.html",user1=list, user=User, rows= user1)

@app.route('/delete_info/<string:USERID>' , methods = ['POST'])
def delete_info(USERID) :
    sql = "DELETE FROM DONATION_TABLE WHERE USERID=?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,USERID)
    ibm_db.execute(stmt)
    print('item deleted')
    return redirect(url_for('Donations'))

@app.route('/donate', methods=['POST','GET'])
def donate():
    sql = "SELECT * FROM login_table WHERE USERID =" + str(session['USERID'])
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)
    assign = ibm_db.fetch_tuple(stmt)
    print(User)
    if request.method == 'POST':
        TYPE_OF_FOOD = request.form['food']
        DATE_OF_COOKING = request.form['date']
        TIME_OF_COOKING= request.form['time']
        QUANTITY=request.form['quantity']
        LOCATION=request.form['location']
        sql = "INSERT INTO donation_table VALUES (?,?,?,?,?,?,?,?,NULL,NULL)"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,User[2])
        ibm_db.bind_param(stmt,2,User[1])
        ibm_db.bind_param(stmt,3,TYPE_OF_FOOD)
        ibm_db.bind_param(stmt,4,DATE_OF_COOKING)
        ibm_db.bind_param(stmt,5,TIME_OF_COOKING)
        ibm_db.bind_param(stmt,6,QUANTITY)
        ibm_db.bind_param(stmt,7,LOCATION)
        ibm_db.bind_param(stmt,8,User[4])
        ibm_db.execute(stmt)
    return render_template('donation.html')

@app.route('/update_info/<string:USERID>', methods = ['POST'])
def update_info(USERID):
    if request.method == "POST":
         AGENT_NAME = request.form.get('agent')
         update_sql ="UPDATE DONATION_TABLE SET AGENT_NAME =? WHERE USERID =  "+ str(USERID)
         stmt = ibm_db.prepare(conn,update_sql)
         ibm_db.bind_param(stmt,1,AGENT_NAME)
         ibm_db.execute(stmt)
         print('item passing')
         return redirect(url_for('Donations'))
    
@app.route('/update_agent/<string:USERID>', methods =['POST'])
def update_agent(USERID):
    if request.method == "POST":
         DONATION_STATUS = request.form.get('update')
         update_sql ="UPDATE DONATION_TABLE SET DONATION_STATUS =? WHERE USERID =  "+ str(USERID)
         stmt = ibm_db.prepare(conn,update_sql)
         ibm_db.bind_param(stmt,1,DONATION_STATUS)
         ibm_db.execute(stmt)
         print('updated')
         return redirect(url_for('Notifications'))
    

@app.route('/logout')
def logout():
    return render_template('index.html')
import sqlite3
def create_db():
    con=sqlite3.connect(database=r'IMS.db')
    cur=con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)')
    con.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,email text,desc text)')
    con.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY ,name text)')
    con.commit()

    #'pid','pname','category','qty','limit','price','supplier','status','expiry'
    cur.execute('CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY,pname text,category text,qty text,qty_limit text,price text,supplier text,expiry text,status text)')
    con.commit()
    
create_db()
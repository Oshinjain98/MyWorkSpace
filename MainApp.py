import streamlit as st
import hashlib
import re
import pandas as pd

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,Email,password,Cpassword) VALUES (?,?,?,?,?,?)',(FirstName,LastName,Mobile,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def create_price():
    c.execute('CREATE TABLE IF NOT EXISTS userstable1(Distance TEXT,price1 TEXT,Time TEXT,price2 TEXT)')
def add_price(Distance,price1,Time,price2):
    c.execute('INSERT INTO userstable1(Distance,price1,Time,price2) VALUES (?,?,?,?)',(Distance,price1,Time,price2))
    conn.commit()
def view_all_rule():
    c.execute('SELECT * FROM userstable1')
    data = c.fetchall()
    return data
def delete_rule(rule):
    c.execute("DELETE FROM userstable1 WHERE Distance="+"'"+rule+"'")
    conn.commit()
def make_hashes(password):   
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

st.title("Welcome To Distance/Time Based Price Calculate System")
menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    original_title="<p style='text-align: center;'>Calculate Price for Source and Destination Location based on KM and Time</p>"
    st.markdown(original_title, unsafe_allow_html=True)

elif choice == "Login":
    Email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        #Validation
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(Email,check_hashes(password,hashed_pswd))
            if result:
                #admin
                if Email=='a@a.com':
                    create_price()
                    st.subheader("Admin Section")
                    st.text("Distance(Km) is")
                    D1=st.text_input("Use > or < For km")
                    DBP1=st.number_input("Price=")
                    st.text("Time(hr) is")
                    T1=st.text_input("Use > or < For hr")
                    TBP1=st.number_input("Price(*x)=")
                    if st.button('Add'):
                        add_price(D1,DBP1,T1,TBP1)
                    Del=st.text_input("Delete Distance")
                    if st.button('Delete'):
                        delete_rule(Del)
                    user_result = view_all_rule()
                    clean_db = pd.DataFrame(user_result,columns=['Distance','price1','Time','price2'])
                    st.dataframe(clean_db)
                #user    
                else:
                    st.subheader("User Section")
                    D=st.number_input("Km Distance",step=0.5)
                    T=st.number_input("hr Time",step=0.5)
                    user_result = view_all_rule()
                    df = pd.DataFrame(user_result,columns=['Distance','price1','Time','price2'])
                    DBP=1.0
                    TBP=1.0
                    for i in range(len(df)):
                        #KM
                        if df.Distance[i][0]=='<':
                            if D < int(df.Distance[i][1]):
                                DBP=df.price1[i]
                        elif df.Distance[i][0]=='>':
                            if D > int(df.Distance[i][1]):
                                DBP=df.price1[i]
                        elif df.Distance[i][0]=='=':
                            if D == int(df.Distance[i][1]):
                                DBP=df.price1[i]
                        #Time
                        if df.Time[i][0]=='<':
                            if T < int(df.Time[i][1]):
                                TBP=df.price2[i]
                        elif df.Time[i][0]=='>':
                            if T > int(df.Time[i][1]):
                                TBP=df.price2[i]
                        elif df.Time[i][0]=='=':
                            if T == int(df.Time[i][1]):
                                TBP=df.price2[i]
                    if st.button("Calculate"):
                        price=(D*float(DBP))+(T*float(TBP))
                        st.success('DBP='+str(DBP)+',TBP='+str(TBP)+',Price='+str(price)+" USD")
            else:
                st.warning("Incorrect Email/Password")
        else:
             st.warning("Not Valid Email")
                        
elif choice == "SignUp":
    FirstName = st.text_input("Firstname")
    LastName = st.text_input("Lastname")
    Mobile = st.text_input("Mobile")
    Email = st.text_input("Email")
    new_password = st.text_input("Password",type='password')
    Cpassword = st.text_input("Confirm Password",type='password')
    
    if st.button("Signup"):
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (pattern.match(Mobile)):
            if re.fullmatch(regex, Email):
                create_usertable()
                add_userdata(FirstName,LastName,Mobile,Email,make_hashes(new_password),make_hashes(Cpassword))
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            else:
                st.warning("Not Valid Email")               
        else:
            st.warning("Not Valid Mobile Number")
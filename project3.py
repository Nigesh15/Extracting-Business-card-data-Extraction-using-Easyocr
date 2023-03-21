import cv2
import easyocr as ea
import re
import mysql.connector
import streamlit as st

st.set_page_config(page_title = "BUSINESS CARD EXTRACTION",layout="wide")
st.title("BUSINESS CARD EXTRACTION")
image="C:/Users/new/Desktop/p3/Creative Modern Business Card/5.png"
st.image(image)
# Image = 
reader = ea.Reader(['en'],gpu=False)
img = cv2.imread(image)
# img = cv2.imread('C:/Users/new/Desktop/p3/Creative Modern Business Card/5.png')G
results = reader.readtext(img,paragraph=True)      #decoder='wordbeamsearch'
# results = reader.readtext(img,paragraph=True)
data = []
j = 0
for i in results:
    data.append(results[j][1])
    j += 1
reg = " ".join(data)
print(reg)


Email = re.compile(r'''([a-zA-z0-9]+@[a-zA-z0-9]+\.[a-zA-Z]{2,10})''', re.VERBOSE)
email = ''
for i in Email.findall(reg):
    email += i
    reg = reg.replace(i, '')
print(f'EMAIL = {email}')

phoneNumber = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
phone_no = ''
for numbers in phoneNumber.findall(reg):
    phone_no = phone_no + ' ' + numbers
    reg = reg.replace(numbers, '')
print(f"Contactno = {phone_no}")

Address= re.compile(r'\d{2,4}.+\d{6}')
address = ''
for addr in Address.findall(reg):
    address += addr
    reg = reg.replace(addr, '')
print(f"Companyaddress = {address}")

link1= re.compile(r'www.?.[\w.]+.', re.IGNORECASE)
link = ''
for lin in link1.findall(reg):
    link += lin
print(f"Weblink = {link}")
reg = reg.replace(lin, '')
print(f"Name, Designation, Companyname = {reg}")

Business_Card=mysql.connector.connect(host='localhost',
                        database='Business_Card',
                        user='root',
                        password='*****') #Your Password
mycursor = Business_Card.cursor()

sq1= "CREATE TABLE if not exists Card_Details (MyIndex INT NOT NULL AUTO_INCREMENT,Name_Designation_Companyname VARCHAR(255),Phone_no VARCHAR(255),Link VARCHAR(255),Address VARCHAR(255),Email VARCHAR(255),PRIMARY KEY (MyIndex))"

mycursor.execute(sq1)
print('Table created successfully.')
Business_Card.commit()

sq2 = "INSERT INTO Card_Details(Name_Designation_Companyname,Phone_no,Link,Address,Email) values(%s,%s,%s,%s,%s)"
sq3=(reg,phone_no,link,address,email)
mycursor.execute(sq2,sq3)
print('Table created successfully.')
Business_Card.commit()
mycursor.close()
#importing library files and modules
from os import system,path,mkdir
from art import *

#to box text
def box(msg, indent=1, width=None, title=None):
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'
    print(box)


#main set up function when installed on a new system
def setup():
    tprint("SUPERMARKET \nMANAGEMENT SYSTEM","big")
    print("Welcome to this Super Market Management System")
    print("Lets get started!")
    print()
    #to display the file which containts the requirements
    w=open("Requirements.txt")
    box(msg=w.read(),title="REQUIREMENTS")
    print()
    r=input("Are all the requirements satisfied?[yes/no] : ")
    #if requirements aren't met, program asks user to satisfy them first
    #program terminates if conditions not met
    if r in "noNO":
        print()
        print("Please use a system which satisfies the requirements!")
        quit()

    #if requirements are met the code continues
    #user is asked to provide the necessary details and password for mysql connectivity
    system('cls')
    print("SETUP")
    print()
    dbname=input("Enter the name of store(seperate words with '_') : ")
    password=input("set password for admin access : ")
    pcheck=input("re-enter password :")
    print()
    dbpw=input("Enter mysql password : ")

    #details are then stored in a textfile
    if password==pcheck:
        f=open("SMMS.txt","w")
        f.write(str([dbname,password,dbpw]))
        print("Details successfully updated!")
        f.close()
        load_resources()
        input("""Your app is ready for use!
Press enter to continue...""")


    else:
        print("Your password does not match. Try again")
        input()
        system('cls')
        setup()





#function to load necessary load_resources
#creates database and tables
def load_resources():
    #creates folder for storing bills
    if path.exists("bills")==False:
        mkdir("bills")

    #creates necessary textfiles

    #file to save product no, employee no, order no and bill no
    if path.exists("sno.txt")==False or path.getsize("sno.txt")==0:
        f=open("sno.txt","w")
        f.writelines(["0\n","0\n","0\n"+"0"])
        f.close()

    #file to save completed orders
    if path.exists("completed_orders.txt")==False or path.getsize("completed_orders.txt")==0:
        f=open("completed_orders.txt","w")
        f.write("[\"Invoice no\",\"Product No\",\"Price\",\"Quantity\",\"Total\",\"Date of order\",\"Date of Deliviery\"]\n")
        f.close()

    #creating database and required tables
    f=open("SMMS.txt","r")
    data=eval(f.read())
    f.close()
    dbname=data[0]
    dbpw=data[2]

    import mysql.connector as mc

    mycon=mc.connect(host="localhost", user="root", passwd=dbpw)
    cursor=mycon.cursor()

    cursor.execute("create database if not exists {}".format(dbname))
    cursor.execute("use {}".format(dbname))

    cursor.execute("create table if not exists PRODUCTS(Pno integer primary key,Pname varchar(50) not null unique,CP float not null,SP float not null,Stock int,Sold int,Profit float)")

    cursor.execute("create table if not exists EMPLOYEE(E_ID integer primary key,Ename varchar(20) not null,DOB date not null,Join_Date date not null,PhoneNo bigint not null unique)")

    cursor.execute("create table if not exists ORDERS(InvoiceNo bigint primary key,Pno integer not null,Price float not null,Qty bigint not null,Total bigint not null,Date_of_order date not null)")

    cursor.execute("create table if not exists BILLS(BillNo integer primary key,Date date not null,Total float not null)")

#importing functions and modules
from databases import *
from os import system
from tabulate import tabulate
import datetime as dt
import menus

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

#billing system
def billing():
    t="bills"
    system('cls')
    print()
    print("BILLING SYSTEM")
    print()
    view("products")
    print()
    bno=sno_read(t)
    d=[]
    h=["Product No","Product name","Price","Qty","Amount"]
    a=True
    total=0
    while a!=False:
        print()
        pno=int(input("Enter product number : "))
        l=[pno]
        cursor.execute("Select Pname,sp from products where pno={}".format(pno))
        pdt=cursor.fetchall()[0]
        l.extend(pdt)
        l.append(int(input("Enter quantity : ")))
        l.append(l[2]*l[3])
        total+=l[4]
        d.append(l)
        print()
        a=input("Press enter to continue and any other key to stop bill.. ")
        if a!="":
            a=False
    system('cls')
    dttm=dt.datetime.now()
    date=dttm.strftime("%Y-%m-%d")
    time=dttm.strftime("%H:%M")
    b=tabulate(d,h)
    bprv=("BILL NO : "+str(bno)+
    "\n\nDate : "+str(date)+
    "\nTime : "+str(time)+
    "\n\n"+tabulate(d,h)+
    "\n\nTOTAL : "+str(total))
    box(bprv)
    print()
    bill_conf(bno,date,time,b,total,d)
    print()
    cont=input("Press enter to continue billing, any other key to exit to main menu..")
    if cont=="":
        billing()

#confirming the bill
def bill_conf(bno,date,time,b,total,d):
    conf=input("Please confirm if the bill is correct[y/n] : ")

    if conf in "YESyes":
        f=open("bills\\Bill{}.txt".format(bno),"w")
        f.writelines(["BILL NO :{}\n\n".format(bno),"Date : {}\n".format(date),"Time : {}\n\n".format(time),b,"\n\n Total : {}".format(total)])
        f.close()
        cursor.execute("insert into BILLS values({},'{}',{})".format(int(bno),date,total))
        for i in d:
            pno=i[0]
            qty=i[3]
            cursor.execute("select stock,sold from products where pno={}".format(pno))
            data1=cursor.fetchall()[0]
            stock=data1[0]-qty
            sold=data1[1]+qty
            cursor.execute("update products set stock={}, sold={} where Pno={}".format(stock,sold,pno))
        mycon.commit()
        sno_upt("bills",bno)
        print("Bill generated successfully!")

    elif conf in "NOno":
        print()
        print("Bill cancelled and discarded!")


    else:
        print("Invalid option selected!")
        bill_conf()

#displaying old bills
def read_bills():
    system('cls')
    print("Bills")
    print()
    dt=input("Enter date of the bill[yyyy-mm-dd]: ")
    cursor.execute("Select * from bills where date='{}'".format(dt))
    d=cursor.fetchall()
    if d==[]:
        print()
        print("No bills found on this date!")
        print()
        input("Press Enter to continue..")

    else :
        cursor.execute("desc bills")
        d2=cursor.fetchall()
        h=[]
        for i in d2:
            h.append(i[0])
        print()
        print(tabulate(d,h))
        print()
        bno=int(input("Enter bill no : "))
        f=open("bills\\Bill{}.txt".format(bno))
        bill=f.read()
        system('cls')
        box(bill)
        print()
        input("Press enter to continue...")

#displaying total profits
def total_profit():
    system('cls')
    print()
    total=0
    h=["Product No","Product Name","Quantity Sold","Profit","Total profit"]
    cursor.execute("Select pno,pname,sold,profit from products")
    initd=cursor.fetchall()
    d=[]
    for i in initd:
        i=list(i)
        t=i[2]*i[3]
        i.append(t)
        total+=t
        d.append(i)
    print(tabulate(d,h,tablefmt="pretty"))
    print()
    print("Total profit on all the products : ",total)
    print()
    input("Press enter to continue..")

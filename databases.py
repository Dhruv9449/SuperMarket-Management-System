#getting the database name and password from tect file
f=open("SMMS.txt","r")
data=eval(f.read())
f.close()
dbname=data[0]
dbpw=data[2]

#importing libraries and modules
from os import path
import datetime
import mysql.connector as mc
from tabulate import tabulate
#establishing connection with mysql
mycon=mc.connect(host="localhost", user="root", passwd=dbpw)
cursor=mycon.cursor()

cursor.execute("use {}".format(dbname))

#serial number functions
#to update serial no when new record is added
def sno_upt(t,sno):
    sno=str(sno)+"\n"
    f=open("sno.txt","r+")
    d=f.readlines()
    if t=="products":
        d[0]=sno
    elif t=="employee":
        d[1]=sno
    elif t=="orders":
        d[2]=sno
    elif t=="bills":
        d[3]=sno
    f.seek(0)
    f.writelines(d)
    f.close()

#to fetch serial number
def sno_read(t):
    f=open("sno.txt","r")
    d=f.readlines()
    if t=="products":
        sno=int(d[0])+1
    elif t=="employee":
        sno=int(d[1])+1
    elif t=="orders":
        sno=int(d[2])+1
    elif t=="bills":
        sno=int(d[3])+1
    f.close()
    return sno


#database functions

#to view table
def view(t):
    print()
    cursor.execute("select * from {}".format(t))
    d=cursor.fetchall()
    cursor.execute("desc {}".format(t))
    d2=cursor.fetchall()
    h=[]
    for i in d2:
        h.append(i[0])
    print()
    print(t)
    print (tabulate(d,h,tablefmt="pretty"))

    print()
    input("Press enter to continue..")
    return d

#to add new records to the table
def add(t):
    cursor.execute("desc {}".format(t))
    d=cursor.fetchall()
    n=int(input("Enter no of records that need to be added : "))


    for i in range(n):
        sno=sno_read(t)
        l=[sno]
        k=0

        for j in d[1:]:
            if "Total" in j[0]:
                l.append(l[2]*l[3])
                continue
            if "Sold" in j[0]:
                l.append(0)
                continue
            if "Profit" in j[0]:
                l.append(l[3]-l[2])
                continue
            if "Date_of_order" in j[0]:
                l.append(str(datetime.date.today()))
                continue
            if t=="orders" and "Price" in j[0]:
                cursor.execute("Select CP from products where Pno={}".format(l[1]))
                price=cursor.fetchone()[0]
                l.append(price)
                continue


            if "varchar" in j[1] or "char" in j[1] or "date" in j[1]:
                l.append(input("enter the value of {}:".format(j[0])))
            elif j[1] in "integer" or j[1] in "bigint":
                l.append(int(input("enter the value of {}:".format(j[0]))))
            else:
                l.append(float(input("enter the value of {}:".format(j[0]))))
            k+=1
        l=str(tuple(l))
        cursor.execute("insert into {} values{}".format(t,l))
        print()
        mycon.commit()
        print("records added successfully!")
        sno_upt(t,sno)
        print()
        input("Press enter to continue..")
        print()


#to mark an order delivered
def ord_del(t):
    view(t)
    inv=int(input("Enter Invoice number of the order that has been delivered :"))
    cursor.execute("select * from orders where InvoiceNo={}".format(inv))
    od=list(cursor.fetchall()[0])
    cursor.execute("select Pno from Products")
    pno=cursor.fetchall()
    n_qty=od[3]
    p1=(od[1],)
    if p1 in pno:
        cursor.execute("select stock from products where Pno={}".format(p1[0]))
        o_qty=cursor.fetchall()[0][0]
        cursor.execute("update products set stock={} where Pno={}".format((o_qty+n_qty),p1[0]))
        cursor.execute("delete from orders where Pno={}".format(p1[0]))
        od.append(datetime.date.today())
        co=open("completed_orders.txt","a+")
        co.write(str(od)+"\n")
        co.close()
        print()
        print("successfully updated details!")
        mycon.commit()
    else:
        print("Product does not exist in database, please add product in products and retry!")
    print()
    input("Press enter to continue..")
    print()

#to display completed orders
def comp_orders(t):
    print()
    f=open("completed_orders.txt")
    d=[]
    h=eval(f.readline())
    for i in f.readlines():
        d.append(eval(i))
    print (tabulate(d,h))
    f.close()
    print()
    input("Press enter to continue..")

#to modify records
def modify(t):
    view(t)
    print()
    cursor.execute("desc {}".format(t))
    d=cursor.fetchall()
    dic={}
    for i in d:
        dic[i[0]]=i[1]

    n=int(input("Enter the {} : ".format(d[0][0])))
    op=""
    a=1
    print()
    cursor.execute("select * from {} where {}={}".format(t,d[0][0],n))
    r=cursor.fetchall()
    h=[]
    for i in d:
        h.append(i[0])
    print()
    print (tabulate(r,h,tablefmt="pretty"))
    print()

    for i in d:
        op=op+str(a)+". "+i[0]+"\n"
        a+=1
        
    f=input("""Enter the field name you would like to modify {} : \n""".format("\n"+op))
    if f[0].islower:
        f.capitalize()
    val=input("Enter new value :")


    if "varchar" in dic[f] or "char" in dic[f] or "date" in dic[f]:
        cursor.execute("update {} set {}='{}' where {}".format(t,f,val,d[0][0]+"="+str(n)))

    else:
        cursor.execute("update {} set {}={} where {}".format(t,f,val,d[0][0]+"="+str(n)))


    print("successfully updated")
    mycon.commit()
    print()
    input("Press enter to continue..")


#to delete records
def delete(t):
    view(t)
    cursor.execute("desc {}".format(t))
    d=cursor.fetchall()
    n=int(input("Enter the {} : ".format(d[0][0])))
    cursor.execute("delete from {} where {}".format(t,d[0][0]+"="+str(n)))
    print()
    mycon.commit()
    print("Record deleted successfully")
    print()
    input("Press enter to continue...")

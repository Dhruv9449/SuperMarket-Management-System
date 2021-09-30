#importing libraries and modules
from databases import *
from os import system
from setup import *
from art import *
from billing_system import *


#menu for viewing,adding,modifying and deleting from tables
def vadm_menu(t):
    system('cls')
    print(t.upper())
    print()
    opt=int(input("""Enter the option you want to access:
1. View
2. Add
3. Modify
4. Delete
5. Go back : """))

    if opt==1:
        view(t)
    elif opt==2:
        add(t)
    elif opt==3:
        modify(t)
    elif opt==4:
        delete(t)
    elif opt==5:
        admin()
    else:
        print("INVALID!")
    print()
    admin()


#for product management functions
def products():
    print()
    print("PRODUCTS")
    print()
    t="products"
    vadm_menu(t)

#for employee management functions
def employee():
    print()
    print("EMPLOYEE MANAGEMENT")
    print()
    t="employee"
    vadm_menu(t)

#for order management functions
def orders():
    print()
    print("ORDERS")
    print()
    system('cls')
    print()
    t="orders"
    opt=int(input("""Enter the option you want to access:
1. View
2. Add
3. Modify
4. Order delivered
5. Delete order
6. Go back : """))

    if opt==1:
        system('cls')
        print()
        opt2=int(input("""Enter the table you would like to view :
1. Pending Orders
2. Completed Orders
3. Go back : """))
        if opt2==1:
            view(t)
        elif opt2==2:
            comp_orders(t)
        elif opt2==3:
            orders()
        else:
            print("INVALID INPUT")

    elif opt==2:
        add(t)
    elif opt==3:
        modify(t)
    elif opt==4:
        ord_del(t)
    elif opt==5:
        delete(t)
    elif opt==6:
        admin()
    else:
        print("INVALID!")
    print()
    admin()

#for stored data and profit stats
def data():
    system('cls')
    print("DATA")
    print()
    t="products"
    dat=int(input("""Select the option you want to access:
1. Bills
2. Profits
3. Go back :
 """))
    if dat==1:
        read_bills()
        admin()
    elif dat==2:
        total_profit()
    elif dat==3:
        admin()
    else:
        print("INVALID!")
    admin()

#for admin menu functions
def admin():
    system('cls')
    print()
    print("ADMIN")
    print()
    o=int(input("""Select the option you want to access:
1. Products
2. Employee Management
3. Orders
4. Data:
5. Exit admin : """))
    if o==1:
        products()
    elif o==2:
        employee()
    elif o==3:
        orders()
    elif o==4:
        data()
    elif o==5:
        main()
    else:
        print("INVALID!")

#for employee functions
def Employee():
    billing()


#main menu
def main():

    while True:
        system('cls')
        print("")
        head=text2art(dbname,font="big")
        print(head)
        print("Have a wonderful experience!")
        print("---------------------------------")
        print("LOGIN")
        a=int(input("""Select access mode :
        1. Admin
        2. Employee
        3. Exit : """))
        if a==1:
            system("cls")
            print("LOGIN")
            pwd=input("Enter password : ")
            f=open("SMMS.txt","r")
            data=eval(f.read())
            f.close()
            password=data[1]
            if pwd==password:
                admin()
            else:
                print("Incorrect password, access denied!")
                input("Press enter to continue..")
                main()
        elif a==2:
            Employee()
        elif a==3:
            end()

        else:
            print("INVALID!")
            input("Press enter to continue..")

#end
def end():
    system('cls')
    box(text2art("""Thank  you  for  using

    SuperMarket Management
    system
    by
    Dhruv and Anirudh""","big"))
    quit()

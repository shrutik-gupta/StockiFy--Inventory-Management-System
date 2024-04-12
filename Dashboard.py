from tkinter import*
from PIL import Image,ImageTk
from Employee import employeeClass
from Supplier import supplierClass
from Category import categoryClass
from Products import productClass
from Sales import salesClass
from datetime import datetime,timedelta
import time
import os
import sqlite3
from tkinter import ttk,messagebox
class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x775+0+0")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")

        #title
        self.icon_title=PhotoImage(file="Images/Icon_logo1.png")
        title=Label(self.root,text="Stockify",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #logout button
        btn_logout=Button(self.root,text='Logout',command=self.logout,font=("times new roman",15,'bold'),bg="yellow",cursor="hand2").place(x=1350,y=10,height=50,width=150)
        
        #calender and clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangement System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #main frame
        MainFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white",)
        MainFrame.place(x=254,y=102,width=1260,height=625)
        canvas = Canvas(MainFrame, bg="white")
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(MainFrame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
       
        #left menu
        self.Menu_logo=Image.open("Images/Menu_logo1.png")
        self.Menu_logo=self.Menu_logo.resize((250,250),Image.AFFINE)
        self.Menu_logo=ImageTk.PhotoImage(self.Menu_logo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=2,y=102,width=250,height=670)

        lbl_menuLogo=Label(LeftMenu,image=self.Menu_logo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        #left menu label
        lbl_menu=Label(LeftMenu,text="Menu",font=("times roman new",25),bg='#009688').pack(side=TOP,fill=X)
        
        #left menu button
        self.icon_side=PhotoImage(file="Images/side1.png")
        Employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times roman new",20,"bold"),bg='white',bd=3,cursor="hand2").pack(side=TOP,fill=X)
        Supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times roman new",20,"bold"),bg='white',bd=3,cursor="hand2").pack(side=TOP,fill=X)
        Category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times roman new",20,"bold"),bg='white',bd=3,cursor="hand2").pack(side=TOP,fill=X)
        Products=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times roman new",20,"bold"),bg='white',bd=3,cursor="hand2").pack(side=TOP,fill=X)
        Sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times roman new",20,"bold"),bg='white',bd=3,cursor="hand2").pack(side=TOP,fill=X)
        Exit=Button(LeftMenu,text="Exit",command=self.exit,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times roman new",20,"bold"),bg='white',bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #Contents

        self.lbl_employee=Label(MainFrame,text="Total Employee\n[ 0 ]",bd=5,relief=RIDGE,bg='#ffc107',fg='white',font=("goudy old style",20,'bold'))
        self.lbl_employee.place(x=90,y=50,height=150,width=300)

        self.lbl_supplier=Label(MainFrame,text="Total Supplier\n[ 0 ]",bd=5,relief=RIDGE,bg='#607d8b',fg='white',font=("goudy old style",20,'bold'))
        self.lbl_supplier.place(x=480,y=50,height=150,width=300)

        self.lbl_category=Label(MainFrame,text="Total Category\n[ 0 ]",bd=5,relief=RIDGE,bg='#009688',fg='white',font=("goudy old style",20,'bold'))
        self.lbl_category.place(x=870,y=50,height=150,width=300)

        self.lbl_product=Label(MainFrame,text="Total Product\n[ 0 ]",bd=5,relief=RIDGE,bg='#ff5722',fg='white',font=("goudy old style",20,'bold'))
        self.lbl_product.place(x=285,y=250,height=150,width=300)

        self.lbl_sales=Label(MainFrame,text="Total Sales\n[ 0 ]",bd=5,relief=RIDGE,bg='#33bbf9',fg='white',font=("goudy old style",20,'bold'))
        self.lbl_sales.place(x=675,y=250,height=150,width=300)

        #Footer
        lbl_footer=Label(self.root,text="IMS-Inventory Mangement System | Developed By SKAD\nFor any Technical Issue Contact xxxxx xxxxx",font=("times roman new",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_date_time()
        self.update_content()

    def employee(self):
        self.__new__win=Toplevel(self.root)
        self.new_obj=employeeClass(self.__new__win)

    def supplier(self):
        self.__new__win=Toplevel(self.root)
        self.new_obj=supplierClass(self.__new__win)

    def category(self):
        self.__new__win=Toplevel(self.root)
        self.new_obj=categoryClass(self.__new__win)
    
    def product(self):
        self.__new__win=Toplevel(self.root)
        self.new_obj=productClass(self.__new__win)
    
    def sales(self):
        self.__new__win=Toplevel(self.root)
        self.new_obj=salesClass(self.__new__win)

    def update_date_time(self):
        set_time=time.strftime("%I:%M:%S")
        set_date=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Mangement System\t\t Date: {str(set_date)}\t\t Time: {str(set_time)}")
        self.lbl_clock.after(200,self.update_date_time)

    # def update_content(self):
    
    #     con=sqlite3.connect(database=r'IMS.db')
    #     cur=con.cursor()
    #     try:
    #         cur.execute("select * from product")
    #         product=cur.fetchall()
    #         self.lbl_product.config(text=f'Total Products\n[ {str(len(product))} ]')
            
    #         cur.execute("select * from supplier")
    #         supplier=cur.fetchall()
    #         self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')
            
    #         cur.execute("select * from category")
    #         category=cur.fetchall()
    #         self.lbl_category.config(text=f'Total Categories\n[ {str(len(category))} ]')

    #         self.lbl_sales.config(text=f'Total Sales\n[{str(len(os.listdir('bill')))}]')

    #         cur.execute("select * from employee")
    #         employee=cur.fetchall()
    #         self.lbl_employee.config(text=f'Total Employee\n[ {str(len(employee))} ]')

    #     except Exception as ex:
    #         messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        

    def update_content(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            products=cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(products))} ]')

            # Check for products with expiry near current date
            near_expiry_products = []
            for product in products:
                expiry_date = datetime.strptime(product[7], "%d-%m-%Y")  # Assuming expiry is stored in YYYY-MM-DD format
                if expiry_date <= datetime.now() + timedelta(days=7):  # Check if expiry is within the next 7 days
                    near_expiry_products.append(product[1])  # Assuming product[1] contains the product name
            
            if near_expiry_products:
                messagebox.showwarning("Near Expiry Products", f"The following products are near expiry: {', '.join(near_expiry_products)}")
            
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')
            
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Categories\n[ {str(len(category))} ]')

            self.lbl_sales.config(text=f'Total Sales\n[{str(len(os.listdir('bill')))}]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee\n[ {str(len(employee))} ]')
            # your existing code continues...

        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system('python login.py')

    def exit(self):
        self.root.destroy()

if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()

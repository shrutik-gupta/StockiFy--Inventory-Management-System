from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class BillingClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x775+0+0")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")

        self.cart_list=[]
        self.chk_print=0

        #title
        self.icon_title=PhotoImage(file="Images/Icon_logo1.png")
        title=Label(self.root,text="Stockify",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #logout button
        btn_logout=Button(self.root,text='Logout',command=self.logout,font=("times new roman",15,'bold'),bg="yellow",cursor="hand2").place(x=1350,y=10,height=50,width=150)
        
        #calender and clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangement System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #Footer
        lbl_footer=Label(self.root,text="IMS-Inventory Mangement System | Developed By SKAD\nFor any Technical Issue Contact xxxxx xxxxx",font=("times roman new",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        #product frame
        self.var_pname=StringVar()
        ProductFrame1=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        ProductFrame1.place(x=5,y=105,width=500,height=620)

        pTitle=Label(ProductFrame1,text='All Products',font=('goudy old style',20,'bold'),bg='#262626',fg='white').pack(side=TOP,fill=X)

        ProductFrame2=Frame(ProductFrame1,bd=2.5,relief=RIDGE,bg='white')
        ProductFrame2.place(x=2,y=42.5,width=490,height=100)

        lbl_search=Label(ProductFrame2,text='Search Product | By Name',font=('times new roman',17,'bold'),bg='white',fg='green').place(x=5,y=5,height=40,width=360)
        lbl_pname=Label(ProductFrame2,text='Product Name',font=('times new roman',17,'bold'),bg='white').place(x=5,y=50,height=40,width=155)
        txt_pname=Entry(ProductFrame2,textvariable=self.var_pname,font=('times new roman',17,'bold'),bg='lightyellow').place(x=165,y=50,height=40,width=200)
        btn_search=Button(ProductFrame2,text='Search',command=self.search,font=('goudy old style',17,'bold'),bg='#2196f3',fg='white',cursor='hand2').place(x=370,y=50,height=40,width=110)
        btn_showall=Button(ProductFrame2,text='Show All',command=self.show,font=('goudy old style',17,'bold'),bg='#083531',fg='white',cursor='hand2').place(x=370,y=5,height=40,width=110)

        #view table
        ProductFrame3=Frame(ProductFrame1,bd=2.5,relief=RIDGE)
        ProductFrame3.place(x=2,y=145,width=490,height=430)
        scrolly1=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx1=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        self.ProductTable=ttk.Treeview(ProductFrame3,columns=('pid','pname','price','qty','status'),yscrollcommand=scrolly1.set,xscrollcommand=scrollx1.set)
        scrollx1.pack(side=BOTTOM,fill=X)
        scrolly1.pack(side=RIGHT,fill=Y)

        scrollx1.config(command=self.ProductTable.xview)
        scrolly1.config(command=self.ProductTable.yview)
        self.ProductTable.heading('pid',text='Product ID')
        self.ProductTable.heading('pname',text='Product Name')
        self.ProductTable.heading('price',text='Price')
        self.ProductTable.heading('qty',text='Quantity')
        self.ProductTable.heading('status',text='Status')
        self.ProductTable['show']='headings'
        self.ProductTable.column('pid',width=90)
        self.ProductTable.column('pname',width=90)
        self.ProductTable.column('price',width=90)
        self.ProductTable.column('qty',width=90)
        self.ProductTable.column('status',width=90)
        self.ProductTable.pack(fill=BOTH,expand=1,)
        self.ProductTable.bind('<ButtonRelease-1>',self.get_data)
        lbl_note=Label(ProductFrame1,text='Note: Enter 0 QTY to remove product from the cart',anchor=W,font=('goudy old style',15),bg='white',fg='red').pack(side=BOTTOM,fill=X)
        
        #Customer Frame
        self.var_cname=StringVar()
        self.var_ccontact=StringVar()
        CustomerFrame1=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        CustomerFrame1.place(x=510,y=105,width=500,height=100)

        cTitle=Label(CustomerFrame1,text='Customer Details',font=('goudy old style',20,'bold'),bg='darkgrey').pack(side=TOP,fill=X)

        lbl_cname=Label(CustomerFrame1,text='Name',font=('goudy old style',15,'bold'),bg='white').place(x=5,y=50,width=60,height=40)
        txt_cname=Entry(CustomerFrame1,textvariable=self.var_cname,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=70,y=50,width=150,height=40)
        lbl_ccontact=Label(CustomerFrame1,text='Contact No',font=('goudy old style',15,'bold'),bg='white').place(x=235,y=50,width=100,height=40)
        txt_ccontact=Entry(CustomerFrame1,textvariable=self.var_ccontact,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=340,y=50,width=150,height=40)

        #calc cart frame
        Calc_cart_Frame=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        Calc_cart_Frame.place(x=510,y=210,width=500,height=400)

        self.var_calc_input=StringVar()
        Calc_Frame=Frame(Calc_cart_Frame,bd=2.5,relief=RIDGE,bg='white')
        Calc_Frame.place(x=5,y=5,width=485,height=190)

        txt_cal_input=Entry(Calc_Frame,textvariable=self.var_calc_input,font=('goudy old style',25,'bold'),bd=5,relief=GROOVE,state='readonly',justify=RIGHT).place(x=0,y=0,height=90,width=255)
        
        btn_7=Button(Calc_Frame,text='7',font=('goudy old style',20,'bold'),command=lambda:self.get_input(7),cursor='hand2',bg='lightgrey').place(x=255,y=0,height=45,width=75)
        btn_8=Button(Calc_Frame,text='8',font=('goudy old style',20,'bold'),command=lambda:self.get_input(8),cursor='hand2',bg='lightgrey').place(x=330,y=0,height=45,width=75)
        btn_9=Button(Calc_Frame,text='9',font=('goudy old style',20,'bold'),command=lambda:self.get_input(9),cursor='hand2',bg='lightgrey').place(x=405,y=0,height=45,width=75)
        
        btn_4=Button(Calc_Frame,text='4',font=('goudy old style',20,'bold'),command=lambda:self.get_input(4),cursor='hand2',bg='lightgrey').place(x=255,y=45,height=45,width=75)
        btn_5=Button(Calc_Frame,text='5',font=('goudy old style',20,'bold'),command=lambda:self.get_input(5),cursor='hand2',bg='lightgrey').place(x=330,y=45,height=45,width=75)
        btn_6=Button(Calc_Frame,text='6',font=('goudy old style',20,'bold'),command=lambda:self.get_input(6),cursor='hand2',bg='lightgrey').place(x=405,y=45,height=45,width=75)
        
        btn_1=Button(Calc_Frame,text='1',font=('goudy old style',20,'bold'),command=lambda:self.get_input(1),cursor='hand2',bg='lightgrey').place(x=255,y=90,height=45,width=75)
        btn_2=Button(Calc_Frame,text='2',font=('goudy old style',20,'bold'),command=lambda:self.get_input(2),cursor='hand2',bg='lightgrey').place(x=330,y=90,height=45,width=75)
        btn_3=Button(Calc_Frame,text='3',font=('goudy old style',20,'bold'),command=lambda:self.get_input(3),cursor='hand2',bg='lightgrey').place(x=405,y=90,height=45,width=75)
        
        btn_00=Button(Calc_Frame,text='00',font=('goudy old style',20,'bold'),command=lambda:self.get_input('00'),cursor='hand2',bg='lightgrey').place(x=255,y=135,height=45,width=75)
        btn_0=Button(Calc_Frame,text='0',font=('goudy old style',20,'bold'),command=lambda:self.get_input(0),cursor='hand2',bg='lightgrey').place(x=330,y=135,height=45,width=75)
        btn_dot=Button(Calc_Frame,text='.',font=('goudy old style',20,'bold'),command=lambda:self.get_input('.'),cursor='hand2',bg='lightgrey').place(x=405,y=135,height=45,width=75)

        btn_clear=Button(Calc_Frame,text='C',font=('goudy old style',20,'bold'),command=self.clear_cal,cursor='hand2',bg='lightgrey').place(x=0,y=90,height=45,width=85)
        btn_minus=Button(Calc_Frame,text='-',font=('goudy old style',20,'bold'),command=lambda:self.get_input('-'),cursor='hand2',bg='lightgrey').place(x=85,y=90,height=45,width=85)
        btn_plus=Button(Calc_Frame,text='+',font=('goudy old style',20,'bold'),command=lambda:self.get_input('+'),cursor='hand2',bg='lightgrey').place(x=170,y=90,height=45,width=85)
        btn_equal=Button(Calc_Frame,text='=',font=('goudy old style',20,'bold'),command=self.perform_cal,cursor='hand2',bg='lightgrey').place(x=0,y=135,height=45,width=85)
        btn_divide=Button(Calc_Frame,text='/',font=('goudy old style',20,'bold'),command=lambda:self.get_input('/'),cursor='hand2',bg='lightgrey').place(x=85,y=135,height=45,width=85)
        btn_multiply=Button(Calc_Frame,text='x',font=('goudy old style',20,'bold'),command=lambda:self.get_input('*'),cursor='hand2',bg='lightgrey').place(x=170,y=135,height=45,width=85)
        
        Cart_Frame=Frame(Calc_cart_Frame,bd=2.5,relief=RIDGE)
        Cart_Frame.place(x=5,y=200,width=485,height=190)
        self.Cart_Title=Label(Cart_Frame,text='Cart \t Total Products : [0]',font=('goudy old style',15,'bold'))
        self.Cart_Title.pack(side=TOP,fill=X)
        scrolly2=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx2=Scrollbar(Cart_Frame,orient=HORIZONTAL)
        self.CartTable=ttk.Treeview(Cart_Frame,columns=('pid','pname','price','qty'),yscrollcommand=scrolly2.set,xscrollcommand=scrollx2.set)
        scrollx2.pack(side=BOTTOM,fill=X)
        scrolly2.pack(side=RIGHT,fill=Y)

        scrollx2.config(command=self.CartTable.xview)
        scrolly2.config(command=self.CartTable.yview)
        self.CartTable.heading('pid',text='Product ID')
        self.CartTable.heading('pname',text='Product Name')
        self.CartTable.heading('price',text='Price')
        self.CartTable.heading('qty',text='Quantity')
        self.CartTable['show']='headings'
        self.CartTable.column('pid',width=90)
        self.CartTable.column('pname',width=90)
        self.CartTable.column('price',width=90)
        self.CartTable.column('qty',width=90)
        self.CartTable.pack(fill=BOTH,expand=1,)
        self.CartTable.bind('<ButtonRelease-1>',self.get_data_cart)

        #Add cart frame
        self.var_pid=StringVar()
        self.var_productname=StringVar()        
        self.var_price_per_qty=StringVar()
        self.var_qty=StringVar()    
        self.var_stock=StringVar()    

        Add_cart_widget_Frame=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        Add_cart_widget_Frame.place(x=510,y=615,width=500,height=110)

        productname=Label(Add_cart_widget_Frame,text='Product Name',font=('goudy old style',15,'bold'),bg='white').place(x=10,y=3,width=160,height=30)
        price_per_qty=Label(Add_cart_widget_Frame,text='Price per QTY',font=('goudy old style',15,'bold'),bg='white').place(x=180,y=3,width=150,height=30)        
        qty=Label(Add_cart_widget_Frame,text='Quantity',font=('goudy old style',15,'bold'),bg='white').place(x=340,y=3,width=150,height=30)        
        
        txt_productname=Entry(Add_cart_widget_Frame,state='readonly',textvariable=self.var_productname,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=10,y=36,width=160,height=30)
        txt_price_per_qty=Entry(Add_cart_widget_Frame,state='readonly',textvariable=self.var_price_per_qty,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=180,y=36,width=150,height=30)        
        txt_qty=Entry(Add_cart_widget_Frame,textvariable=self.var_qty,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=340,y=36,width=150,height=30)        
        
        self.lbl_inStock=Label(Add_cart_widget_Frame,text='In Stock',font=('goudy old style',15,'bold'),bg='white')
        self.lbl_inStock.place(x=10,y=72,height=30,width=160)
        btn_clear_cart=Button(Add_cart_widget_Frame,text='Clear Cart',command=self.clear_cart,font=('goudy old style',15,'bold'),cursor='hand2',bg='darkgrey').place(x=180,y=72,height=30,width=150)
        btn_add_cart=Button(Add_cart_widget_Frame,text='Add/Upadte Cart',command=self.add_update_cart,font=('goudy old style',15,'bold'),cursor='hand2',bg='orange').place(x=340,y=72,height=30,width=150)

        #bill area frame
        bill=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        bill.place(x=1015,y=105,width=500,height=470)
        Btitle=Label(bill,text='Customer Billing Area',font=('goudy old style',20,'bold'),bg='orange',fg='black')
        Btitle.pack(side=TOP,fill=X)

        scrolly3=Scrollbar(bill,orient=VERTICAL,)
        scrolly3.pack(side=RIGHT,fill=Y)
        scrollx3=Scrollbar(bill,orient=HORIZONTAL,)
        scrollx3.pack(side=BOTTOM,fill=X)
        self.txt_bill_area=Text(bill,font=('goudy old style',15,'bold'),yscrollcommand=scrolly3.set,xscrollcommand=scrollx3.set)
        self.txt_bill_area.pack(fill=BOTH,expand=10)
        scrolly3.config(command=self.txt_bill_area.yview)
        scrollx3.config(command=self.txt_bill_area.xview)

        #bill menu frame
        billmenu=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        billmenu.place(x=1015,y=575,width=500,height=150)

        self.lbl_amt=Label(billmenu,text='Bill Amount [0]',font=('goudy old style',15,'bold'),bg='#3f51b5',fg='white')
        self.lbl_amt.place(x=0,y=0,height=37,width=330)
        
        self.lbl_discount=Label(billmenu,text='Discount',font=('goudy old style',15,'bold'),bg='#8bc34a',fg='white')
        self.lbl_discount.place(x=0,y=37,height=38,width=110)
        
        self.var_discount=IntVar()
        self.txt_discount=Entry(billmenu,textvariable=self.var_discount,font=('goudy old style',15,'bold'),bd=2.5,relief=RIDGE,bg='lightyellow')
        self.txt_discount.place(x=110,y=37,height=38,width=110)
        
        btn_set_discount=Button(billmenu,text='Set discount',command=self.bill_updates,font=('goudy old style',15,'bold'),cursor='hand2',bg='red',fg='white').place(x=220,y=37,height=38,width=110)

        self.lbl_tax=Label(billmenu,text='Select GST',font=('goudy old style',15,'bold'),bg='#c1847c',fg='white')
        self.lbl_tax.place(x=0,y=75,height=38,width=110)
       
        self.var_tax=StringVar()
        cmb_tax=ttk.Combobox(billmenu,textvariable=self.var_tax,values=('Select','5% IGST','2.5% CGST\n\t\t    +2.5% SGST','12% IGST','6.0% CGST\n\t\t    +6.0% SGST','18% IGST','9.0% CGST\n\t\t    +9.0% SGST','28% IGST','14% CGST\n\t\t    +14% SGST'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',12))
        cmb_tax.place(x=110,y=75,height=38,width=220)
        cmb_tax.current(0)

        self.values=['Select','5% IGST','2.5% CGST\n\t\t    +2.5% SGST','12% IGST','6.0% CGST\n\t\t    +6.0% SGST','18% IGST','9.0% CGST\n\t\t    +9.0% SGST','28% IGST','14% CGST\n\t\t    +14% SGST']
        
        self.lbl_netpay=Label(billmenu,text='Net Pay [0]',font=('goudy old style',15,'bold'),bg='#607d8b',fg='white')
        self.lbl_netpay.place(x=0,y=113,height=37,width=330)
        
        btn_print=Button(billmenu,text='Print Bill',command=self.print_bill,font=('goudy old style',15,'bold'),cursor='hand2',bg='lightgreen',fg='white').place(x=330,y=50,height=50,width=165)
        
        btn_clear_all=Button(billmenu,text='Clear All',command=self.clear_all,font=('goudy old style',15,'bold'),cursor='hand2',bg='grey',fg='white').place(x=330,y=100,height=50,width=165)
        
        btn_generate=Button(billmenu,text='Generate Bill/\nSave Bill',command=self.generate_bill,font=('goudy old style',15,'bold'),cursor='hand2',bg='#009688',fg='white').place(x=330,y=0,height=50,width=165)

        self.show()
        self.update_date_time()

    #functions
    
    def get_input(self,num):
        xnum=self.var_calc_input.get()+str(num)
        self.var_calc_input.set(xnum)

    def clear_cal(self):
        self.var_calc_input.set('')

    def perform_cal(self):
        result=self.var_calc_input.get()
        self.var_calc_input.set(eval(result))

    def show(self):
        self.var_pname.set('')
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,pname,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_pname.get()=='':
              messagebox.showerror('Error','Search input should be required',parent=self.root)
            else: 
                cur.execute("select pid,pname,price,qty,status from product where pname LIKE '%"+self.var_pname.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror('Error','No record found',parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
    
    def get_data(self,ev):
        f=self.ProductTable.focus()
        content= (self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_productname.set(row[1])
        self.var_price_per_qty.set(row[2])  
        self.lbl_inStock.config(text=f'In Stock [{str(row[3])}]') 
        self.var_stock.set(row[3])
        self.var_qty.set('1') 
    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content= (self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_productname.set(row[1])
        self.var_price_per_qty.set(row[2])
        self.var_qty.set(row[3])   
        self.lbl_inStock.config(text=f'In Stock [{str(row[4])}]') 
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
        if self.var_qty.get() == '':
            messagebox.showerror('Error', 'Quantity is Required')
            return
        elif self.var_productname.get() == '':
            messagebox.showerror('Error', 'Please select a product from the list')
            return
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error','The required quantity is exceeding the quantity in stock',parent=self.root)
        # price_cal = int(self.var_qty.get()) * float(self.var_price_per_qty.get())
        # price_cal = float(price_cal)
        elif int(self.var_qty.get()) <= int(self.var_stock.get()):
            price_cal=self.var_price_per_qty.get()
            cart_data = [self.var_pid.get(), self.var_productname.get(), price_cal, self.var_qty.get(),self.var_stock.get()]

            present = False
            index = -1
            for i, row in enumerate(self.cart_list):
                if self.var_pid.get() == row[0]:
                    present = True
                    index = i
                    break

            if present:
                op = messagebox.askyesno('Confirm', 'Product already added to cart\nDo you want to update the cart')
                if op:
                    if self.var_qty.get() == '0':
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index] = cart_data
            else:
                self.cart_list.append(cart_data)

        self.show_cart()
        self.bill_updates()

    def bill_updates(self):
        self.bill_amt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amt=self.bill_amt+(float(row[2])*int(row[3]))
        self.discount=((self.bill_amt*self.var_discount.get())/100)
        self.net_pay=self.bill_amt-self.discount
        self.lbl_amt.config(text=f'Bill Amount Rs[{str(self.bill_amt)}]')
        self.lbl_netpay.config(text=f'Net Amount Rs[{str(self.net_pay)}]')
        self.Cart_Title.config(text=f'Cart \t Total products: [{str(len(self.cart_list))}]')
        self.gst=0

             
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def calc_tax(self):
        x=self.var_tax.get()
        if x==self.values[1] or x==self.values[2]:
            return 0.05*self.net_pay
        elif x==self.values[3] or x==self.values[4]:
            return 0.12*self.net_pay
        elif x==self.values[5] or x==self.values[6]:
            return 0.18*self.net_pay
        elif x==self.values[7] or x==self.values[8]:
            return 0.28*self.net_pay


    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_ccontact.get()=='':
            messagebox.showerror('Error',f'Customer Details are required',parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror('Error','Cant Generate empty bill\nPlease select some products',parent=self.root)
        elif self.var_tax.get()=='Select':
            messagebox.showerror('Error','Please Select Appropriate Tax',parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved','Bill has been generated and saved',parent=self.root)
            self.chk_print=1
            self.limit()


    def bill_top(self):
        self.invoice=str(time.strftime("%H%M%S"))+str(time.strftime("%d%m%Y"))
        bill_top_template=f'''
\t     SKAD INVENTORY MANAGERS
\tPhone No 8291598930 , Mumbai 400002
{str('='*47)}
Customer Name: {self.var_cname.get()}       
Phone Number: {self.var_ccontact.get()}
Bill No. : {str(self.invoice)}
Date: {str(time.strftime("%d/%m/%Y"))} 
Time: {str(time.strftime("%H:%M:%S"))}
{str('='*47)}
Product Name\t\t\tQTY\tPrice
{str('='*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_template)

    def bill_bottom(self):
        bill_bottom_template=f'''
{str('='*47)}
Bill Amount\t\t\t\tRs.{self.bill_amt}
Discount\t\t\t{self.var_discount.get()}%\tRs.{self.discount}
Sub Total\t\t\t\tRs.{self.net_pay}
GST\t\t      {self.var_tax.get()}\t\tRs.{self.calc_tax()}
{str('='*47)}
Grand Total\t\t\t\tRs.{self.net_pay+self.calc_tax()}
{str('='*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_template)

    def bill_middle(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                cur.execute('Update product set qty=?,status=? where pid=? ',(
                    qty,
                    status,
                    pid,
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        
    def clear_cart(self):
        self.var_pid.set('')
        self.var_productname.set('')
        self.var_price_per_qty.set('')
        self.var_qty.set('')   
        self.lbl_inStock.config(text=f'In Stock ') 
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_ccontact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.Cart_Title.config(text=f'Cart \t Total Products: [0]')
        self.var_pname.set('')
        self.lbl_amt.config(text='Bill Amount [0]')
        self.lbl_netpay.config(text='Net Amount [0]')
        self.var_discount.set('0')
        self.var_tax.set('Select')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        set_time=time.strftime("%I:%M:%S")
        set_date=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Mangement System\t\t Date: {str(set_date)}\t\t Time: {str(set_time)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Priint','Please generate bill to print receipt',parent=self.root)

    def limit(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                pname=row[1]
                cur.execute("SELECT qty, qty_limit FROM product WHERE pid=?", (pid,))
                result = cur.fetchone()
                if result:
                    current_qty = int(result[0])
                    qty_limit = int(result[1])
                    if current_qty < qty_limit:
                        messagebox.showerror('Quantity Alert', f'Quantity for product {pname} is less than quantity limit!', parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to: {str(ex)}', parent=self.root)
        finally:
            con.close()

    def stock_clearance(self):
        pass
    
    def logout(self):
        self.root.destroy()
        os.system('python login.py')


if __name__=="__main__":
    root=Tk()
    obj=BillingClass(root)
    root.mainloop()
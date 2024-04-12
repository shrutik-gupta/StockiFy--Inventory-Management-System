from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from tkcalendar import Calendar,DateEntry
import sqlite3
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x600+260+140")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #Variable declaration
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_category=StringVar()
        self.var_qty=StringVar()
        self.var_price=StringVar()
        self.var_limit=StringVar()
        self.var_supplier=StringVar()
        self.var_expiry=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchText=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        #Product Frame
        productFrame=Frame(self.root,bd=2.5,relief=RIDGE,bg='white')
        productFrame.place(x=10,y=10,height=575,width=550)

        #title
        title=Label(productFrame,text='Product Details',font=('goudy old style',25,'bold'),bg='#0f4d7d',fg='white').pack(side=TOP,fill=X)

        #labels 
        pid=Label(productFrame,text='Product Id',font=('goudy old style',20),bg='white').place(x=10,y=50,height=40,width=200)
        pname=Label(productFrame,text='Product Name',font=('goudy old style',20),bg='white').place(x=10,y=100,height=40,width=200)
        category=Label(productFrame,text='Category',font=('goudy old style',20),bg='white').place(x=10,y=150,height=40,width=200)
        expiry_date=Label(productFrame,text='Expiry Date',font=('goudy old style',20),bg='white').place(x=10,y=200,height=40,width=200)
        qty=Label(productFrame,text='Quantity',font=('goudy old style',20),bg='white').place(x=10,y=250,height=40,width=200)
        price=Label(productFrame,text='Price',font=('goudy old style',20),bg='white').place(x=10,y=300,height=40,width=200)
        set_limit=Label(productFrame,text='Set Limit',font=('goudy old style',20),bg='white').place(x=10,y=350,height=40,width=200)
        supplier=Label(productFrame,text='Supplier',font=('goudy old style',20),bg='white').place(x=10,y=400,height=40,width=200)
        status=Label(productFrame,text='Status',font=('goudy old style',20),bg='white').place(x=10,y=450,height=40,width=200)

        #entry fields and combo box 
        txt_pid=Entry(productFrame,textvariable=self.var_pid,bg='lightyellow',font=('goudy old style',20)).place(x=220,y=50,height=40,width=285)
        txt_pname=Entry(productFrame,textvariable=self.var_pname,bg='lightyellow',font=('goudy old style',20)).place(x=220,y=100,height=40,width=285)       
        cmb_category=ttk.Combobox(productFrame,textvariable=self.var_category,values=self.cat_list,cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',20))
        cmb_category.place(x=220,y=150,height=40,width=285)
        cmb_category.current(0)
        txt_expiry=DateEntry(productFrame,textvariable=self.var_expiry,state='readonly',date_pattern='dd-mm-yyyy',bg='lightyellow',font=('goudy old style',20)).place(x=220,y=200,height=40,width=285)
        txt_qty=Entry(productFrame,textvariable=self.var_qty,bg='lightyellow',font=('goudy old style',20)).place(x=220,y=250,height=40,width=285)
        txt_price=Entry(productFrame,textvariable=self.var_price,bg='lightyellow',font=('goudy old style',20)).place(x=220,y=300,height=40,width=285)       
        txt_set_limit=Entry(productFrame,textvariable=self.var_limit,bg='lightyellow',font=('goudy old style',20)).place(x=220,y=350,height=40,width=285)
        cmb_supplier=ttk.Combobox(productFrame,textvariable=self.var_supplier,values=self.sup_list,cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',20))
        cmb_supplier.place(x=220,y=400,height=40,width=285)
        cmb_supplier.current(0)
        cmb_status=ttk.Combobox(productFrame,textvariable=self.var_status,values=('Select','Active','Inactive'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',20))
        cmb_status.place(x=220,y=450,height=40,width=285)
        cmb_status.current(0)

        #buttons
        btn_save=Button(productFrame,text='Save',command=self.add,font=('goudy old style',20,'bold'),bg='blue',fg='white',cursor='hand2').place(x=5,y=510,width=125,height=45)
        btn_update=Button(productFrame,text='Update',command=self.update,font=('goudy old style',20,'bold'),bg='green',fg='white',cursor='hand2').place(x=140,y=510,width=125,height=45)
        btn_delete=Button(productFrame,text='Delete',command=self.delete,font=('goudy old style',20,'bold'),bg='red',fg='white',cursor='hand2').place(x=280,y=510,width=125,height=45)
        btn_clear=Button(productFrame,text='Clear',command=self.clear,font=('goudy old style',20,'bold'),bg='grey',fg='white',cursor='hand2').place(x=415,y=510,width=125,height=45)

        #search frame
        SearchFrame=LabelFrame(self.root,text="search Product",font=('goudy old style',12,'bold'),bd=2.5,relief=RIDGE,bg="white")
        SearchFrame.place(x=575,y=10,width=650,height=100)

        #options
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=('Select','Pname','Category','Supplier'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',20))
        cmb_search.place(x=10,y=10,width=200,height=50)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchText,font=('goudy old style',20),bg='lightyellow').place(x=220,y=10,width=200,height=50)
        btn_search=Button(SearchFrame,text='Search',command=self.search,font=('goudy old style',20),bg='#4caf50',fg='white',cursor='hand2').place(x=430,y=10,width=200,height=50)

        #view table for product
        prodct_frame=Frame(self.root,bd=2.5,relief=RIDGE)
        prodct_frame.place(x=575,y=110,width=650,height=475)
        scrolly=Scrollbar(prodct_frame,orient=VERTICAL)
        scrollx=Scrollbar(prodct_frame,orient=HORIZONTAL)
        self.ProductTable=ttk.Treeview(prodct_frame,columns=('pid','pname','category','qty','qty_limit','price','supplier','expiry','status'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading('pid',text='Product ID')
        self.ProductTable.heading('pname',text='Product Name')
        self.ProductTable.heading('category',text='Category')
        self.ProductTable.heading('qty',text='Quantity')
        self.ProductTable.heading('qty_limit',text='Min Limit')
        self.ProductTable.heading('price',text='Price')
        self.ProductTable.heading('supplier',text='Supplier')
        self.ProductTable.heading('expiry',text='Expiry Date')
        self.ProductTable.heading('status',text='Status')
        self.ProductTable['show']='headings'
        self.ProductTable.column('pid',width=75,)
        self.ProductTable.column('pname',width=150,)
        self.ProductTable.column('category',width=90,)
        self.ProductTable.column('qty',width=60,)
        self.ProductTable.column('qty_limit',width=60,)
        self.ProductTable.column('price',width=60,)
        self.ProductTable.column('supplier',width=150,)
        self.ProductTable.column('expiry',width=90,)
        self.ProductTable.column('status',width=60,)
        self.ProductTable.pack(fill=BOTH,expand=1,)
        self.ProductTable.bind('<ButtonRelease-1>',self.get_data)

        self.show()
        
    #functions
    def fetch_cat_sup(self):
        self.cat_list.append('Empty')
        self.sup_list.append('Empty')
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute('Select name from category')
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append('Select')
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute('Select name from supplier')
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append('Select')
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        

    def add(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_category.get()=="Select" or self.var_category.get()=="Empty" or self.var_limit.get()=='' or self.var_supplier.get()=='Select' or self.var_supplier.get()=='Empty' or self.var_status.get()=='Select' or self.var_pname.get()=='':
                messagebox.showerror('Error','All fields must be filled',parent=self.root)
            else:
                cur.execute('Select * from product where pid=?',(self.var_pid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror('Error','Product already exists',parent=self.root)
                else:
                    cur.execute("Insert into product (pid,pname,category,qty,qty_limit,price,supplier,expiry,status) values(?,?,?,?,?,?,?,?,?)",
                                    (
                                    int(self.var_pid.get()),
                                    self.var_pname.get(),
                                    self.var_category.get(),
                                    self.var_qty.get(),
                                    self.var_limit.get(),
                                    self.var_price.get(),
                                    self.var_supplier.get(),
                                    self.var_expiry.get(),
                                    self.var_status.get(),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Product details added successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()

    def show(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute('select * from product')
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content= (self.ProductTable.item(f))
        row=content['values']
        #print(row)
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_category.set(row[2])
        self.var_qty.set(row[3])
        self.var_limit.set(row[4])
        self.var_price.set(row[5])
        self.var_supplier.set(row[6])
        self.var_expiry.set(row[7])
        self.var_status.set(row[8])
        
    def update(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_category.get()=="Select" or self.var_category.get()=="Empty" or self.var_limit.get()=='' or self.var_supplier.get()=='Select' or self.var_supplier.get()=='Empty' or self.var_status.get()=='Select' or self.var_pname.get()=='':
                messagebox.showerror('Error','All fields must be filled',parent=self.root)
            else:
                cur.execute('Select * from product where pid=?',(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Product',parent=self.root)
                else:
                    cur.execute("Update product set pname=?,category=?,qty=?,qty_limit=?,price=?,supplier=?,expiry=?,status=? where pid=?",
                                    (
                                    self.var_pname.get(),
                                    self.var_category.get(),
                                    self.var_qty.get(),
                                    self.var_limit.get(),
                                    self.var_price.get(),
                                    self.var_supplier.get(),
                                    self.var_expiry.get(),
                                    self.var_status.get(),
                                    self.var_pid.get(),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Product details updated successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()

    def delete(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror('Error','Select product from the list',parent=self.root)
            else:
                cur.execute('Select * from product where pid=?',(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Product',parent=self.root)
                else:
                    op=messagebox.askyesno('Confirm','Do you really want to delete?',parent=self.root)
                    if op==True:
                        cur.execute('delete from product where pid=?',(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo('Delete','Product Details Deleted Succesfully',parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def clear(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_category.set('Select')
        self.var_qty.set('')
        self.var_limit.set('')
        self.var_price.set('')
        self.var_supplier.set('Select')
        self.var_expiry.set('')
        self.var_status.set('Select')
        self.var_searchText.set('')
        self.var_searchby.set('Select')
        self.show()
    
    def search(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=='Select':
                messagebox.showerror('Error','Select search by option',parent=self.root)
            elif self.var_searchText.get()=='':
              messagebox.showerror('Error','Search input should be required',parent=self.root)
            else: 
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchText.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror('Error','No record found',parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()
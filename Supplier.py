from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x600+260+140")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")
        self.root.focus_force()

        style = ttk.Style()
        style.configure("Treeview", rowheight=60)

        self.var_searchby=StringVar()
        self.var_serachText=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_sname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        

        #search frame
        

        #options
        lbl_serach=Label(self.root,text='Search by Invoice No :',bg='white',cursor='hand2',font=('goudy old style',15))
        lbl_serach.place(x=500,y=100,width=210,height=30)

        txt_search=Entry(self.root,textvariable=self.var_serachText,font=('goudy old style',15),bg='lightyellow').place(x=720,y=100,width=210,height=30)
        btn_search=Button(self.root,text='Search',command=self.serach,font=('goudy old style',15),bg='#4caf50',fg='white',cursor='hand2').place(x=940,y=100,width=210,height=30)

        #title
        title=Label(self.root,text='Supplier Details',font=('goudy old style',20,'bold'),bg='#0f4d7d',fg='white').place(x=50,y=10,width=1150,height=50)

        #content

        #row1
        lbl_sup_invoice=Label(self.root,text='Invoice No',font=('goudy old style',15),bg='white').place(x=50,y=75,width=100,height=40)
        txt_sup_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=('goudy old style',15),bg='lightyellow').place(x=160,y=75,width=300,height=40)
        
        #row2
        lbl_sname=Label(self.root,text='Name',font=('goudy old style',15),bg='white').place(x=50,y=125,width=100,height=40)
        txt_sname=Entry(self.root,textvariable=self.var_sname,font=('goudy old style',15),bg='lightyellow').place(x=160,y=125,width=300,height=40)

        #row3
        lbl_contact=Label(self.root,text='Contact',font=('goudy old style',15),bg='white').place(x=50,y=175,width=100,height=40)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=('goudy old style',15),bg='lightyellow').place(x=160,y=175,width=300,height=40)
        
        #row4
        lbl_email=Label(self.root,text='Email',font=('goudy old style',15),bg='white').place(x=50,y=225,width=100,height=40)
        txt_email=Entry(self.root,textvariable=self.var_email,font=('goudy old style',15),bg='lightyellow').place(x=160,y=225,width=300,height=40)
        
        #row5
        lbl_desc=Label(self.root,text='Description',font=('goudy old style',15),bg='white').place(x=50,y=275,width=100,height=40)
        self.txt_desc=Text(self.root,font=('goudy old style',15),bg='lightyellow')
        self.txt_desc.place(x=160,y=275,width=300,height=150)
        
        btn_save=Button(self.root,text='Save',command=self.add,font=('goudy old style',15),bg='blue',fg='white',cursor='hand2').place(x=50,y=440,width=200,height=40)
        btn_update=Button(self.root,text='Update',command=self.update,font=('goudy old style',15),bg='green',fg='white',cursor='hand2').place(x=260,y=440,width=200,height=40)
        btn_delete=Button(self.root,text='Delete',command=self.delete,font=('goudy old style',15),bg='red',fg='white',cursor='hand2').place(x=50,y=490,width=200,height=40)
        btn_clear=Button(self.root,text='Clear',command=self.clear,font=('goudy old style',15),bg='grey',fg='white',cursor='hand2').place(x=260,y=490,width=200,height=40)

        #view table
        supp_frame=Frame(self.root,bd=3,relief=RIDGE)
        supp_frame.place(x=500,y=150,width=700,height=400)
        scrolly=Scrollbar(supp_frame,orient=VERTICAL)
        scrollx=Scrollbar(supp_frame,orient=HORIZONTAL)
        self.supplierTable=ttk.Treeview(supp_frame,columns=('invoice','name','contact','email','desc'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading('invoice',text='Invoice No')
        self.supplierTable.heading('name',text='Name')
        self.supplierTable.heading('contact',text='Contact')
        self.supplierTable.heading('email',text='Email')
        self.supplierTable.heading('desc',text='Description')
        self.supplierTable['show']='headings'
        self.supplierTable.column('invoice',width=90)
        self.supplierTable.column('name',width=90)
        self.supplierTable.column('contact',width=90)
        self.supplierTable.column('email',width=90)
        self.supplierTable.column('desc',width=90)
        self.supplierTable.pack(fill=BOTH,expand=1,)
        self.supplierTable.bind('<ButtonRelease-1>',self.get_data)

        self.show()

    def add(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror('Error','Invoice is required',parent=self.root)
            else:
                cur.execute('Select * from supplier where invoice=?',(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror('Error','This Invoice No is already assigned',parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,email,desc) values(?,?,?,?,?)",
                                    (
                                    self.var_sup_invoice.get(),
                                    self.var_sname.get(),
                                    self.var_contact.get(),
                                    self.var_email.get(),
                                    self.txt_desc.get('1.0',END),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Supplier details added successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()

    def show(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute('select * from supplier')
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content= (self.supplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0])
        self.var_sname.set(row[1])
        self.var_contact.set(row[2])
        self.var_email.set(row[3])
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[4]),

    def update(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror('Error','Invoice No is required',parent=self.root)
            else:
                cur.execute('Select * from supplier where invoice=?',(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Invoice No',parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,email=?,desc=? where invoice=?",
                                    (
                                    self.var_sname.get(),
                                    self.var_contact.get(),
                                    self.var_email.get(),
                                    self.txt_desc.get('1.0',END),
                                    self.var_sup_invoice.get(),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Supplier details updated successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()

    def delete(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror('Error','Invoice No is required',parent=self.root)
            else:
                cur.execute('Select * from supplier where invoice=?',(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Invoice No',parent=self.root)
                else:
                    op=messagebox.askyesno('Confirm','Do you really want to delete?',parent=self.root)
                    if op==True:
                        cur.execute('delete from supplier where invoice=?',(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo('Delete','Supplier Details Deleted Succesfully',parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def clear(self):
        self.var_sup_invoice.set('')
        self.var_sname.set('')
        self.var_contact.set('')
        self.var_email.set('')
        self.txt_desc.delete('1.0',END),
        self.var_serachText.set('')
        self.show()
    
    def serach(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_serachText.get()=='':
              messagebox.showerror('Error','Invoice No is be required',parent=self.root)
            else: 
                cur.execute("select * from supplier where invoice=?",(self.var_serachText.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror('Error','No record found',parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()

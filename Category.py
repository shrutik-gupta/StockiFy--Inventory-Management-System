from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x600+260+140")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_cat=StringVar()
        self.var_name=StringVar()
        self.var_id=StringVar()

        #title
        lbl_title=Label(self.root,text='Mangage Product Category',font=('goudy old style',30,'bold'),bg='#184a45',fg='white',bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=15,pady=20)
        
        lbl_name=Label(self.root,text='Category Name',font=('goudy old style',15,'bold'),bg='white').place(x=50,y=160,height=50,width=200)
        lbl_name_text=Entry(self.root,textvariable=self.var_name,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=260,y=160,height=50,width=340)

        lbl_id=Label(self.root,text='Category ID',font=('goudy old style',15,'bold'),bg='white').place(x=50,y=100,height=50,width=200)
        lbl_id_text=Entry(self.root,textvariable=self.var_id,font=('goudy old style',15,'bold'),bg='lightyellow').place(x=260,y=100,height=50,width=340)

        btn_add=Button(self.root,text="ADD",command=self.add,font=('goudy old style',15,'bold'),bg='green',fg='white',cursor='hand2').place(x=330,y=220,width=270,height=50)
        btn_delete=Button(self.root,text="DELETE",command=self.delete,font=('goudy old style',15,'bold'),bg='red',fg='white',cursor='hand2').place(x=50,y=220,width=270,height=50)

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=50,y=280,width=550,height=300)
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)
        self.categoryTable=ttk.Treeview(cat_frame,columns=('cid','name'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)
        self.categoryTable.heading('cid',text='Category ID')
        self.categoryTable.heading('name',text='Category')
        self.categoryTable['show']='headings'
        self.categoryTable.column('cid',width=270)
        self.categoryTable.column('name',width=270)
        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind('<ButtonRelease-1>',self.get_data)

        self.image=Image.open("Images/cat.jpg")
        self.image=self.image.resize((550,400),Image.AFFINE)
        self.image=ImageTk.PhotoImage(self.image)
        self.lbl_image=Label(self.root,image=self.image)
        self.lbl_image.place(x=650,y=150)

        self.show()

    def add(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror('Error','Category ID is required',parent=self.root)
            if self.var_name.get()=="":
                messagebox.showerror('Error','Category Name is required',parent=self.root)
            else:
                cur.execute('Select * from category where cid=?',(self.var_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror('Error','This Category Id is already assigned\n Try a different Id',parent=self.root)
                else:
                    cur.execute("Insert into category (cid,name) values(?,?)",
                                    (
                                    self.var_id.get(),
                                    self.var_name.get(),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Category details added successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()
            
    def show(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute('select * from category')
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def get_data(self,ev):
        f=self.categoryTable.focus()
        content= (self.categoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        
    def delete(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror('Error','Category ID is required',parent=self.root)
            if self.var_name.get()=="":
                messagebox.showerror('Error','Category Name is required',parent=self.root)
            else:
                cur.execute('Select * from category where cid=?',(self.var_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Category Id',parent=self.root)
                else:
                    op=messagebox.askyesno('Confirm','Do you really want to delete?',parent=self.root)
                    if op==True:
                        cur.execute('delete from category where cid=?',(self.var_id.get(),))
                        con.commit()
                        messagebox.showinfo('Delete','Category Details Deleted Succesfully',parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def clear(self):
        self.var_id.set('')
        self.var_name.set('')
        self.show()
        
if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()

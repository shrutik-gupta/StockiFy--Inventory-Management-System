from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from tkcalendar import Calendar,DateEntry
import re
import sqlite3
class employeeClass:
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
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()
        self.var_address=StringVar()

        #search frame
        SearchFrame=LabelFrame(self.root,text="Serach Employee",font=('goudy old style',12,'bold'),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=305,y=20,width=640,height=70)

        #options
        cmb_serach=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=('Select','Email','Name','Contact'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',15))
        cmb_serach.place(x=10,y=10,width=200,height=30)
        cmb_serach.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_serachText,font=('goudy old style',15),bg='lightyellow').place(x=220,y=10,width=200,height=30)
        btn_search=Button(SearchFrame,text='Search',command=self.serach,font=('goudy old style',15),bg='#4caf50',fg='white',cursor='hand2').place(x=430,y=10,width=200,height=30)

        #title
        title=Label(self.root,text='Employee Details',font=('goudy old style',15),bg='#0f4d7d',fg='white').place(x=50,y=100,width=1150)

        #content

        #row1
        lbl_empid=Label(self.root,text='Emp ID',font=('goudy old style',15),bg='white').place(x=50,y=150,width=100,height=30)
        lbl_gender=Label(self.root,text='Gender',font=('goudy old style',15),bg='white').place(x=425,y=150,width=100,height=30)
        lbl_contact=Label(self.root,text='Contact',font=('goudy old style',15),bg='white').place(x=800,y=150,width=100,height=30)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=('goudy old style',15),bg='lightyellow').place(x=160,y=150,width=220,height=30)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=('Select','Male','Female','Other'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',15))
        cmb_gender.place(x=535,y=150,width=220,height=30)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=('goudy old style',15),bg='lightyellow').place(x=910,y=150,width=220,height=30)

        #row2
        lbl_name=Label(self.root,text='Name',font=('goudy old style',15),bg='white').place(x=50,y=200,width=100,height=30)
        lbl_dob=Label(self.root,text='D.O.B.',font=('goudy old style',15),bg='white').place(x=425,y=200,width=100,height=30)
        lbl_doj=Label(self.root,text='D.O.J.',font=('goudy old style',15),bg='white').place(x=800,y=200,width=100,height=30)

        txt_name=Entry(self.root,textvariable=self.var_name,font=('goudy old style',15),bg='lightyellow').place(x=160,y=200,width=220,height=30)
        txt_dob=DateEntry(self.root,textvariable=self.var_dob,state='readonly',font=('goudy old style',15),bg='lightyellow',date_pattern='dd-mm-yyyy').place(x=535,y=200,width=220,height=30)
        txt_doj=DateEntry(self.root,textvariable=self.var_doj,state='readonly',font=('goudy old style',15),bg='lightyellow',date_pattern='dd-mm-yyyy').place(x=910,y=200,width=220,height=30)

        #row3
        lbl_email=Label(self.root,text='Email',font=('goudy old style',15),bg='white').place(x=50,y=250,width=100,height=30)
        lbl_pass=Label(self.root,text='Password',font=('goudy old style',15),bg='white').place(x=425,y=250,width=100,height=30)
        lbl_utype=Label(self.root,text='User type',font=('goudy old style',15),bg='white').place(x=800,y=250,width=100,height=30)

        txt_email=Entry(self.root,textvariable=self.var_email,font=('goudy old style',15),bg='lightyellow').place(x=160,y=250,width=220,height=30)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=('goudy old style',15),bg='lightyellow').place(x=535,y=250,width=220,height=30)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=('Admin','Employee'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',15))
        cmb_utype.place(x=910,y=250,width=220,height=30)
        cmb_utype.current(0)

        #row4
        lbl_address=Label(self.root,text='Address',font=('goudy old style',15),bg='white').place(x=50,y=300,width=100,height=30)
        lbl_salary=Label(self.root,text='Salary',font=('goudy old style',15),bg='white').place(x=425,y=300,width=100,height=30)

        self.txt_address=Text(self.root,font=('goudy old style',15),bg='lightyellow')
        self.txt_address.place(x=160,y=300,width=220,height=90)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=('goudy old style',15),bg='lightyellow').place(x=535,y=300,width=220,height=30)

        btn_save=Button(self.root,text='Save',command=self.add,font=('goudy old style',15),bg='blue',fg='white',cursor='hand2').place(x=800,y=300,width=200,height=30)
        btn_update=Button(self.root,text='Update',command=self.update,font=('goudy old style',15),bg='green',fg='white',cursor='hand2').place(x=1010,y=300,width=200,height=30)
        btn_delete=Button(self.root,text='Delete',command=self.delete,font=('goudy old style',15),bg='red',fg='white',cursor='hand2').place(x=800,y=340,width=200,height=30)
        btn_clear=Button(self.root,text='Clear',command=self.clear,font=('goudy old style',15),bg='grey',fg='white',cursor='hand2').place(x=1010,y=340,width=200,height=30)

        #view table
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=400,relwidth=1,height=200)
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        self.EmployeeTable=ttk.Treeview(emp_frame,columns=('eid','name','email','gender','contact','dob','doj','pass','utype','address','salary'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading('eid',text='EmpId')
        self.EmployeeTable.heading('name',text='Name')
        self.EmployeeTable.heading('email',text='Email')
        self.EmployeeTable.heading('gender',text='Gender')
        self.EmployeeTable.heading('contact',text='Contact')
        self.EmployeeTable.heading('dob',text='D.O.B.')
        self.EmployeeTable.heading('doj',text='D.O.J.')
        self.EmployeeTable.heading('pass',text='Password')
        self.EmployeeTable.heading('utype',text='User Type')
        self.EmployeeTable.heading('address',text='Adrress')
        self.EmployeeTable.heading('salary',text='Salary')
        self.EmployeeTable['show']='headings'
        self.EmployeeTable.column('eid',width=50,)
        self.EmployeeTable.column('name',width=90,)
        self.EmployeeTable.column('email',width=170,)
        self.EmployeeTable.column('gender',width=50,)
        self.EmployeeTable.column('contact',width=90,)
        self.EmployeeTable.column('dob',width=90,)
        self.EmployeeTable.column('doj',width=90,)
        self.EmployeeTable.column('pass',width=90,)
        self.EmployeeTable.column('utype',width=90,)
        self.EmployeeTable.column('address',width=90,)
        self.EmployeeTable.column('salary',width=90,)
        self.EmployeeTable.pack(fill=BOTH,expand=1,)
        self.EmployeeTable.bind('<ButtonRelease-1>',self.get_data)

        self.show()

    def add(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror('Error','Employee ID is required',parent=self.root)
            elif not self.validate_password(self.var_pass.get()):
                messagebox.showerror('Error','Password must be at least 8 characters long and contain at least \none uppercase letter, \none lowercase letter, \none digit, and \none special character.',parent=self.root)
            else:
                cur.execute('Select * from employee where eid=?',(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror('Error','This Employee ID  is already assigned\n Try a different Id',parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",
                                    (
                                    self.var_emp_id.get(),
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),
                                    self.var_dob.get(),
                                    self.var_doj.get(),
                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get('1.0',END),
                                    self.var_salary.get(),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Employee details added successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()

    def show(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            cur.execute('select * from employee')
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content= (self.EmployeeTable.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END),
        self.txt_address.insert(END,row[9]),
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror('Error','Employee ID is required',parent=self.root)
            elif not self.validate_password(self.var_pass.get()):
                messagebox.showerror('Error','Password must be at least 8 characters long and contain at least \none uppercase letter, \none lowercase letter, \none digit, and \none special character.',parent=self.root)
            else:
                cur.execute('Select * from employee where eid=?',(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Employee ID',parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",
                                    (
                                    
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),
                                    self.var_dob.get(),
                                    self.var_doj.get(),
                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get('1.0',END),
                                    self.var_salary.get(),
                                    self.var_emp_id.get(),
                                    )
                                )
                    con.commit()
                    messagebox.showinfo('Success',"Employee details updated successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
        self.show()

    def delete(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror('Error','Employee ID is required',parent=self.root)
            else:
                cur.execute('Select * from employee where eid=?',(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Employee ID',parent=self.root)
                else:
                    op=messagebox.askyesno('Confirm','Do you really want to delete?',parent=self.root)
                    if op==True:
                        cur.execute('delete from employee where eid=?',(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo('Delete','Employee Details Deleted Succesfully',parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def clear(self):
        self.var_emp_id.set('')
        self.var_name.set('')
        self.var_email.set('')
        self.var_gender.set('Select')
        self.var_contact.set('')
        self.var_dob.set('')
        self.var_doj.set('')
        self.var_pass.set('')
        self.var_utype.set('Admin')
        self.txt_address.delete('1.0',END),
        self.var_salary.set('')
        self.var_serachText.set('')
        self.var_searchby.set('Select')
        self.show()
    
    def serach(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=='Select':
                messagebox.showerror('Error','Select search by option',parent=self.root)
            elif self.var_serachText.get()=='':
              messagebox.showerror('Error','Search input should be required',parent=self.root)
            else: 
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_serachText.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror('Error','No record found',parent=self.root)
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def validate_password(self, password):
        # Password must be at least 8 characters long
        if len(password) < 8:
            return False
        
        # Password must contain at least one uppercase letter
        if not re.search("[A-Z]", password):
            return False
        
        # Password must contain at least one lowercase letter
        if not re.search("[a-z]", password):
            return False
        
        # Password must contain at least one digit
        if not re.search("[0-9]", password):
            return False
        
        # Password must contain at least one special character
        if not re.search("[!@#$%^&*()-_+=]", password):
            return False
        
        return True

if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()

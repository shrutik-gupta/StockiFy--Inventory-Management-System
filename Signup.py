from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from tkcalendar import Calendar,DateEntry
import re
import sqlite3
class signupClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1000x500+250+150")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_confpass=StringVar()

        
        title=Label(self.root,text='Enter Employee Details',font=('goudy old style',15),bg='#0f4d7d',fg='white').place(x=25,y=10,width=950,height=30)

        # #row1
        lbl_empid=Label(self.root,text='Emp ID',font=('goudy old style',15),bg='white').place(x=25,y=75,width=90,height=40)
        lbl_gender=Label(self.root,text='Gender',font=('goudy old style',15),bg='white').place(x=350,y=75,width=90,height=40)
        lbl_contact=Label(self.root,text='Contact',font=('goudy old style',15),bg='white').place(x=675,y=75,width=90,height=40)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=('goudy old style',15),bg='lightyellow').place(x=125,y=75,width=200,height=40)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=('Select','Male','Female','Other'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',15))
        cmb_gender.place(x=450,y=75,width=200,height=40)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=('goudy old style',15),bg='lightyellow').place(x=775,y=75,width=200,height=40)

        #row2
        lbl_name=Label(self.root,text='Name',font=('goudy old style',15),bg='white').place(x=25,y=150,width=90,height=40)
        lbl_dob=Label(self.root,text='D.O.B.',font=('goudy old style',15),bg='white').place(x=350,y=150,width=90,height=40)
        lbl_doj=Label(self.root,text='D.O.J.',font=('goudy old style',15),bg='white').place(x=675,y=150,width=90,height=40)

        txt_name=Entry(self.root,textvariable=self.var_name,font=('goudy old style',15),bg='lightyellow').place(x=125,y=150,width=200,height=40)
        txt_dob=DateEntry(self.root,textvariable=self.var_dob,state='readonly',font=('goudy old style',15),bg='lightyellow',date_pattern='dd-mm-yyyy').place(x=450,y=150,width=200,height=40)
        txt_doj=DateEntry(self.root,textvariable=self.var_doj,state='readonly',font=('goudy old style',15),bg='lightyellow',date_pattern='dd-mm-yyyy').place(x=775,y=150,width=200,height=40)

        #row3
        lbl_email=Label(self.root,text='Email',font=('goudy old style',15),bg='white').place(x=25,y=225,width=90,height=40)
        lbl_pass=Label(self.root,text='Password',font=('goudy old style',15),bg='white').place(x=350,y=225,width=90,height=40)
        lbl_utype=Label(self.root,text='User type',font=('goudy old style',15),bg='white').place(x=675,y=225,width=90,height=40)

        txt_email=Entry(self.root,textvariable=self.var_email,font=('goudy old style',15),bg='lightyellow').place(x=125,y=225,width=200,height=40)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=('goudy old style',15),bg='lightyellow').place(x=450,y=225,width=200,height=40)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=('Admin','Employee'),cursor='hand2',state='readonly',justify=CENTER,font=('goudy old style',15))
        cmb_utype.place(x=775,y=225,width=200,height=40)
        cmb_utype.current(0)

        #row4
        lbl_address=Label(self.root,text='Address',font=('goudy old style',15),bg='white').place(x=25,y=300,width=90,height=40)
        lbl_confpass=Label(self.root,text='Confirm \npassword',font=('goudy old style',15),bg='white').place(x=350,y=300,width=90,height=50)

        self.txt_address=Text(self.root,font=('goudy old style',15),bg='lightyellow')
        self.txt_address.place(x=125,y=300,width=200,height=90)
        txt_confpass=Entry(self.root,textvariable=self.var_confpass,font=('goudy old style',15),bg='lightyellow').place(x=450,y=300,width=200,height=40)

        btn_submitt=Button(self.root,text='SUBMITT',command=self.submitt,font=('goudy old style',25,'bold'),cursor='hand2',bg='darkred',fg='white')
        btn_submitt.place(x=700,y=325,height=50,width=250)
        btn_clear=Button(self.root,text='CLEAR ALL',command=self.clear,font=('goudy old style',25,'bold'),cursor='hand2',bg='darkgrey',fg='white')
        btn_clear.place(x=700,y=400,height=50,width=250)

        #row5
        lbl_note=Label(self.root,text='NOTE: ALL FIELDS MUST BE FILLED',anchor=W,font=('goudy old style',17,'bold'),bg='white',fg='red').place(x=25,y=410,width=500,height=40)

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
        self.var_confpass.set('')

    def submitt(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="" or self.var_name.get()=='' or self.var_email.get()=='' or self.var_gender.get()=='' or  self.var_contact.get()=='' or self.var_dob.get()=='' or self.var_doj.get()=='' or self.var_pass.get()=='' or self.var_confpass.get()=='':
                messagebox.showerror('Error','All details must be filled',parent=self.root)
            else:
                if self.var_pass.get()!=self.var_confpass.get():
                    messagebox.showerror('Error','Both passwords don\'t match',parent=self.root)
                else:
                    is_valid, message = self.validate_password(self.var_pass.get())
                    if not is_valid:
                        messagebox.showerror('Error', message, parent=self.root)
                        return
                    cur.execute('Select * from employee where eid=?',(self.var_emp_id.get(),))
                    row1=cur.fetchone()
                    if row1!=None:
                        messagebox.showerror('Error','This Employee ID  is already assigned\n Try a different Id',parent=self.root)
                    
                    cur.execute('Select * from employee where email=?',(self.var_email.get(),))
                    row2=cur.fetchone()
                    if row2!=None:
                        messagebox.showerror('Error','This Email ID  is already assigned\n Try a different Email Id',parent=self.root)
                    
                    cur.execute('Select * from employee where contact=?',(self.var_contact.get(),))
                    row3=cur.fetchone()
                    if row3!=None:
                        messagebox.showerror('Error','This Contact is already assigned\n Try a different Contact',parent=self.root)
                    
                    if self.var_pass.get()!=self.var_confpass.get():
                        messagebox.showerror('Error','Both passwords dont match',parent=self.root)
                    else:
                        cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address) values(?,?,?,?,?,?,?,?,?,?)",
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
                                        )
                                    )
                        con.commit()
                        messagebox.showinfo('Success',"Employee details added successfully",parent=self.root)
                        self.root.destroy()
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)
    
    def validate_password(self, password):
        # Check for minimum length
        if len(password) < 8:
            return False, "Password must be at least 8 characters long, must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        
        # Check for complexity
        if not re.search("[a-z]", password) or \
           not re.search("[A-Z]", password) or \
           not re.search("[0-9]", password) or \
           not re.search("[!@#$%^&*()_+]", password):
            return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        
        return True, "Password is valid."

if __name__=="__main__":
    root=Tk()
    obj=signupClass(root)
    root.mainloop()
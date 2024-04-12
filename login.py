from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
import re
from Signup import signupClass
class Login_system:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x775+0+0")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="#fafafa")

        self.otp=''

        self.var_employee_id=StringVar()
        self.var_password=StringVar()

        self.phone_image=ImageTk.PhotoImage(file='Images/phone.png')
        self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=300,y=50)

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        login_frame.place(x=800,y=90,width=400,height=500)

        title=Label(login_frame,text='Login System',font=('Elephant',30,'bold'),bg='white').place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,anchor='sw',text='Employee ID',font=('Andalus',15),bg='white',fg='#767171')
        lbl_user.place(x=50,y=100,height=40,width=200)
        txt_user=Entry(login_frame,textvariable=self.var_employee_id,font=('times new roman',15),bg='#ECECEC')
        txt_user.place(x=50,y=150,height=40,width=300)

        lbl_password=Label(login_frame,anchor='sw',text='Password',font=('Andalus',15),bg='white',fg='#767171')
        lbl_password.place(x=50,y=200,height=40,width=200)
        txt_password=Entry(login_frame,textvariable=self.var_password,show='*',font=('times new roman',15),bg='#ECECEC')
        txt_password.place(x=50,y=250,height=40,width=300)

        btn_login=Button(login_frame,text='Login',command=self.login,cursor='hand2',font=('Arial Rounded MT Bold',15),bg='#00B0F0',fg="white")
        btn_login.place(x=50,y=315,height=40,width=300)

        OR_lbl1=Label(login_frame,bg='lightgrey',)
        OR_lbl1.place(x=50,y=390,height=2,width=300)
        OR_lbl2=Label(login_frame,bg='white',fg='lightgrey',text='OR',font=('times new roman',15,'bold'))
        OR_lbl2.place(x=175,y=375)

        btn_forgot=Button(login_frame,text='Forgot Password?',command=self.forgot_pass,font=('times new roman',13),bg='white',fg='#00759E',cursor='hand2',bd=0,activebackground='white',activeforeground='#00759E')
        btn_forgot.place(x=50,y=425,height=40,width=300)

        signup_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        signup_frame.place(x=800,y=600,width=400,height=75)

        lbl_signup=Label(signup_frame,text="Don't have an account?",anchor='e',font=('times new roman',15),bg='white')
        lbl_signup.place(x=50,y=25,height=25,width=200)
        btn_signup=Button(signup_frame,text='SignUp',command=self.signup,anchor='w',font=('times new roman',15),bg='white',fg='#00759E',cursor='hand2',bd=0,activebackground='white',activeforeground='#00759E')
        btn_signup.place(x=250,y=25,height=25,width=100)

        self.im1=ImageTk.PhotoImage(file='images/im1.png')
        self.im2=ImageTk.PhotoImage(file='images/im2.png')
        self.im3=ImageTk.PhotoImage(file='images/im3.png')

        self.lbl_change_image=Label(self.root,bg='white')
        self.lbl_change_image.place(x=467,y=153,width=240,height=428)
        self.animate()

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)
    
    def login(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            if self.var_employee_id.get()=='' or self.var_password.get()=='':
                messagebox.showerror('Error','All ifelds must be filled',parent=self.root)
            else:
                cur.execute('select utype from employee where eid=? AND pass=?',(self.var_employee_id.get(),self.var_password.get()))
                user=cur.fetchone()
                if user==None:
                   messagebox.showerror('Error','Invalid login credentials\nTry again',parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python Dashboard.py")
                    else:
                        self.root.destroy()
                        os.system('python billing.py') 
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

        # if self.var_employee_id.get()=='' or self.var_password.get()=='':
        #     messagebox.showerror('Error','All field must be filled',parent=self.root)
        # elif self.var_employee_id.get()!='SKAD' or self.var_password.get()!='skad@20/07/23':
        #     messagebox.showerror('Error','Password and Username dont match\nTry again',parent=self.root)
        # else:
        #     messagebox.showinfo('Information',f'Welcome back: {self.var_employee_id.get()}\nYour password: {self.var_password.get()}')
            
    def forgot_pass(self):
        con=sqlite3.connect(database=r'IMS.db')
        cur=con.cursor()
        try:
            
            if str(self.var_employee_id.get())=='':
                messagebox.showerror('Error','Employee ID is required',parent=self.root)
            else:
                cur.execute('select email from employee where eid=?',(self.var_employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error','Invalid Employee ID',parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror('Error','Connection Error,try again',parent=self.root)
                    else:
                        self.forget_window=Toplevel(self.root)
                        self.forget_window.title('Reset password')
                        self.forget_window.geometry('400x350+600+100')
                        self.forget_window.focus_force()

                        title=Label(self.forget_window,text='Reset Password',font=('goudy old style',15,'bold'),bg='#3f51b5',fg='white').pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_window,text='Enter OTP Sent on Registered Email',font=('times new roman',15)).place(x=20,y=60)
                        txt_resest=Entry(self.forget_window,textvariable=self.var_otp,font=('times new roman',15),bg='lightyellow')
                        txt_resest.place(x=20,y=100,height=30,width=250)
                        self.btn_reset=Button(self.forget_window,text='SUBMIT',command=self.validate_otp,cursor='hand2',font=('times new roman',15),bg='lightblue')
                        self.btn_reset.place(x=280,y=100,width=100,height=30)
                        
                        lbl_new_pass=Label(self.forget_window,text='New Password',font=('times new roman',15))
                        lbl_new_pass.place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_window,textvariable=self.var_new_pass,font=('times new roman',15),bg='lightyellow')
                        txt_new_pass.place(x=20,y=190,width=250,height=30)
                        
                        lbl_conf_pass=Label(self.forget_window,text='Confirm Password',font=('times new roman',15))
                        lbl_conf_pass.place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_window,textvariable=self.var_conf_pass,font=('times new roman',15),bg='lightyellow')
                        txt_conf_pass.place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_window,text='UPDATE',command=self.update_pass,state=DISABLED,cursor='hand2',font=('times new roman',15),bg='lightblue')
                        self.btn_update.place(x=150,y=300,width=100,height=30)
                    
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_
        s.login(email_,pass_)
        self.otp=(int(time.strftime("%H%S%M"))+int(time.strftime('%S')))
        subj="IMS-Reset password OTP"
        msg=f'Dear Sir/Mam, \n\nYour verification OTP is {str(self.otp)}\n\nWith Regards,\nIMS Team '
        msg='Subject:{}\n\n{}'.format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
        
    def update_pass(self):
        if self.var_new_pass.get()=='' or self.var_conf_pass.get()=='':
            messagebox.showerror('Error','Both fields must be filled',parent=self.forget_window)
        
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror('Error','New Password and Confirm Password should be same',parent=self.forget_window)
        else:
            is_valid, message = self.validate_password(self.var_new_pass.get())
            if not is_valid:
                messagebox.showerror('Error', message, parent=self.forget_window)
                return
            con=sqlite3.connect(database=r'IMS.db')
            cur=con.cursor()
            try:
                cur.execute('Update employee SET pass=? where eid=? ',(self.var_new_pass.get(),self.var_employee_id.get()))
                con.commit()
                messagebox.showinfo('Success','Password updated successfully',parent=self.forget_window)
                self.forget_window.destroy()
            except Exception as ex:
                messagebox.showerror('Error',f'Error due to: {str(ex)}',parent=self.root)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
            messagebox.showinfo('Success','OTP verified successfully\nPlease set your new password',parent=self.forget_window)
        else:
            messagebox.showerror('Error','Invalid OTP\nTry Again',parent=self.forget_window)

    def validate_password(self, password):
        # Check for minimum length
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        
        # Check for complexity
        if not re.search("[a-z]", password) or \
           not re.search("[A-Z]", password) or \
           not re.search("[0-9]", password) or \
           not re.search("[!@#$%^&*()_+]", password):
            return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        
        # Check against common passwords (optional)
        common_passwords = ['password', '123456', 'qwerty']  # Add more common passwords if needed
        if password.lower() in common_passwords:
            return False, "Password is too common. Please choose a different one."

        return True, "Password is valid."

    def signup(self):
        self.__new__win=Toplevel(self.root)
        self.new_obj=signupClass(self.__new__win)

root=Tk()
obj=Login_system(root)
root.mainloop()

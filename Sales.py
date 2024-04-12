from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x600+260+140")
        self.root.title("Inventory Management System | Developed by SKAD")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar()

        #title
        lbl_title=Label(self.root,text='View Customers Bill',font=('goudy old style',30,'bold'),bg='#184a45',fg='white',bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=15,pady=20)

        lbl_invoice=Label(self.root,text='Invoice No',font=('goudy old style',20,'bold'),bg='white',anchor=E).place(x=10,y=100,height=50,width=150)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=('goudy old style',20,'bold'),bg='lightyellow').place(x=170,y=100,height=50,width=250)

        btn_serach=Button(self.root,text='Search',command=self.serach,font=('goudy old style',20,'bold'),bg='#2196f3',fg='white',cursor='hand2').place(x=430,y=100,height=50,width=175)
        btn_clear=Button(self.root,text='Clear',command=self.clear,font=('goudy old style',20,'bold'),bg='lightgrey',fg='black',cursor='hand2').place(x=615,y=100,height=50,width=175)

        #bill list
        salesFrame=Frame(self.root,bd=2.5,relief=RIDGE)
        salesFrame.place(x=20,y=160,width=300,height=420)

        scrolly=Scrollbar(salesFrame,orient=VERTICAL)
        self.Sales_list=Listbox(salesFrame,font=('goudy old style',15),bg='white',yscrollcommand=scrolly)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_list.yview)
        self.Sales_list.pack(fill=BOTH,expand=1)
        self.Sales_list.bind('<ButtonRelease-1>',self.get_data)

        #bill area
        billFrame=Frame(self.root,bd=2.5,relief=RIDGE)
        billFrame.place(x=330,y=160,width=460,height=420)

        lbl_bill_area_title=Label(billFrame,text='Customers Bill Area',font=('goudy old style',20),bg='orange').pack(side=TOP,fill=X)


        scrolly2=Scrollbar(billFrame,orient=VERTICAL)
        self.bill_area=Text(billFrame,font=('goudy old style',13),bg='lightyellow',yscrollcommand=scrolly2)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        self.Sales_logo=Image.open("Images/sales.jpg")
        self.Sales_logo=self.Sales_logo.resize((440,400),Image.Resampling.LANCZOS)
        self.Sales_logo=ImageTk.PhotoImage(self.Sales_logo)

        lbl_image=Label(self.root,image=self.Sales_logo)
        lbl_image.place(x=800,y=145)

        self.show()
        
    def show(self):
        del self.bill_list[:]
        self.Sales_list.delete(0,END)  
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])
    
    def get_data(self,ev):
        index_=self.Sales_list.curselection()
        file_name=self.Sales_list.get(index_)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()
    
    def serach(self):
        if self.var_invoice.get()=='':
            messagebox.showerror('Error','Invoice No is required',parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror('Error','Invalid Invoice No',parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)

if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()

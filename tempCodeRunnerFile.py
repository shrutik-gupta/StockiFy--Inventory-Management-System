self.Sales_logo=Image.open("Images/invoice.png")
        self.Sales_logo=self.Sales_logo.resize((400,400),Image.Resampling.LANCZOS)
        self.Sales_logo=ImageTk.PhotoImage(self.Sales_logo)

        lbl_image=Label(self.root,image=self.Sales_logo)
        lbl_image.place(x=10,y=165)
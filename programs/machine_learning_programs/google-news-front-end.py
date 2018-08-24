from Tkinter import *
import tkMessageBox
import google_news_source_extraction as g_news
def show_articles():
    #e1.delete(0)
    T.delete(0.0,END)
    res=g_news.query(e1.get())
    for e in res:
        if e is not None:
            T.insert(END,e+"\n\n\n\n")
master=Tk()
"""L1=Label(master, text="GOOGLE NEWS",font=("Helvetica", 16),fg='red').grid(row=0,column=20)
#FOR NEWS CATEGORY
e1 = Entry(master,width=30)
e1.pack(side=TOP)
e1.grid(row=0, column=21)"""



Label(master, text="GOOGLE NEWS",font=("Helvetica", 16),fg='BLACK').grid(row=0,column=35,sticky=E+W+N+S)
label1=Label(master, text="SEARCH",font=("ARIAL", 16),fg='PURPLE').grid(row=2,column=30)
#label2=Label(master, text="Second").grid(row=1, sticky=W)
e1 = Entry(master,width=70,font=25)
#e2 = Entry(master)

e1.grid(row=2, column=35,sticky=E,ipady=6)

#e2.grid(row=1, column=1)
#label1.grid(sticky=E)
#label2.grid(sticky=E)

#e1.grid(row=0, column=1)
#e2.grid(row=1, column=1)
click_button=Button(master, text='Extract Articles',width=25, command=show_articles).grid(row=12, column=35, pady=4,sticky=S)
#click_button.grid(columnspan=2, sticky=W)



#l=Listbox(master,width=80,height=20,selectmode=BROWSE)
#l.pack()
#l.grid(row=16,column=35,sticky=S)
#l.insert(END, "a list entry")


T = Text(master, height=20, width=70)
T.grid(row=13,column=35,columnspan=1,rowspan=3,sticky=(N))
S=Scrollbar(master)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
S.grid(padx=5,row=13,column=36,sticky='ns',rowspan=3)




#for related categories
"""S = Scrollbar(master)
T = Text(master, height=80, width=80)
#S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
T.grid(row=13,column=30,)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
S.grid(row=18,column=31,sticky='S')"""


#related_categories=Button(master, text='Search',width=25, command=show_entry_fields).grid(row=2, column=22, pady=4)
mainloop()
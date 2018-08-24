from Tkinter import *
import tkMessageBox
import domain_to_category as dom
def show_wikipedia_suggessions():
    res=dom.wiki_result(e2.get())
    if len(res)>0:
        T3.delete(0.0,END)
        T3.insert(END,res)
    else:
        tkMessageBox.showinfo("","No info found\n Please enter valid Entity")
        T3.delete(0.0,END)

def show_entry_fields():
   print("Entered category is", (e1.get()))
   res=dom.result(e1.get())
   T.delete(0.0,END)
   T1.delete(0.0,END)
   #e2.delete(0.0,END)
   T2.delete(0.0,END)
   T3.delete(0.0,END)
   try:
        if len(res[0])>0:
            T.insert(END,res[0]+'\n')
        if len(res[1])>0:
            T.insert(END,res[1]+'\n')
        T2.insert(END,res[3])
   except:
       if len(res[3])>0:
            T2.insert(END,res[3])
       else:
           T2.insert(END,"Sorry No Suggessions Found")
           #tkMessageBox.showinfo("","Please Enter Correct Category\n Check Suggessions Box")
       if (len(res[0])==0) and (len(res[1])==0)and len(res[2])==0:
           tkMessageBox.showinfo("","Please Enter Correct Category\n Check Suggessions Box")
       if (len(res[0])==0) and (len(res[1])==0)and len(res[2])>0:
           tkMessageBox.showinfo("","No related categories found \n Check Suggessions Box and news sources")
       pass
   #wikipedia suggessions for category
   try:
        res1=dom.wiki_result(e1.get())
        T3.insert(END,res1)
   except:
       pass


def show_related_news_sources():
    print "news sources are"
    res=dom.result(e1.get())
    T1.delete(0.0,END)
    T1.insert(END,res[2]+'\n')


master = Tk()

L1=Label(master, text="ENTER NEWS CATEGORY",font=("Helvetica", 16),fg='red').grid(row=0,column=22)
L2=Label(master, text="RELATED CATEGORIES",font=("Helvetica", 12),fg='blue').grid(row=8,column=20)
L3=Label(master, text="NEWS SOURCES",font=("Helvetica", 12),fg='blue').grid(row=8,column=51)
L4=Label(master, text="SUGGESSIONS",font=("Helvetica", 12),fg='blue').grid(row=8,column=22)
L5=Label(master, text="WIKIPEDIA BASED SUGGESSIONS",font=("Helvetica", 12),fg='blue').grid(row=8,column=24)
L6=Label(master, text="ENTER NEWS ENTITY",font=("Helvetica", 16),fg='red').grid(row=0,column=24)
#L7=Label(master, text="ENTER NEWS SOURCE",font=("Helvetica", 16),fg='red').grid(row=60,column=23)

#FOR NEWS CATEGORY
e1 = Entry(master,width=30)
e1.pack(side=TOP)
e1.grid(row=1, column=22)

#FOR ENTITY
e2 = Entry(master,width=30)
e2.pack(side=TOP)
e2.grid(row=1, column=24)

#FOR NEWS SOURCE
"""e3 = Entry(master,width=30)
e3.pack(side=TOP)
e3.grid(row=61, column=23)"""

#for related categories
S = Scrollbar(master)
T = Text(master, height=20, width=20)
#S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
T.grid(row=9,column=20)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
S.grid(row=9,column=21,sticky='ns')

#for news sources
S1 = Scrollbar(master)
T1 = Text(master, height=20, width=50)
#S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
T1.grid(row=9,column=51)
S1.config(command=T1.yview)
T1.config(yscrollcommand=S1.set)
S1.grid(row=9,column=55,sticky='ns')

#for suggessions
S2 = Scrollbar(master)
T2 = Text(master, height=20, width=32)
#S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
T2.grid(row=9,column=22)
S2.config(command=T2.yview)
T2.config(yscrollcommand=S2.set)
S2.grid(row=9,column=23,sticky='ns')
#quit_button.grid(row=2, column=22, sticky=W, pady=4)
#quit_button.pack(side=LEFT, padx=5, pady=5)

#wikipedia suggessions
S3 = Scrollbar(master)
T3 = Text(master, height=20, width=32)
#S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
T3.grid(row=9,column=24)
S3.config(command=T3.yview)
T3.config(yscrollcommand=S3.set)
S3.grid(row=9,column=25,sticky='ns')


#for news sources categories
"""S4 = Scrollbar(master)
T4 = Text(master, height=20, width=32)
#S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
T4.grid(row=9,column=24)
S4.config(command=T4.yview)
T4.config(yscrollcommand=S4.set)
S4.grid(row=66,column=24,sticky='ns')"""


related_categories=Button(master, text='Show Related Categories',width=25, command=show_entry_fields).grid(row=2, column=22, pady=4)

entity_categories=Button(master, text='Show Entity suggessions',width=25, command=show_wikipedia_suggessions).grid(row=2, column=24, pady=4)
#related_categories.pack(side=LEFT, padx=5, pady=5)

sources=Button(master, text='Show News Sources',width=25, command=show_related_news_sources).grid(row=3, column=23, pady=4)
#sources.grid(row=2, column=21, sticky=W, pady=4)
quit_button=Button(master, text='Quit', command=master.quit).grid(row=0, column=80,pady=4)
mainloop()
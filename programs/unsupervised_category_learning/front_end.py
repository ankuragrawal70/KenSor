from Tkinter import *
#import domain_to_category as dom
class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"


    def output_categories(self,inp):
        value=inp.get()
        print 'input category is',value

    def createWidgets(self):
        self.my_text_box=Label(text="User Category or Entity")
        self.my_text_box.pack(side = TOP)

        self.category_input = Entry(bd =5)
        self.category_input.pack(side = TOP)
        #self.category_input["command"]=self.output_categories
        print 'data is',self.category_input.get()

        self.QUIT = Button(self)
        #self.QUIT= Text(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack(side=BOTTOM)


        """T = Text(root, height=2, width=30)
        T.pack()
        T.insert(END, " ")

        S = Scrollbar(root)
        T = Text(root, height=4, width=50)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)"""
        #canvas = Canvas(1000, 1000)
        #canvas.pack()
        #canvas.create_text(200, 200, text="Example Text")

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side=BOTTOM)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.category_input=None
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
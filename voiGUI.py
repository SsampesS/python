import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):     
        self.frame = tk.LabelFrame(text="VOI SCOOTER LOOKUP")
        self.frame.pack(fill="x",expand="yes")
        
        self.entry = tk.Entry(self.frame, text="Hello World\n(click me)")
        self.entry.pack(side="left")

        self.quit = tk.Button(self.frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


root = tk.Tk()
root.geometry("600x800")
app = Application(master=root)
app.mainloop()

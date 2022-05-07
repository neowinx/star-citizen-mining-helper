#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class MainguiApp:
    def __init__(self, master=None):
        # build ui
        self.mainFrame = tk.Frame(master)
        self.mineralsFrame = tk.Frame(self.mainFrame)
        self.mineralsFrame.configure(background="#000000", height="200", width="200")
        self.mineralsFrame.pack(expand="true", fill="both", side="top")

        self.logsFrame = tk.Frame(self.mainFrame)

        self.text1 = tk.Text(self.logsFrame)
        self.text1.configure(
            exportselection="true", height="10", relief="flat", state="normal"
        )
        self.text1.configure(
            tabstyle="tabular", takefocus=False, undo="false", width="50"
        )
        self.text1.pack(expand="true", fill="both", side="left")
        self.text1.bind("<1>", self.callback, add="")

        self.logsFrame.configure(height="200", width="200")
        self.logsFrame.pack(expand="true", fill="both", side="right")
        
        self.mainFrame.configure(height="200", width="200")
        self.mainFrame.pack(side="top")

        # Main widget
        self.mainwindow = self.mainFrame

    def run(self):
        self.mainwindow.mainloop()

    def callback(self, event=None):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MainguiApp(root)
    app.run()

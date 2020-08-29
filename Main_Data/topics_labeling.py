import tkinter as tk
import tkinter.font as tkFont


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.data = self.load()
        self.res = []
        self.index = 0
        self.text = self.data[0]

        self.create_widgets()

    def load(self):
        with open('topics.txt') as f:
            return f.read().split('\n')

    def create_widgets(self):
        fontStyle = tkFont.Font(family="Open sans", size=20)
        self.word = tk.Label(self, text=self.text, width=50, height=10, font=fontStyle)
        self.yes = tk.Button(self, text="Yes", command=lambda: self.go_next(1), width=50, height=5, bg='green')
        self.no = tk.Button(self, text="No", command=lambda: self.go_next(0), width=50, height=5, bg='red')
        self.word.pack(side="top")
        self.yes.pack(side="bottom")
        self.no.pack(side="bottom")

    def go_next(self, yes):
        if len(self.res) < len(self.data):
            self.res.append([self.data[self.index], yes])
            print(self.res[self.index])
            self.index += 1
            try:
                self.word['text'] = self.data[self.index]
            except:
                pass


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

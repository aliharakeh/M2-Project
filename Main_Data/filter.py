import json
import tkinter as tk
import tkinter.font as tkFont


def f():
    count = {}
    with open('kadaas_topics.json', encoding='utf-8') as f:
        data = json.loads(f.read())

    for topics in data.values():
        for topic in topics:
            words = topic.split()
            for w in words:
                if w in count:
                    count[w] += 1
                else:
                    count[w] = 1

    return sorted(count.items(), key=lambda x: x[1], reverse=True)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.data = f()
        self.res = []
        self.index = 0
        self.create_widgets()

    def load(self):
        with open('data_v4.txt') as f:
            return f.read().split('\n')

    def create_widgets(self):
        fontStyle = tkFont.Font(family="Open sans", size=20)
        self.word = tk.Label(self, text=self.data[self.index][0], width=50, height=10, font=fontStyle)
        self.index += 1
        self.yes = tk.Button(self, text="Yes", command=lambda: self.go_next(1), width=50, height=5, bg='green')
        self.no = tk.Button(self, text="No", command=lambda: self.go_next(0), width=50, height=5, bg='red')
        self.word.pack(side="top")
        self.yes.pack(side="bottom")
        self.no.pack(side="bottom")

    def go_next(self, y):
        if y:
            self.res.append(self.data[self.index][0])
        self.word['text'] = self.data[self.index][0]
        self.index += 1


if __name__ == '__main__':
    # root = tk.Tk()
    # app = Application(master=root)
    # app.mainloop()
    #
    # with open('res.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(app.res, indent=2, ensure_ascii=False))

    res = f()
    for r in res:
        print(r)
        print('------------------------')

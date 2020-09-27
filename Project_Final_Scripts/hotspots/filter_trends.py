import json
import tkinter as tk
import tkinter.font as tkFont


def filter_empty_topics():
    with open('hotspots.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    final_hotspots = {}
    for date, hotspot in hotspots.items():
        final_hotspots[date] = {
            **hotspot,
            'trends': []
        }
        for trend in hotspot['trends']:
            if trend['topic']:
                final_hotspots[date]['trends'].append(trend)

    with open('hotspots.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(final_hotspots, indent=2, ensure_ascii=False))


def tkinter_app():
    def flatten_trends():
        with open('hotspots.json', encoding='utf-8') as f:
            hotspots = json.loads(f.read())
        data = set()
        for _, h in hotspots.items():
            for t in h['trends']:
                data.add(t['topic'].strip().lower())
        return list(data)

    class Application(tk.Frame):
        def __init__(self, master=None):
            # initialize
            super().__init__(master)
            self.master = master
            self.pack()

            # widgets
            fontStyle = tkFont.Font(family="Open sans", size=20)
            self.trend = tk.Label(self, text='', width=50, height=10, font=fontStyle)
            self.remove = tk.Button(self, text="remove", command=lambda: self._remove(1), width=50, height=5, bg='red')
            self.keep = tk.Button(self, text="keep", command=lambda: self._remove(0), width=50, height=5, bg='green')

            # positions
            self.trend.pack(side="top")
            self.remove.pack(side="right")
            self.keep.pack(side="left")

            # variables
            self.trends = flatten_trends()
            self.length = len(self.trends)
            self.index = 0
            self.removed_trends = []

        def _remove(self, remove):
            if remove:
                self.removed_trends.append(self.trends[self.index])
            self.index += 1
            if self.index < self.length:
                self.trend['text'] = self.trends[self.index]
            else:
                self.trend['text'] = 'Done!!'

        def save_results(self):
            with open('removed_trends.txt', 'w', encoding='utf-8') as f:
                for t in self.removed_trends:
                    f.write(t + '\n')

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    app.save_results()


if __name__ == '__main__':
    filter_empty_topics()

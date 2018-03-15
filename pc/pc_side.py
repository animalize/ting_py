import re
import datetime

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import pyperclip

import message
from cates import cate_list
from call_tz2txt import getArticle

__all__ = ('pc_main',)

class Gui(ttk.Notebook):
    def __init__(self, root):
        super().__init__(root)
        self.master = root

        # adding Frames as pages for the ttk.Notebook
        # first page, which would get widgets gridded into it
        page1 = ttk.Frame(self)

        page1.rowconfigure(3, weight=1)
        page1.columnconfigure(0, weight=1)
        page1.columnconfigure(1, weight=1)
        page1.columnconfigure(2, weight=1)
        page1.columnconfigure(3, weight=1)
        page1.columnconfigure(4, weight=1)

        # 分类
        self.to_cate = StringVar()
        self.to_cate.set(cate_list[0].code)

        r = Radiobutton(page1, text=cate_list[0].name,
                        variable=self.to_cate, value=cate_list[0].code)
        r.grid(row=0, column=0)

        if cate_list[1] is not None:
            r = Radiobutton(page1, text=cate_list[1].name,
                            variable=self.to_cate, value=cate_list[1].code)
            r.grid(row=0, column=1)

        if cate_list[2] is not None:
            r = Radiobutton(page1, text=cate_list[2].name,
                            variable=self.to_cate, value=cate_list[2].code)
            r.grid(row=0, column=2)

        if cate_list[3] is not None:
            r = Radiobutton(page1, text=cate_list[3].name,
                            variable=self.to_cate, value=cate_list[3].code)
            r.grid(row=0, column=3)

        # 提交
        bt = Button(page1,
                    text='提交',
                    command=self.submit)
        bt.grid(row=0, column=3, columnspan=2)

        # 粘贴标题
        bt = Button(page1,
                    text='粘贴标题',
                    command=self.paste_title,
                    fg='#990000')
        bt.grid(row=1, column=0)
        # 清空标题
        bt = Button(page1,
                    text='清空标题',
                    command=self.clear_title)
        bt.grid(row=1, column=1)
        # 粘贴正文
        bt = Button(page1,
                    text='粘贴正文',
                    command=self.paste_text,
                    fg='#990000')
        bt.grid(row=1, column=2)
        # 清空正文
        bt = Button(page1,
                    text='清空正文',
                    command=self.clear_text)
        bt.grid(row=1, column=3)
        # tz2txt
        bt = Button(page1,
                    text='tz2txt',
                    command=self.tz2txt)
        bt.grid(row=1, column=4)

        # 标题
        self.title = StringVar()
        entry = Entry(page1, textvariable=self.title)
        entry.grid(row=2, column=0, columnspan=5, sticky=W + E)

        # 正文
        self.text = ScrolledText(page1)
        self.text.grid(row=3, column=0, columnspan=5, sticky=W + E + S + N)

        # second page
        page2 = ttk.Frame(self)
        page2.columnconfigure(0, weight=1)
        page2.columnconfigure(1, weight=1)
        page2.columnconfigure(2, weight=0)
        page2.rowconfigure(0, weight=0)
        page2.rowconfigure(1, weight=1)

        # 刷新列表
        bt = Button(page2,
                    text='刷新列表',
                    command=self.get_list)
        bt.grid(row=0, column=1)

        self.tree = ttk.Treeview(page2, selectmode='browse')

        vsb = ttk.Scrollbar(page2, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree["columns"] = ("1", "2", "3", "4")
        self.tree['show'] = 'headings'
        self.tree.column("1", minwidth=50, width=100, stretch=NO)
        self.tree.column("2", minwidth=80, width=150, stretch=NO)
        self.tree.column("3", minwidth=50, width=100, stretch=NO)
        self.tree.column("4", minwidth=50, width=600, stretch=NO)
        self.tree.heading("1", text="分类")
        self.tree.heading("2", text="时间")
        self.tree.heading("3", text="汉字数")
        self.tree.heading("4", text="标题")
        self.tree.grid(row=1, column=0, columnspan=2, sticky=W + E + N + S)
        vsb.grid(row=1, column=3, sticky=N + S)

        self.add(page1, text='文章')
        self.add(page2, text='列表')
        self.pack(expand=1, fill="both")

    def submit(self):
        text = self.text.get("1.0", END).strip()
        if not text:
            return

        title = self.title.get().strip()
        cate = self.to_cate.get()

        r = message.post_article(title, text, cate)
        if r:
            self.clear_title()
            self.clear_text()

    def get_list(self):
        def time_str(t):
               return datetime.datetime.\
                   fromtimestamp(t).strftime('%m-%d %H:%M')

        lst = message.get_list()

        # 删旧的
        self.tree.delete(*self.tree.get_children())

        for d in lst:
            s = (d['cate'], time_str(d['time']), d['cjk_chars'], d['title'])
            self.tree.insert("", 'end', text="L1", values=s)

    def paste_title(self):
        try:
            t = pyperclip.paste().strip()
        except Exception as e:
            print(e)
            return

        t = re.sub(r'[^\u0000-\uFFFF]', '', t)

        self.title.set(t)

    def paste_text(self):
        try:
            t = pyperclip.paste().strip()
        except Exception as e:
            print(e)
            return

        t = re.sub(r'[^\u0000-\uFFFF]', '', t)

        self.text.insert(END, t)

    def clear_title(self):
        self.title.set('')

    def clear_text(self):
        self.text.delete("1.0", END)

    def tz2txt(self):
        url = self.master.clipboard_get().strip()
        title, text = getArticle(url)

        if title == text == '':
            return

        title = re.sub(r'[^\u0000-\uFFFF]', '', title)
        self.title.set(title)

        text = re.sub(r'[^\u0000-\uFFFF]', '', text)
        self.text.delete("1.0", END)
        self.text.insert(END, text)


def pc_main(host=''):
    if host:
        import vars
        vars.host = host
    
    root = Tk()
    root.geometry("780x600")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title('ting PC端')

    gui = Gui(root)

    root.mainloop()


if __name__ == '__main__':
    pc_main()

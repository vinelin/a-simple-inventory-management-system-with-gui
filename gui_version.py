#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.17
# In conjunction with Tcl version 8.6
#    Sep 23, 2018 11:18:07 AM CST  platform: Windows NT

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from icon import img
from header import header
import sqlite3
import os
import base64


class TopLevel_1():
    def __init__(self, top=None):
        top.geometry ("650x450")
        top.title ("进销存系统")
        top.configure (background="#d9d9d9")
        self.Button1 = Button (top)
        self.Button1.bind('<ButtonRelease-1>',lambda e:PurchaseTale())
        self.Button1.place (relx=0.131, rely=0.844, height=50, width=100)
        self.Button1.configure (activebackground="#d9d9d9")
        self.Button1.configure (activeforeground="#000000")
        self.Button1.configure (background="#d9d9d9")
        self.Button1.configure (disabledforeground="#a3a3a3")
        self.Button1.configure (foreground="#000000")
        self.Button1.configure (highlightbackground="#d9d9d9")
        self.Button1.configure (highlightcolor="black")
        self.Button1.configure (pady="0")
        self.Button1.configure (text='''进货表''')
        self.Button2 = Button (top)
        self.Button2.bind('<ButtonRelease-1>',lambda e:SaleTable())
        self.Button2.place (relx=0.415, rely=0.844, height=50, width=100)
        self.Button2.configure (activebackground="#d9d9d9")
        self.Button2.configure (activeforeground="#000000")
        self.Button2.configure (background="#d9d9d9")
        self.Button2.configure (disabledforeground="#a3a3a3")
        self.Button2.configure (foreground="#000000")
        self.Button2.configure (highlightbackground="#d9d9d9")
        self.Button2.configure (highlightcolor="black")
        self.Button2.configure (pady="0")
        self.Button2.configure (text='''销货表''')
        self.Button3 = Button (top)
        self.Button3.bind('<ButtonRelease-1>',lambda e:InventoryTable())
        self.Button3.place (relx=0.708, rely=0.844, height=50, width=100)
        self.Button3.configure (activebackground="#d9d9d9")
        self.Button3.configure (activeforeground="#000000")
        self.Button3.configure (background="#d9d9d9")
        self.Button3.configure (disabledforeground="#a3a3a3")
        self.Button3.configure (foreground="#000000")
        self.Button3.configure (highlightbackground="#d9d9d9")
        self.Button3.configure (highlightcolor="black")
        self.Button3.configure (pady="0")
        self.Button3.configure (text='''库存表''')
        self.Button3.configure (width=500)
        self.Label1 = Label (top)
        self.Label1.place (relx=0.0, rely=0.0, height=300, width=650)
        self.Label1.configure (background="#000000")
        self.Label1.configure (disabledforeground="#a3a3a3")
        self.Label1.configure (foreground="#000000")
        tmp = open ('header.gif', 'wb+')
        tmp.write (base64.b64decode (header))
        tmp.close ()
        self._img1 = PhotoImage (file="header.gif")
        self.Label1.configure (image=self._img1)
        os.remove ('header.gif')

class InventoryTable:
    def add_row(self,event):
        item_id = self.entry1.get ()
        item_name = self.entry2.get ()
        num = self.entry3.get ()
        self.cursor.execute ("select 商品ID from 库存 where 商品ID=?", (item_id,))
        row = self.cursor.fetchone ()
        if not item_id:
            messagebox.showerror (title='错误!', message='商品ID不能为空!')
            return
        if row:
            messagebox.showwarning (title='警告!', message='商品ID已存在!')
            return
        sql = "insert into 库存 values (?,?,?)"
        para = (item_id, item_name, num)
        self.List.insert ('', 'end', values=para)
        self.cursor.execute (sql, para)
        self.conn.commit ()

    def change_row(self,event):
        item_id = self.entry1.get ()
        item_name = self.entry2.get ()
        num = self.entry3.get ()
        para = (item_id, item_name, num)
        self.cursor.execute ("select 商品ID from 库存")
        values = self.cursor.fetchall ()
        if (item_id,) in values:
            messagebox.showwarning (title='警告!', message='商品ID已存在!')
            return
            # if not item_id:
            #     messagebox.showerror(title='错误!', message='商品ID不能为空!')
            return
        # selection方法得到是所选行的一个序号
        iid = self.List.selection ()
        # item方法可以根据行id（iid）查询也可以修改
        ex_id = self.List.item (iid, "value")[0]
        self.List.item (iid, values=para)
        self.cursor.execute ('update 库存 set 商品ID=?,商品名称=?,数量=? where 商品ID=?', (item_id, item_name, num, ex_id))
        self.conn.commit ()

    def delete_row(self,event):
        iid = self.List.selection ()
        item_id = self.List.item (iid, "value")[0]
        self.List.delete (iid)
        self.cursor.execute ('delete from 库存 where 商品ID=?', (item_id,))
        self.conn.commit ()

    def __init__(self):
        #Toplevel()类才能使用grab_set()。。
        self.table = Toplevel()
        self.db_file = os.path.join (os.path.dirname (__file__), 'inventory.db')
        self.conn = sqlite3.connect (self.db_file)
        self.cursor = self.conn.cursor ()
        self.table.title ("库存表")
        self.table.grab_set()
        # ttk Treeview用法 参考 https://segmentfault.com/q/1010000004206667
        # show属性为hedings可隐藏首列，selectmode设置为browse,因此只能单选一行
        self.List = ttk.Treeview (self.table, columns=('col1', 'col2', 'col3'), show='headings', selectmode='browse')
        self.ysb = ttk.Scrollbar (self.table, orient='vertical', command=self.List.yview)
        # 不能使用pack()了
        self.ysb.place (x=583, y=0, height=230)
        self.List.configure (yscrollcommand=self.ysb.set)
        self.List.column ('col1', width=200, anchor='center')
        self.List.column ('col2', width=200, anchor='center')
        self.List.column ('col3', width=200, anchor='center')
        self.List.heading ('col1', text='商品ID')
        self.List.heading ('col2', text='商品名称')
        self.List.heading ('col3', text='商品数量')
        self.List.grid (row=0, column=1, columnspan=3)
        self.entry1 = Entry (self.table)
        self.entry2 = Entry (self.table)
        self.entry3 = Entry (self.table)
        self.entry1.grid (row=1, column=1)
        self.entry2.grid (row=1, column=2)
        self.entry3.grid (row=1, column=3)
        # 若使用bind，则布局必须写在bind后无法会报AttributeError错
        self.button1 = Button (self.table, text='添加')
        self.button1.bind ('<ButtonRelease-1>', self.add_row)
        self.button2 = Button (self.table, text='修改')
        self.button2.bind ('<ButtonRelease-1>', self.change_row)
        self.button3 = Button (self.table, text='删除')
        self.button3.bind ('<ButtonRelease-1>', self.delete_row)
        self.button1.grid (row=2, column=1)
        self.button2.grid (row=2, column=2)
        self.button3.grid (row=2, column=3)
        self.cursor.execute("select * from 库存")
        self.values = self.cursor.fetchall ()
        for row in self.values:
            self.List.insert ('', 'end', values=row)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

class PurchaseTale():
    def add_row(self,event):
        trade_id = self.entry1.get ()
        item_id = self.entry2.get ()
        item_name = self.entry3.get ()
        num = self.entry4.get()
        price = self.entry5.get()
        trade_time = self.entry6.get()
        counterpart = self.entry7.get()
        phone = self.entry8.get()
        self.cursor.execute ("select 交易序号 from 进货 where 交易序号=?", (trade_id,))
        row = self.cursor.fetchone ()
        if not trade_id:
            messagebox.showerror (title='错误!', message='交易序号不能为空!')
            return
        if row:
            messagebox.showwarning (title='警告!', message='这笔交易已存在!')
            return
        sql = "insert into 进货 values (?,?,?,?,?,?,?,?)"
        para = (trade_id, item_id, item_name, num, price, trade_time, counterpart, phone)
        self.List.insert ('', 'end', values=para)
        self.cursor.execute (sql, para)
        # self.cursor.execute ("select 商品ID,数量 from 库存 where 商品ID=?", (item_id,))
        # row = self.cursor.fetchone ()
        # if row:
        #     self.cursor.execute ("update 库存 set 数量=(?+?) where 商品ID=?", (row[1], num, item_id,))
        # else:
        #     self.cursor.execute ("insert into 库存 values (?,?,?)", (item_id, item_name, num))
        self.conn.commit ()

    def change_row(self,event):
        trade_id = self.entry1.get ()
        item_id = self.entry2.get ()
        item_name = self.entry3.get ()
        num = self.entry4.get()
        price = self.entry5.get()
        trade_time = self.entry6.get()
        counterpart = self.entry7.get()
        phone = self.entry8.get()
        para = (trade_id, item_id, item_name, num, price, trade_time, counterpart, phone)
        self.cursor.execute ("select 交易序号 from 进货")
        values = self.cursor.fetchall ()
        if (trade_id,) in values:
            messagebox.showwarning (title='警告!', message='该交易已存在!')
            return
        if not item_id:
            messagebox.showerror(title='错误!', message='交易序号不能为空!')
            return
        iid = self.List.selection ()
        ex_id = self.List.item (iid, "value")[0]
        ex_num = self.List.item (iid, "value")[3]
        self.List.item (iid, values=para)
        self.cursor.execute ('update 进货 set 交易序号=?,商品ID=?,商品名称=?,数量=?,进价=?,交易时间=?,供应商=?,电话=? where 交易序号=?', (trade_id,item_id, item_name, num, price, trade_time, counterpart, phone,ex_id))
        # self.cursor.execute ("select 商品ID,数量 from 库存 where 商品ID=?", (item_id,))
        # row = self.cursor.fetchone ()
        # self.cursor.execute ("update 库存 set 数量=(?-?+?) where 商品ID=?", (row[1], ex_num,num, item_id,))
        self.conn.commit ()

    def delete_row(self,event):
        iid = self.List.selection ()
        trade_id = self.List.item (iid, "value")[0]
        self.List.delete (iid)
        self.cursor.execute ('delete from 进货 where 交易序号=?', (trade_id,))
        self.conn.commit ()

    def __init__(self):
        self.table = Toplevel ()
        self.db_file = os.path.join (os.path.dirname (__file__), 'inventory.db')
        self.conn = sqlite3.connect (self.db_file)
        self.cursor = self.conn.cursor ()
        self.table.title ("进货表")
        self.table.grab_set ()
        self.List = ttk.Treeview (self.table, columns=('col1', 'col2', 'col3','col4','col5','col6','col7','col8'), show='headings', selectmode='browse')
        self.ysb = ttk.Scrollbar (self.table, orient='vertical', command=self.List.yview)
        self.ysb.place (x=1570, y=0, height=230)
        self.List.configure (yscrollcommand=self.ysb.set)
        self.List.column ('col1', width=100, anchor='center')
        self.List.column ('col2', width=100, anchor='center')
        self.List.column ('col3', width=100, anchor='center')
        self.List.column ('col4', width=100, anchor='center')
        self.List.column ('col5', width=100, anchor='center')
        self.List.column ('col6', width=200, anchor='center')
        self.List.column ('col7', width=200, anchor='center')
        self.List.column ('col8', width=200, anchor='center')
        self.List.heading ('col1', text='交易序号')
        self.List.heading ('col2', text='商品ID')
        self.List.heading ('col3', text='商品名称')
        self.List.heading ('col4', text='数量')
        self.List.heading ('col5', text='进价')
        self.List.heading ('col6', text='交易时间')
        self.List.heading ('col7', text='供应商')
        self.List.heading ('col8', text='电话')
        self.List.pack()
        self.entry1 = Entry (self.table)
        self.entry2 = Entry (self.table)
        self.entry3 = Entry (self.table)
        self.entry4 = Entry (self.table)
        self.entry5 = Entry (self.table)
        self.entry6 = Entry (self.table)
        self.entry7 = Entry (self.table)
        self.entry8 = Entry (self.table)
        Label(self.table,text='交易序号').place(x=390,y=230)
        Label (self.table, text='商品ID').place (x=390, y=252)
        Label (self.table, text='商品名称').place (x=390, y=274)
        Label (self.table, text='数量').place (x=390, y=296)
        Label (self.table, text='进价').place (x=390, y=318)
        Label (self.table, text='交易时间').place (x=390, y=340)
        Label (self.table, text='供应商').place (x=390, y=362)
        Label (self.table, text='电话').place (x=390, y=384)
        self.entry1.pack()
        self.entry2.pack()
        self.entry3.pack()
        self.entry4.pack()
        self.entry5.pack()
        self.entry6.pack()
        self.entry7.pack()
        self.entry8.pack()
        self.button1 = Button (self.table, text='添加')
        self.button1.bind ('<ButtonRelease-1>', self.add_row)
        self.button2 = Button (self.table, text='修改')
        self.button2.bind ('<ButtonRelease-1>', self.change_row)
        self.button3 = Button (self.table, text='删除')
        self.button3.bind ('<ButtonRelease-1>', self.delete_row)
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.cursor.execute ("select * from 进货")
        self.values = self.cursor.fetchall ()
        for row in self.values:
            self.List.insert ('', 'end', values=row)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

class SaleTable():
    def add_row(self,event):
        trade_id = self.entry1.get ()
        item_id = self.entry2.get ()
        item_name = self.entry3.get ()
        num = self.entry4.get()
        price = self.entry5.get()
        trade_time = self.entry6.get()
        counterpart = self.entry7.get()
        phone = self.entry8.get()
        self.cursor.execute ("select 交易序号 from 销货 where 交易序号=?", (trade_id,))
        row = self.cursor.fetchone ()
        if not trade_id:
            messagebox.showerror (title='错误!', message='交易序号不能为空!')
            return
        if row:
            messagebox.showwarning (title='警告!', message='这笔交易已存在!')
            return
        sql = "insert into 销货 values (?,?,?,?,?,?,?,?)"
        para = (trade_id, item_id, item_name, num, price, trade_time, counterpart, phone)
        self.List.insert ('', 'end', values=para)
        self.cursor.execute (sql, para)
        # self.cursor.execute ("select 商品ID,数量 from 库存 where 商品ID=?", (item_id,))
        # row = self.cursor.fetchone ()
        # if row:
        #     self.cursor.execute ("update 库存 set 数量=(?+?) where 商品ID=?", (row[1], num, item_id,))
        # else:
        #     self.cursor.execute ("insert into 库存 values (?,?,?)", (item_id, item_name, num))
        self.conn.commit ()

    def change_row(self,event):
        trade_id = self.entry1.get ()
        item_id = self.entry2.get ()
        item_name = self.entry3.get ()
        num = self.entry4.get()
        price = self.entry5.get()
        trade_time = self.entry6.get()
        counterpart = self.entry7.get()
        phone = self.entry8.get()
        para = (trade_id, item_id, item_name, num, price, trade_time, counterpart, phone)
        self.cursor.execute ("select 交易序号 from 销货")
        values = self.cursor.fetchall ()
        if (trade_id,) in values:
            messagebox.showwarning (title='警告!', message='该交易已存在!')
            return
        if not item_id:
            messagebox.showerror(title='错误!', message='交易序号不能为空!')
            return
        iid = self.List.selection ()
        ex_id = self.List.item (iid, "value")[0]
        ex_num = self.List.item (iid, "value")[3]
        self.List.item (iid, values=para)
        self.cursor.execute ('update 销货 set 交易序号=?,商品ID=?,商品名称=?,数量=?,售价=?,交易时间=?,买家=?,电话=? where 交易序号=?', (trade_id,item_id, item_name, num, price, trade_time, counterpart, phone,ex_id))
        # self.cursor.execute ("select 商品ID,数量 from 库存 where 商品ID=?", (item_id,))
        # row = self.cursor.fetchone ()
        # self.cursor.execute ("update 库存 set 数量=(?-?+?) where 商品ID=?", (row[1], ex_num,num, item_id,))
        self.conn.commit ()

    def delete_row(self,event):
        iid = self.List.selection ()
        trade_id = self.List.item (iid, "value")[0]
        self.List.delete (iid)
        self.cursor.execute ('delete from 销货 where 交易序号=?', (trade_id,))
        self.conn.commit ()

    def __init__(self):
        self.table = Toplevel ()
        self.db_file = os.path.join (os.path.dirname (__file__), 'inventory.db')
        self.conn = sqlite3.connect (self.db_file)
        self.cursor = self.conn.cursor ()
        self.table.title ("销货表")
        self.table.grab_set ()
        self.List = ttk.Treeview (self.table, columns=('col1', 'col2', 'col3','col4','col5','col6','col7','col8'), show='headings', selectmode='browse')
        self.ysb = ttk.Scrollbar (self.table, orient='vertical', command=self.List.yview)
        self.ysb.place (x=1570, y=0, height=230)
        self.List.configure (yscrollcommand=self.ysb.set)
        self.List.column ('col1', width=100, anchor='center')
        self.List.column ('col2', width=100, anchor='center')
        self.List.column ('col3', width=100, anchor='center')
        self.List.column ('col4', width=100, anchor='center')
        self.List.column ('col5', width=100, anchor='center')
        self.List.column ('col6', width=200, anchor='center')
        self.List.column ('col7', width=200, anchor='center')
        self.List.column ('col8', width=200, anchor='center')
        self.List.heading ('col1', text='交易序号')
        self.List.heading ('col2', text='商品ID')
        self.List.heading ('col3', text='商品名称')
        self.List.heading ('col4', text='数量')
        self.List.heading ('col5', text='售价')
        self.List.heading ('col6', text='交易时间')
        self.List.heading ('col7', text='买方')
        self.List.heading ('col8', text='电话')
        self.List.pack()
        self.entry1 = Entry (self.table)
        self.entry2 = Entry (self.table)
        self.entry3 = Entry (self.table)
        self.entry4 = Entry (self.table)
        self.entry5 = Entry (self.table)
        self.entry6 = Entry (self.table)
        self.entry7 = Entry (self.table)
        self.entry8 = Entry (self.table)
        Label(self.table,text='交易序号').place(x=390,y=230)
        Label (self.table, text='商品ID').place (x=390, y=252)
        Label (self.table, text='商品名称').place (x=390, y=274)
        Label (self.table, text='数量').place (x=390, y=296)
        Label (self.table, text='售价').place (x=390, y=318)
        Label (self.table, text='交易时间').place (x=390, y=340)
        Label (self.table, text='买方').place (x=390, y=362)
        Label (self.table, text='电话').place (x=390, y=384)
        self.entry1.pack()
        self.entry2.pack()
        self.entry3.pack()
        self.entry4.pack()
        self.entry5.pack()
        self.entry6.pack()
        self.entry7.pack()
        self.entry8.pack()
        self.button1 = Button (self.table, text='添加')
        self.button1.bind ('<ButtonRelease-1>', self.add_row)
        self.button2 = Button (self.table, text='修改')
        self.button2.bind ('<ButtonRelease-1>', self.change_row)
        self.button3 = Button (self.table, text='删除')
        self.button3.bind ('<ButtonRelease-1>', self.delete_row)
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.cursor.execute ("select * from 销货")
        self.values = self.cursor.fetchall ()
        for row in self.values:
            self.List.insert ('', 'end', values=row)

    def __del__(self):
        self.cursor.close()
        self.conn.close()


def open_time():
    db_file = os.path.join (os.path.dirname (__file__), 'inventory.db')
    path = './record.txt'
    with open (path, 'r+', encoding='UTF-8') as text:
        #把数据库文件删除后能重建
        print(not os.path.isfile (db_file))
        if not os.path.isfile (db_file):
            conn = sqlite3.connect (db_file)
            cursor = conn.cursor ()
            text.seek(0)
            text.truncate()
            text.write('0')
        text.seek (0)
        count = text.read()
        num = int (count)
        print(num)
        if num == 0:
            num += 1
            text.seek (0)
            text.truncate ()
            text.write (str (num))
            cursor = conn.cursor ()
            cursor.execute ('''create table 库存 (
            商品ID varchar(20) primary key,
            商品名称 varchar(20),
            数量 int)
            ''')
            cursor.execute ('''create table 进货 (
             交易序号 varchar(20) primary key,
             商品ID varchar(20),
             商品名称 varchar(20),
             数量 int,
             进价 float,
             交易时间 datetime,
             供应商 varchar(20),
             电话 varchar(12))
             ''')
            cursor.execute ('''create table 销货 (
             交易序号 varchar(20) primary key,
             商品ID varchar(20),
             商品名称 varchar(20),
             数量 int,
             售价 float,
             交易时间 datetime,
             买家 varchar(20),
             电话 varchar(12))
             ''')
            conn.commit()
            cursor.close()
        else:
            num += 1
            text.seek (0)
            text.truncate()
            text.write(str(num))


if __name__ == '__main__':
    open_time()
    root = Tk()
    # 将root作为参数传递进去
    main_menu = TopLevel_1(root)
    tmp = open ('tmp.ico', 'wb+')
    tmp.write (base64.b64decode(img))
    tmp.close ()
    root.iconbitmap('tmp.ico')
    os.remove ('tmp.ico')
    mainloop()
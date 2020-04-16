# -*- encoding:utf-8 -*-
"""
Author: Yijie.Wu
Email: 1694517106@qq.com
Date: 2020/4/8 13:13
"""

import os
import time
import sqlite3
import getpass
import requests
import paramiko
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, scrolledtext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'icons')
USER = getpass.getuser()
DEFAULT_LOG_FINDER = '/User/{0}/Desktop/AutoLogs/'.format(USER)
SQLITE_DB = os.path.join(BASE_DIR, 'pen.sqlite')


class Pencil():
    # 初始化函数
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('120x800')
        self.root.resizable(False, False)
        self.sidebar = tk.Frame(self.root)
        self.work_frame = tk.Frame(self.root)
        self.sidebar.place(x=0, y=0, width=120, height=800)
        self.persion_image = tk.PhotoImage(file=os.path.join(ICON_DIR, 'home.png'))
        self.chart_image = tk.PhotoImage(file=os.path.join(ICON_DIR, 'chart.png'))
        self.return_image = tk.PhotoImage(file=os.path.join(ICON_DIR, 'return.png'))
        self.time_label = tk.Label(self.sidebar, text='VxRail OSS', bg='#a6b7c8', font='Monaco 16 bold', fg='gold')
        self.persion_button = tk.Button(self.sidebar, image=self.persion_image, command=self.on_persion_button_clicked)
        self.remain_button = tk.Button(self.sidebar, text='当前遗留', image=self.chart_image, compound='left', command=self.on_remain_button_clicked)
        self.spy_button = tk.Button(self.sidebar, text='寻找开发', image=self.chart_image, compound='left', command=self.on_spy_button_clicked)
        self.release_button = tk.Button(self.sidebar, text='发行伴侣', image=self.chart_image, compound='left', command=self.on_release_button_clicked)
        self.assist_button = tk.Button(self.sidebar, text='辅助对比', image=self.chart_image, compound='left', command=self.on_assist_button_clicked)
        self.help_button = tk.Button(self.sidebar, text='帮助文档', image=self.chart_image, compound='left', command=self.on_help_button_clicked)
        self.setting_button = tk.Button(self.sidebar, text='基础设置', image=self.chart_image, compound='left', command=self.on_settings_button_clicked)
        self.back_button = tk.Button(self.sidebar, text='收起窗口', image=self.return_image, compound='left', command=self.destroy_work_frame)

        self.mail_send_var = tk.IntVar()

    @staticmethod
    def run(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    # 绘制左边功能区
    def drew_ui(self):
        self.root.title('VxRail')
        self.time_label.place(x=0, y=0, width=120, height=30)
        self.persion_button.place(x=5, y=51, width=110, height=110)
        self.remain_button.place(x=5, y=200, width=110, height=40)
        self.spy_button.place(x=5, y=242, width=110, height=40)
        self.release_button.place(x=5, y=284, width=110, height=40)
        self.assist_button.place(x=5, y=326, width=110, height=40)
        self.help_button.place(x=5, y=368, width=110, height=40)
        self.setting_button.place(x=5, y=410, width=110, height=40)
        self.back_button.place(x=5, y=750, width=110, height=40)

    # 绘制右边工作区
    def drew_work_frame(self, width=800, bg='white'):
        self.work_frame = tk.Frame(self.root, bg=bg)
        self.root.geometry('{0}x800'.format(width + 120))
        self.work_frame.place(x=120, y=0, width=width, height=800)

    # 销毁右边工作区
    def destroy_work_frame(self):
        self.root.title('VxRail')
        self.work_frame.destroy()
        self.root.geometry('120x800')

    # 当小人button点击时
    def on_persion_button_clicked(self):
        self.root.title('配置选项')
        self.drew_work_frame(width=800)
        conn = sqlite3.connect(SQLITE_DB)
        corsor = conn.cursor()
        mail_info = corsor.execute('select * from mail where id=1;')
        mail_data = mail_info.fetchone()
        conn.close()

        def on_mail_save_clicked():
            send_mail = self.mail_send_var.get()
            mail_subject = subject_entry.get().strip()
            mail_sender = sender_entry.get().strip()
            mail_receivers = receivers_entry.get().strip()
            mail_message = mail_content.get(0.0, tk.END)

            try:
                sql = 'update mail set send_mail=%d,subject="%s",sender="%s",receivers="%s",content="%s" where id=1;' % (send_mail, mail_subject, mail_sender, mail_receivers, mail_message)
                conn = sqlite3.connect(SQLITE_DB)
                corsor = conn.cursor()
                corsor.execute(sql)
                conn.commit()
                conn.close()
                messagebox.showinfo(title='Mail Settings', message='Update Mail settings success!')
            except Exception as e:
                messagebox.showerror(title='Mail Settings Error', message='Save mail settings failed at:' + str(e))

        send_mail_checkbox = tk.Checkbutton(self.work_frame, text='发送邮件', variable=self.mail_send_var, onvalue=1, offvalue=0)
        send_mail_checkbox.place(x=10, y=10, width=75, height=30)
        self.mail_send_var.set(mail_data[1])

        mail_save = tk.Button(self.work_frame, text='Save', fg='green', font='Monaco 16 bold', command=lambda: self.run(on_mail_save_clicked))
        mail_save.place(x=735, y=10, width=60, height=30)

        subject_label = tk.Label(self.work_frame, text='主题', bg='gray88', fg='white', font='Monaco 16 bold')
        subject_label.place(x=10, y=50, width=60, height=30)

        subject_entry = tk.Entry(self.work_frame)
        subject_entry.place(x=71, y=50, width=728, height=30)
        subject_entry.delete(0, tk.END)
        subject_entry.insert(0, mail_data[2])

        sender_label = tk.Label(self.work_frame, text='发件人', bg='gray88', fg='white', font='Monaco 16 bold')
        sender_label.place(x=10, y=85, width=60, height=30)

        sender_entry = tk.Entry(self.work_frame)
        sender_entry.place(x=71, y=85, width=728, height=30)
        sender_entry.delete(0, tk.END)
        sender_entry.insert(0, mail_data[3])

        receivers_label = tk.Label(self.work_frame, text='收件人', bg='gray88', fg='white', font='Monaco 16 bold')
        receivers_label.place(x=10, y=120, width=60, height=30)

        receivers_entry = tk.Entry(self.work_frame)
        receivers_entry.place(x=71, y=120, width=728, height=30)
        receivers_entry.delete(0, tk.END)
        receivers_entry.insert(0, mail_data[4])

        mail_content = scrolledtext.ScrolledText(self.work_frame, bg='gray90', font='Monaco 16 bold')
        mail_content.place(x=10, y=155, width=780, height=642)
        mail_content.delete(0.0, tk.END)
        mail_content.insert(tk.END, mail_data[5])

    # 当当前遗留按钮点击时
    def on_remain_button_clicked(self):
        self.root.title('残留部分')
        self.drew_work_frame(width=800)
        remain_var = tk.StringVar()
        remain_var.set('点击右边button开始运行-->')

        def run_remain():
            remain_var.set('正在运行')
            text_tmp = scrolledtext.ScrolledText(self.work_frame, fg='green')
            text_tmp.place(x=2, y=40, width=796, height=735)
            for i in range(100):
                time.sleep(0.1)
                remain_var.set('Running :' + str(i))
                text_tmp.insert(tk.END, str(i) + '\n')
                self.root.update()

            text_tmp.place_forget()
            messagebox.showinfo(title='Info', message='更新成功')
            remain_var.set('report at C:/wwk/hq')

        remain_label = tk.Label(self.work_frame, textvariable=remain_var, bg='gray90')
        remain_label.place(x=2, y=0, width=700, height=30)

        remain_button = tk.Button(self.work_frame, text='运行', command=lambda: self.run(run_remain))
        remain_button.place(x=705, y=0, width=93, height=30)

    # 当寻找开发按钮点击时
    def on_spy_button_clicked(self):
        self.root.title('寻找开发')
        self.drew_work_frame(width=800, bg='gray')
        spy_var = tk.StringVar()
        spy_var.set('点击右边button更新结果-->')

        def update_search():
            time.sleep(100)
            messagebox.showinfo(title='Info', message='Success!')

        def on_search_button_clicked():
            search_result = scrolledtext.ScrolledText(self.work_frame, bg='gray96', fg='red', font='Monaco 16 bold')
            search_result.place(x=2, y=65, width=796, height=700)
            search_key = search_entry.get().strip()
            search_result.insert(tk.END, search_key)
            search_result.insert(tk.END, 'hfbejrhbejrhb')

        spy_label = tk.Label(self.work_frame, textvariable=spy_var, bg='gray90')
        spy_label.place(x=2, y=0, width=700, height=30)

        update_button = tk.Button(self.work_frame, text='更新', command=lambda: self.run(update_search))
        update_button.place(x=705, y=0, width=93, height=30)

        search_entry = tk.Entry(self.work_frame, fg='sea green', font='Monaco 16 bold')
        search_entry.place(x=2, y=32, width=700, height=30)

        search_button = tk.Button(self.work_frame, text='寻找', command=lambda: self.run(on_search_button_clicked))
        search_button.place(x=705, y=32, width=93, height=30)

    # 当发行伴侣按钮点击时
    def on_release_button_clicked(self):
        self.root.title('发行伴侣')
        self.drew_work_frame(width=800, bg='gold')

    # 当辅助对比按钮点击时
    def on_assist_button_clicked(self):
        self.root.title('辅助对比')
        self.drew_work_frame(width=800, bg='yellow')

    # 当帮助文档按钮点击时
    def on_help_button_clicked(self):
        self.root.title('帮助文档')
        self.drew_work_frame(width=800)
        help_text = scrolledtext.ScrolledText(self.work_frame)
        help_text.place(x=1, y=0, width=798, height=798)
        with open(os.path.join(BASE_DIR, 'help.txt'), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                help_text.insert(tk.END, line)

        # 当基础设置按钮点击时

    def on_settings_button_clicked(self):
        self.root.title('基础设置')
        self.drew_work_frame(width=800)

        conn = sqlite3.connect(SQLITE_DB)
        corsor = conn.cursor()
        basic_info = corsor.execute('select * from basic where id=1;')
        basic_data = basic_info.fetchone()
        conn.close()

        def on_finder_button_clicked():
            path_ = filedialog.askdirectory()
            finder_entry.delete(0, tk.END)
            finder_entry.insert(0, path_)

        def on_save_button_clicked():
            oss_server = oss_server_entry.get().strip()
            oss_server_user = oss_server_user_entry.get().strip()
            oss_server_pass = oss_server_pass_entry.get().strip()
            finder_dir = finder_entry.get().strip()

            try:
                sql = 'update basic set oss_server="%s",oss_server_user="%s",oss_server_pass="%s",report_dir="%s" where id=1;' % (oss_server, oss_server_user, oss_server_pass, finder_dir)
                conn = sqlite3.connect(SQLITE_DB)
                corsor = conn.cursor()
                corsor.execute(sql)
                conn.commit()
                conn.close()
                messagebox.showinfo(title='Basic Settings', message='Update Basic settings success!')
            except Exception as e:
                messagebox.showerror(title='Update Error', message='Update basic setting failed at:' + str(e))

        info_label = tk.Label(self.work_frame, text='以下设置一般默认即可, 只有OSS Server改变的时候才需要修改\n可以点击选择报告保存路径,来自定义报告生成后存放的文件夹', fg='red', font="Monaco 16 bold")
        info_label.place(x=10, y=10, width=780, height=290)

        oss_server_label = tk.Label(self.work_frame, text='OSS Server IP', bg='gray88', fg='red', font='Monaco 16 bold')
        oss_server_label.place(x=10, y=310, width=200, height=40)

        oss_server_entry = tk.Entry(self.work_frame, font='Monaco 16 bold')
        oss_server_entry.place(x=211, y=310, width=580, height=40)
        oss_server_entry.delete(0, tk.END)
        oss_server_entry.insert(0, basic_data[1])

        oss_server_user_label = tk.Label(self.work_frame, text='OSS Server User', bg='gray88', fg='red', font='Monaco 16 bold')
        oss_server_user_label.place(x=10, y=360, width=200, height=40)

        oss_server_user_entry = tk.Entry(self.work_frame, font='Monaco 16 bold')
        oss_server_user_entry.place(x=211, y=360, width=580, height=40)
        oss_server_user_entry.delete(0, tk.END)
        oss_server_user_entry.insert(0, basic_data[2])

        oss_server_pass_label = tk.Label(self.work_frame, text='OSS Server Password', bg='gray88', fg='red', font='Monaco 16 bold')
        oss_server_pass_label.place(x=10, y=410, width=200, height=40)

        oss_server_pass_entry = tk.Entry(self.work_frame, font='Monaco 16 bold', show='*')
        oss_server_pass_entry.place(x=211, y=410, width=580, height=40)
        oss_server_pass_entry.delete(0, tk.END)
        oss_server_pass_entry.insert(0, basic_data[3])

        finder_choice_button = tk.Button(self.work_frame, text='选择报告保存路径', fg='green', font='Monaco 16 bold', command=on_finder_button_clicked)
        finder_choice_button.place(x=10, y=480, width=200, height=40)

        finder_entry = tk.Entry(self.work_frame, font='Monaco 16 bold')
        finder_entry.place(x=211, y=480, width=580, height=40)
        finder_entry.delete(0, tk.END)
        finder_entry.insert(0, basic_data[4])

        basic_save_button = tk.Button(self.work_frame, text='Save', fg='green', font='Monaco 16 bold', command=on_save_button_clicked)
        basic_save_button.place(x=700, y=700, width=80, height=30)

    # 入口函数
    def write(self):
        self.drew_ui()
        self.root.mainloop()


pencil = Pencil()
pencil.write()

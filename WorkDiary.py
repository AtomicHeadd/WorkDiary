import sys
from copy import *

# 追加したい設定項目
# 計測時間を表示する/時間、分だけ
# 30分ごとに自動で録画を停止する機能
# 総時間と統計(時間、日、月)
#
# 問題
# 設定ファイルの文字列次第でデータファイルが壊れると思います(特に改行や,)
try:
    import Tkinter as tk
except:
    import tkinter as tk
import tkinter.ttk as ttk
import time
import os
import re


class recorder():
    def load(self):
        configfile_name = "WorkDiary.setting"
        if not os.path.isfile(configfile_name):
            # 存在しない場合
            setting_file = open(configfile_name, mode="x")
            self.button_name = ["ボタン1", "ボタン2", "ボタン3"]
            setting_file.write("button_name1=ボタン1\n")
            setting_file.write("button_name2=ボタン2\n")
            setting_file.write("button_name3=ボタン3\n")
            setting_file.close()
        else:
            setting_file = open(configfile_name, "r")
            self.button_name = ["ボタン1", "ボタン2", "ボタン3"]
            for s in setting_file:
                content = s.split("=")
                if "button_name" in content[0]:
                    num = int(re.findall(r"button_name(\d)", content[0])[0])
                    if num <= 0 or num >= 4:
                        continue
                    self.button_name[num-1] = content[1].strip()
            setting_file.close()


    def save_recording(self):
        if self.current_target_index == -1:
            return
        recordfile_name = "DiaryRecord.csv"
        now_str = time.strftime("%H:%M:%S")
        now = now_str.split(":")
        if not (int(self.start_time[0]) == int(now[0]) and int(self.start_time[1]) == int(now[1])):
            if not os.path.isfile(recordfile_name):
                self.record_file = open(recordfile_name, mode="x")
            else:
                self.record_file = open(recordfile_name, mode="a")
            start_time_str = str(self.start_time[0]) + ":" + str(self.start_time[1]) + ":" + self.start_time[2]
            passed_time_str = str(self.passed_time[0]) + ":"
            if int(self.passed_time[1]) < 9:
                passed_time_str += "0"
            passed_time_str += str(self.passed_time[1])
            self.record_file.write(time.strftime("%Y-%m-%d ") + start_time_str + ", " + self.button_name[self.current_target_index] + ", " + passed_time_str + "\n")
            self.record_file.close()
        self.button1.configure(text=self.button_name[0])
        self.button2.configure(text=self.button_name[1])
        self.button3.configure(text=self.button_name[2])
        self.current_target.configure(text="")

    def button1_clicked(self):
        self.save_recording()
        if not self.current_target_index == 0:
            self.save_recording()
            self.current_target_index = 0
            self.button1.configure(text=self.button_name[0] + "停止")
            self.start_time = time.strftime("%H:%M:%S").split(":")
            self.passed_time = [0, 0, 0]
            self.current_target.configure(text=self.button_name[0] + "計測中... ")
        else:
            self.current_target_index = -1

    def button2_clicked(self):
        self.save_recording()
        if not self.current_target_index == 1:
            self.save_recording()
            self.current_target_index = 1
            self.button2.configure(text=self.button_name[1] + "停止")
            self.start_time = time.strftime("%H:%M:%S").split(":")
            self.passed_time = [0, 0, 0]
            self.current_target.configure(text=self.button_name[1] + "計測中... ")
        else:
            self.current_target_index = -1

    def button3_clicked(self):
        self.save_recording()
        if not self.current_target_index == 2:
            self.current_target_index = 2
            self.button3.configure(text=self.button_name[2] + "停止")
            self.start_time = time.strftime("%H:%M:%S").split(":")
            self.passed_time = [0, 0, 0]
            self.current_target.configure(text=self.button_name[2] + "計測中... ")
        else:
            self.current_target_index = -1

    def update_clock(self):
        if self.current_target_index != -1:
            hour_minute = str(self.passed_time[0]) + "時間" + str(self.passed_time[1]) + "分"
            self.passed_time[2] += 1
            if self.passed_time[2] == 60:
                self.passed_time[1] += 1
                self.passed_time[2] = 0
                if self.passed_time[1] == 60:
                    self.passed_time[0] += 1
                    self.passed_time[1] = 0
            self.current_target.configure(text=self.button_name[self.current_target_index] + "計測中... " + hour_minute)
        else:
            self.current_target.configure(text="")
        self.root.after(1000, self.update_clock)

    def __init__(self):
        if hasattr(sys, 'setdefaultencoding'):
            import locale
            lang, enc = locale.getdefaultlocale()
            sys.setdefaultencoding('utf-8')
        self.root = tk.Tk()
        self.start_time = [0, 0, 0]
        self.passed_time = [0, 0, 0]
        # label.pack()
        # 設定ファイル類
        self.load()

        # ウィンドウ作成
        self.root.title("作業レコーダー")
        self.root.geometry("400x400")
        self.root.minsize(width=370, height=200)
        self.root.maxsize(width=370, height=200)

        # ボタン等
        setting = tk.Button(self.root, text="⚙")
        setting.grid(row=0, column=0)
        take_time = tk.Button(self.root, text="測定")
        take_time.grid(row=0, column=1)
        stats = tk.Button(self.root, text="統計")
        stats.grid(row=0, column=2)
        self.button1 = tk.Button(self.root, text=self.button_name[0], height=5, width=10, command=self.button1_clicked)
        self.button1.place(x=10, y=40)
        self.button2 = tk.Button(self.root, text=self.button_name[1], height=5, width=10, command=self.button2_clicked)
        self.button2.place(x=140, y=40)
        self.button3 = tk.Button(self.root, text=self.button_name[2], height=5, width=10, command=self.button3_clicked)
        self.button3.place(x=270, y=40)
        self.current_target_index = -1
        self.current_target = tk.Label(text="")
        self.current_target.place(x=0, y=130)

        self.update_clock()

        self.root.mainloop()

        # 設定ファイル閉じる
        self.save_recording()
        sys.exit()


app = recorder()

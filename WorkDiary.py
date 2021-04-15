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
            # 設定ファイルが存在しない場合
            with open(configfile_name, mode="x") as f:
                f.write("button_name1=ボタン1\nbutton_name2=ボタン2\nbutton_name3=ボタン3\n")
            return
        # 設定ファイルが存在する場合
        with open(configfile_name, "r") as setting_file:
            for s in setting_file:
                content = s.split("=")
                if "button_name" in content[0]:
                    num = int(re.findall(r"button_name(\d)", content[0])[0])
                    if num <= 0 or num >= 4:
                        continue
                    self.button_name[num-1] = content[1].strip()

    def save_recording(self):
        if self.current_target_index == -1:
            return
        record_file_name = "DiaryRecord.csv"
        now_str = time.strftime("%H:%M:%S")
        now = now_str.split(":")
        if not (int(self.start_time[0]) == int(now[0]) and int(self.start_time[1]) == int(now[1])):
            if not os.path.isfile(record_file_name):
                self.record_file = open(record_file_name, mode="x")
            else:
                self.record_file = open(record_file_name, mode="a")
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
        self.load_data()

    def record_button_clicked(self, index):
        buttons = [self.button1, self.button2, self.button3]
        self.save_recording()
        if not self.current_target_index == index:
            self.save_recording()
            self.current_target_index = index
            buttons[index].configure(text=self.button_name[index] + "停止")
            self.start_time = time.strftime("%H:%M:%S").split(":")
            self.passed_time = [0, 0, 0]
            self.current_target.configure(text=self.button_name[index] + "計測中... ")
        else:
            self.current_target_index = -1

    def stats_button_clicked(self, right):
        date_num = [int(s) for s in self.stats_showing_date.split("-")]
        today_num = [int(s) for s in time.strftime("%Y-%m-%d").split("-")]
        if (date_num == today_num and right) or (date_num == self.software_origin and not right):
            return
        if right:
            date_num[2] += 1
            if date_num[2] > 31:
                date_num[1] += 1
                date_num[2] = 1
                if date_num[1] > 12:
                    date_num[0] += 1
                    date_num[1] = 1
        else:
            date_num[2] -= 1
            if date_num[2] < 1:
                date_num[2] = 31
                date_num[1] -= 1
                if date_num[1] < 1:
                    date_num[1] = 12
                    date_num[0] -= 1
        self.stats_showing_date = f"{date_num[0]}-{date_num[1]}-{date_num[2]}"
        self.load_data(date_num)

    # 統計移動ボタンの実装には統計画面が今表示している日付が必要

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

    def load_data(self, target=[int(s) for s in time.strftime("%Y-%m-%d").split("-")]):
        a = dict()
        with open("DiaryRecord.csv", "r") as f:
            for line in f:
                line_info = re.match(r"(\d\d\d\d-\d+-\d+).+,\s(.+),\s(\d+):(\d+)", line)
                if line_info is None:
                    continue
                date_num = [int(s) for s in line_info.group(1).split("-")]
                if date_num == target:
                    # 既に登録されている場合
                    task_name = line_info.group(2)
                    if task_name in a:
                        a[task_name] = [int(x)+int(y) for (x, y) in zip(a[task_name], [line_info.group(3), line_info.group(4)])]
                    # 無い場合
                    else:
                        a[task_name] = [int(line_info.group(3)), int(line_info.group(4))]
        today_num = [int(s) for s in time.strftime("%Y-%m-%d").split("-")]
        if target == today_num:
            stats_content = "本日\n"
        elif target == self.software_origin:
            stats_content = "このソフトウェアの誕生日です\n"
        else:
            stats_content = f"{target[0]}/{target[1]}/{target[2]}\n"
        if len(a) == 0:
            stats_content += "活動なし"
            self.stats_text.configure(text=stats_content)
            return
        for key, value in a.items():
            up = int(value[1] / 60)
            rest = value[1] % 60
            if value[0] + up < 1:
                stats_content += key + ": " + str(value[1]) + "分\n"
            else:
                stats_content += key + ": " + str(up) + "時間" + str(rest) + "分\n"
        self.stats_text.configure(text=stats_content)

    def __init__(self):
        if hasattr(sys, 'setdefaultencoding'):
            import locale
            lang, enc = locale.getdefaultlocale()
            sys.setdefaultencoding('utf-8')
        self.root = tk.Tk()
        self.start_time = [0, 0, 0]
        self.passed_time = [0, 0, 0]
        self.stats_showing_date = time.strftime("%Y-%m-%d")
        self.software_origin = [2021, 4, 3]
        # label.pack()
        # 設定ファイル類
        self.button_name = ["ボタン1", "ボタン2", "ボタン3"]
        self.load()

        # ウィンドウ作成
        self.root.title("作業レコーダー")
        self.root.geometry("400x400")
        self.root.minsize(width=370, height=250)
        self.root.maxsize(width=370, height=250)

        # ボタン等
        tab_setting = tk.Button(self.root, text="⚙")
        tab_setting.grid(row=0, column=0)
        tab_watch = tk.Button(self.root, text="測定")
        tab_watch.grid(row=0, column=1)
        tab_stats = tk.Button(self.root, text="統計")
        tab_stats.grid(row=0, column=2)
        self.button1 = tk.Button(self.root, text=self.button_name[0], height=5, width=10,
                                 command= lambda: self.record_button_clicked(0))
        self.button1.place(x=10, y=40)
        self.button2 = tk.Button(self.root, text=self.button_name[1], height=5, width=10,
                                 command= lambda: self.record_button_clicked(1))
        self.button2.place(x=140, y=40)
        self.button3 = tk.Button(self.root, text=self.button_name[2], height=5, width=10,
                                 command= lambda: self.record_button_clicked(2))
        self.button3.place(x=270, y=40)
        self.current_target_index = -1
        self.current_target = tk.Label(text="")
        self.current_target.place(x=0, y=130)
        #統計ボタン
        self.stats_left = tk.Button(self.root, text="←", height=1, width=1,
                                    command=lambda : self.stats_button_clicked(False))
        self.stats_left.place(x=10, y=180)
        self.stats_right = tk.Button(self.root, text="→", height=1, width=1,
                                     command=lambda : self.stats_button_clicked(True))
        self.stats_right.place(x=340, y=180)
        self.stats_text = tk.Label(text="本日")
        self.stats_text.place(x=140, y=150)

        self.load_data()
        self.update_clock()

        self.root.mainloop()

        # 設定ファイル閉じる
        self.save_recording()
        sys.exit()


app = recorder()

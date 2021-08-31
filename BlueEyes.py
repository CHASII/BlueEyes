'''
@Autor: Chason
@Date: 2018-05-15 15:53:34
LastEditors: Chas
LastEditTime: 2021-08-31 15:18:08
@Version: 2.0
@Description: 定时锁屏，保护眼睛。
'''

import tkinter
import shutil
import sys
import time
import os
import configparser
import tkinter.messagebox


class Eyes(object):
    
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        # 使用__file__会导致pyinstaller打出的exe文件，绝对路径会变成c:/widnows/system32，使用sys.argv[0]解决
        conf_content ="[System]\nwork_time = 9-22\n[Time_config]\nremind_time = 8\nscreensaver_time = 30\nlockworkstation = 1\nlocktaskmgr = 1"
        os.chdir(self.root_dir)
        if not os.path.exists("Blue-Eyes.ini"):
            with open("Blue-Eyes.ini", "w") as f:f.write(conf_content)
        config_file = os.path.join(self.root_dir, "Blue-Eyes.ini")
        config = configparser.ConfigParser()
        config.read(config_file)
        now_time = int(time.strftime("%H", time.localtime()))
        work_time = config.get("System", "work_time")
        start = int(work_time.split("-")[0])
        end = int(work_time.split("-")[1])
        if not start <= now_time <= end:sys.exit(-1)
        self.remind_time = int(config.get("Time_config", "remind_time"))
        self.screensaver_time = int(config.get("Time_config", "screensaver_time"))
        self.lockworkstation = int(config.get("Time_config", "lockworkstation"))
        self.locktaskmgr = int(config.get("Time_config", "locktaskmgr"))
        self.root = tkinter.Tk()
        self.root.title("屏保小助手_v1.2")
        self.root.geometry("300x80+10+10")
        self.Label1 = tkinter.Label(self.root, font="微软雅黑 -14", text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        self.Label2 = tkinter.Label(self.root, font="微软雅黑 -14", text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        self.Button1 = tkinter.Button(self.root, text="我知道了", command=self.root.quit, activeforeground="white", activebackground="red")

    def remindWindows(self, num):
        for j in range(num, 0, -1):
            self.Label1["text"] = f"\n 温馨提示：桌面将在{j}秒后进入屏保模式！"
            self.Label1.pack()
            self.root.update()
            time.sleep(1)

    def screensaverWindows(self, num):
        self.root.wm_attributes("-topmost", True)# 强制置顶
        self.Label2["text"] = '\n 珍爱生命，远离蓝光！\n'
        self.Label2.pack()
        i = 1# 设置指针，多少秒后锁屏
        for j in range(num, 0, -1):
            self.Label1["text"] = j
            self.root.update()
            i = i + 1
            time.sleep(1)
            if i == 10 and self.lockworkstation == 1:os.system("rundll32.exe user32.dll,LockWorkStation")# 锁屏
            # if i == 15:os.system("shutdown.exe /h");self.logEvent("关闭显示器")# 黑色屏幕保护程序
            if i == 15:os.system(r"%systemroot%\system32\scrnsave.scr /s");self.logEvent("关闭显示器")# 黑色屏幕保护程序
        # os.system('shutdown.exe -c "exit"')
        os.system(r"{0}\sbin\nircmd.exe monitor async_on".format(self.root_dir))
        self.logEvent("唤醒显示器")
        self.root.destroy()

    def logEvent(self, str):
        data_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("Blue-Eyes.log", encoding="utf-8",mode="a") as f:
            f.write(data_time + "   " + str + "\n")

    def main(self):
        def closeWindow():
            tkinter.messagebox.showerror(title="警告", message="不许关闭，好好休息！")
            return
        self.root.protocol("WM_DELETE_WINDOW", closeWindow)
        self.remindWindows(self.remind_time)# 执行提醒
        self.root.minsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())# 定时窗口
        self.root.state("zoomed")# 窗口最大化
        self.root.attributes("-fullscreen", True) # 全屏
        self.root.config(bg="black")
        topTitle = self.root.winfo_toplevel()
        topTitle.overrideredirect(True)
        self.screensaverWindows(self.screensaver_time)
        self.root.mainloop()

Eyes().main()

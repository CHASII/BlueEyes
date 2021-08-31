'''
@Autor: Chason
@Date: 2018-05-15 15:53:34
LastEditors: Please set LastEditors
LastEditTime: 2020-10-07 17:05:09
@Version: 2.0
@Description: 定时锁屏，保护眼睛
说明：
pyinstaller -c -a -w --clean -F Blue-Eyes.py
参数说明
-a, --ascii
Do not include unicode encoding support (default: included if available)
--clean
Clean PyInstaller cache and remove temporary files before building.
-w, --windowed, --noconsole # 出现问题使需要把这个去掉，排查问题
Windows and Mac OS X: do not provide a console window for standard i/o.
On Mac OS X this also triggers building an OS X .app bundle. This option is ignored in *NIX systems.
PermissionError: [Errno 13] Permission denied: ... ucrtbase.dll 问题，则import shutil
https://winaero.com/create-shutdown-restart-hibernate-and-sleep-shortcuts-in-windows-10/
'''

import tkinter
import shutil
import sys
import time
import os
import configparser
import tkinter.messagebox


class Eyes():
    root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    # 使用__file__会导致pyinstaller打出的exe文件，绝对路径会变成c:/widnows/system32，使用sys.argv[0]解决
    conf_content ="[System]\nwork_time = 9-22\n[Time_config]\nnotice_time = 8\nprotect_time = 30\nlockworkstation = 1\nlocktaskmgr = 1"
    os.chdir(root_dir)
    if not os.path.exists("Blue-Eyes.ini"):
        with open("Blue-Eyes.ini", "w") as f:
            f.write(conf_content)
    config_file = os.path.join(root_dir, "Blue-Eyes.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    # 当前时间
    now_time = int(time.strftime("%H", time.localtime()))
    # 工作时间
    work_time = config.get("System", "work_time")
    # 判断时间
    start = int(work_time.split("-")[0])
    end = int(work_time.split("-")[1])
    if not start <= now_time <= end:
        # 不能直接用exit，否则会报错
        sys.exit(-1)
    # 提醒时间
    notice_time = int(config.get("Time_config", "notice_time"))
    # 保护眼睛时间
    protect_time = int(config.get("Time_config", "protect_time"))
    # 是否锁屏
    lockworkstation = int(config.get("Time_config", "lockworkstation"))
    # 是否禁止调用任务栏
    locktaskmgr = int(config.get("Time_config", "locktaskmgr"))
    root = tkinter.Tk()
    root.title("护眼小程序 - By Chas")
    # root.iconbitmap(os.path.join(root_dir, "conf", "eye.ico"))
    root.geometry("300x80+300+200")
    # 定义字体
    # Label1 = tkinter.Label(root, font="微软雅黑 -14 ", text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    Label1 = Label2 = tkinter.Label(root, text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    # Label2 = tkinter.Label(root, font="微软雅黑 -14 ", text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    Button1 = tkinter.Button(root, text="我知道了", command=root.quit, activeforeground="white", activebackground="red")

    def beBig(self):
        # 防止关闭窗口
        def closeWindow():
            tkinter.messagebox.showerror(title="警告", message="不许关闭，好好休息！")
            return
        self.root.protocol("WM_DELETE_WINDOW", closeWindow)
        # 执行提醒
        self.notice(self.notice_time)
        # 定时窗口
        self.root.minsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        # 窗口最大化
        self.root.state("zoomed")
        # 全屏
        self.root.attributes("-fullscreen", True)
        self.root.config(bg="black")
        topTitle = self.root.winfo_toplevel()
        topTitle.overrideredirect(True)
        self.protect(self.protect_time)
        self.root.mainloop()

    # 提醒窗口
    def notice(self, num):
        if self.locktaskmgr == 1:
            # 禁止调用任务管理器
            # command = r"""reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v "DisableTaskMgr" /t REG_DWORD /F /d 1"""
            # os.system(command)
            self.write_log("禁止调用任务栏")
        for j in range(num, 0, -1):
            self.Label1["text"] = "\n 温馨提示：桌面将在%s秒后进入护眼模式！" % j
            self.Label1.pack()
            self.root.update()
            time.sleep(1)

    # 护眼窗口
    def protect(self, num):
        # 强制置顶
        self.root.wm_attributes("-topmost", True)
        self.Label2["text"] = '\n 珍爱生命，远离蓝光！\n'
        self.Label2.pack()
        # 设置指针，多少秒后锁屏
        i = 1
        for j in range(num, 0, -1):
            self.Label1["text"] = j
            self.root.update()
            i = i + 1
            time.sleep(1)
            if i == 10 and self.lockworkstation == 1:
                # 锁屏
                os.system("rundll32.exe user32.dll,LockWorkStation")
            if i == 15:
                # 黑色屏幕保护程序
                os.system("scrnsave.scr /s")
                # 是电脑进入休眠
                # os.system("rundll32.exe powrprof.dll,SetSuspendState Hibemate")
                # 调用程序设置息屏
                # os.system(r"{0}\sbin\nircmd.exe monitor async_off".format(self.root_dir))
                self.write_log("关闭显示器")
        # 还原调用任务管理器
        # command = r"""reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v "DisableTaskMgr" /t REG_DWORD /F /d 0"""
        # os.system(command)
        # self.write_log("还原调用任务栏")
        os.system(r"{0}\sbin\nircmd.exe monitor async_on".format(self.root_dir))
        self.write_log("唤醒显示器")
        self.root.destroy()

    # 写入日志
    def write_log(self, str):
        data_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("Blue-Eyes.log", "a") as f:
            f.write(data_time + "       " + str + "\n")


beBig = Eyes()
beBig.beBig()

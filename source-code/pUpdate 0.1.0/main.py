import os
import shutil
import subprocess
import threading
import time
import tkinter
import zipfile
from tkinter import *
from tkinter import messagebox

import requests
from Vsvpack import absoluteScriptFolderPath
from Vsvpack import vsvpack

import lodingbar




def getbool(string):
    if string == "True" or string == "true":
        return True
    elif string == "False" or string == "false":
        return False
    else:
        return None

def pass_event():
    messagebox.showinfo("Info"," you can't close this during \n"
                               " the update. Please Klick On the '✓' \n "
                               "to finish the Update after it's done.")
tk=Tk()
path_this=absoluteScriptFolderPath().get(__file__)
Theme=vsvpack(path_this+"\images","theme")
tk.title(Theme.read("Title"))
tk.resizable(False,False)
status=0
tk.overrideredirect(not getbool(Theme.read("showBar")))
print(getbool(Theme.read("showBar")))
tk.protocol("WM_DELETE_WINDOW", pass_event)

tk.geometry("+%d+%d" % (int(Theme.read("windowX")), int(Theme.read("windowY"))))#x,y
tk.configure(bg='#5EEFFF')
imageList={}
tk.iconbitmap(path_this+r"\images\icon.ico")
t=PhotoImage(file=r"images\b.png",master=tk)
l=Label(master=tk,image=t,borderwidth=0)
l.grid(row=0,column=0)
t_done= PhotoImage(file=path_this+r"\images\b_done.png", master=tk)
loading_done= PhotoImage(file=path_this+r"\images\load\end.png", master=tk)

x=None

for i in range(1,12):
    imageList[i] = PhotoImage(file=path_this+r"\images\load\\"+str(i)+".png", master=tk)

fortschrit=Label(master=tk,text="",borderwidth=0,bg='#5EEFFF')
fortschrit.grid(row=1,column=0)
index=1
Loding= lodingbar.LodingBar()

u=None

def exit_(self):
    global x,Loding,tk
    if(Loding.getLoad()>=100):
        tk.destroy()
        exit()
class label_l:
    def __init__(self):

        self.label=Label(tk,image=imageList[1],borderwidth=0)
        self.label.grid(row=0,column=0)
        self.label.bind("<Button-1>",exit_)


label = label_l()


def thread_function(t="f"):

    global tk,imageList,index,label,fortschrit,Loding,l,t_done,loading_done
    label.label.configure(image=imageList[index])
    fortschrit.configure(text=Loding.add(status-Loding.getLoad()))
    time.sleep(0.1)
    if index!=11:
        index+=1
    else:
        index=1
    if(Loding.getLoad()<100):
        thread_function()
    else:
        tk.configure(bg="#00FF6A")
        l.configure(image=t_done)
        label.label.configure(image=loading_done)
        fortschrit.configure(bg="#00FF6A")
        label.label.configure(borderwidth=5)



def exeute_exe(exe):

    pass

class updater:
    def __init__(self):

        self.a=path_this
        self.pack=vsvpack(path_this+r"\job","inst")
        p=self.pack
        self.doneTask=0
        self.task_list = []
        self.task_count=int(p.read("task_count"))
        for c in range(1,self.task_count+1):
            self.task_list+=[p.read("task_"+str(c)).split("|")]
    def doTasks(self):
        global status
        print("doing")
        for index in range(0,self.task_count):
            task = self.task_list[index]


            try:
                status= self.doneTask/self.task_count

                print(f"{task[0]=}")
                match task[0]:
                    case ".move":
                        file=task[1]
                        moveto=task[2]
                        print("move file:"+file+" to "+moveto)
                        shutil.move(file.replace("<Path>",self.a),moveto.replace("<Path>",self.a))
                        self.doneTask+=1
                        del file
                        continue
                    case ".delete":

                        delete_content = task[1].replace("<Path>",self.a)
                        print("deleted :"+delete_content)
                        os.remove(delete_content)
                        self.doneTask += 1
                        continue
                    case ".unzip":
                        with zipfile.ZipFile(task[1].replace("<Path>",self.a), 'r') as zip_file:

                            zip_file.extractall(task[2].replace("<Path>",self.a))
                        print("unziped")
                        continue

                    case ".dowl":
                        req=requests.get(task[1])
                        open(task[2].replace("<Path>",self.a), "wb").write(req.content)
                        continue
                    case _:

                        raise ValueError("'"+task[0]+"' is an invalid oporation")
            except shutil.Error as e:

                t=file.replace("<Path>", self.a).split("\\")
                os.remove(moveto.replace("<Path>", self.a)+t[-1])
                shutil.move(file.replace("<Path>", self.a), moveto.replace("<Path>", self.a))

                #print(e)


            except Exception as e:


                if (messagebox.showerror("Installation Error","The Instalation-Script is corupted \n please ask the Publischer for help \n or try to redonload the Program.")):
                    messagebox.showerror("ERROR-Code", "Exeption: " + str(e))
                    print(e)
                tk.destroy()
                exit()

                pass
        status=100




def main():
    global u
    u = updater()
    x = threading.Thread(target=thread_function, args=(label,))
    update_maker = threading.Thread(target=u.doTasks(), args=(label,))

    x.start()
    update_maker.start()

    # x.join()

    tk.mainloop()


if __name__ == "__main__":
    main()
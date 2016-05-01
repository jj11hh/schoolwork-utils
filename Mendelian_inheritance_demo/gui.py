#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from Tkinter import *
import tkMessageBox
import genes,demo
import time
import threading

records=[]
str_output=""
pure=""

class Surrounding():
    demo_started=False
    str_output=""
    
sur=Surrounding()
    
def gen_records():
    try:
        input_genes=e_genes.get()
        pure=input_genes.upper()
        times=int(e_times.get())
        if not input_genes:raise ValueError
        if not times: raise ValueError
        records[:]=[]
        for i in range(times):
            records.append(genes.make_record(input_genes))
    except ValueError:
        tkMessageBox.showerror("错误","输入格式有误")
    else:
        sur.str_output=genes.sprint_records(records)
        text_show.delete("1.0",END)
        text_show.insert(END,sur.str_output)
    gen_text="重新实验"
        
def save_as_text():
    if not sur.str_output:
        tkMessageBox.showerror("错误","请先生成记录")
        return
    
    f=open("output.txt","w")
    f.write(sur.str_output)
    f.close()
def save_as_html():
    if not records:
        tkMessageBox.showerror("错误","请先生成记录")
    f=open("output.html","w")
    f.write(genes.sprint_records_as_html(records))
    f.close()
        
def start_demo():
    if not records:
        tkMessageBox.showerror("错误","请先生成记录")
        return
    
    d=demo.Demo(records)
    d.run()

win=Tk()
win.minsize(800,50)
win.title("基因分离演示程序|Wrote by Mr.Y")
root=Frame(win)
root.pack(fill=X,expand=2,side=TOP)

input_frame=Frame(root)
input_frame.pack(side=LEFT,fill=X,expand=2)
lbl_frame=Frame(input_frame)
e_frame=Frame(input_frame)
lbl_frame.pack(side=LEFT)
e_frame.pack(side=RIGHT,fill=X,expand=2)
btn_frame=Frame(root)
btn_frame.pack(side=RIGHT)
text_frame=Frame(win)
text_frame.pack(side=BOTTOM,fill=BOTH,expand=5)

lbl_times=Label(lbl_frame,text="实验次数:")
lbl_genes=Label(lbl_frame,text="基因(示例:AB):")
lbl_times.pack()
lbl_genes.pack()
text_show=Text(text_frame)
text_show.pack(side=LEFT,fill=BOTH,expand=5)

scr_show=Scrollbar(text_frame)
scr_show.pack(side=RIGHT,fill=Y,expand=2)
scr_show["command"]=text_show.yview
text_show["yscrollcommand"]=scr_show.set

e_times=Entry(e_frame)
e_genes=Entry(e_frame)
e_times.pack(fill=X,expand=2)
e_genes.pack(fill=X,expand=2)

gen_text=StringVar()
gen_text.set("生成记录")
btn_gen=Button(btn_frame,textvariable=gen_text,command=gen_records)
btn_output_text=Button(btn_frame,text="导出为纯文本",command=save_as_text)
btn_output_html=Button(btn_frame,text="导出为HTML表格",command=save_as_html)
btn_show=Button(btn_frame,text="演示",command=start_demo)

btn_gen.pack(side=LEFT,fill=Y,expand=1)
btn_output_text.pack(side=LEFT,fill=Y,expand=1)
btn_output_html.pack(side=LEFT,fill=Y,expand=1)
btn_show.pack(side=LEFT,fill=Y,expand=1)

root.mainloop()

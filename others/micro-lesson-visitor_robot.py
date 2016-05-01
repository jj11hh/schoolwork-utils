#!/usr/bin/python2
###################################
#                                 #
#  A robot to visit xk.zjer.cn    #
#                                 #
###################################
#2015 Mr.Jiang Copyleft.

import urllib2
import threading

HEADERS=[\
('Host','wk.zjer.cn'),\
('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'),\
('Accept','*/*'),\
('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),\
('Accept-Encoding','gzip, deflate'),\
('X-Requested-With','XMLHttpRequest'),\
('Referer','http://wk.zjer.cn/wkxx/index.htm?id=5753&type=1&newsid=4319'),\
('Cookie','pgv_pvi=7601722368; CNZZDATA1253226936=219464253-1431834207-%7C1432416476; clientlanguage=zh_CN; JSESSIONID=37A16C6155CF87BDD34EBB6E467F2B97.tomcat01; jiathis_rdc=%7B%22http%3A//wk.zjer.cn/wkxx/index.htm%3Fid%3D5753%26type%3D1%26newsid%3D4319%22%3A%221%7C1432421803833%22%7D; pgv_si=s4346678272')
]

LESSON_IDs=[5749,5750,5751,5752,5753,5754] #id of lessons.

URLS=[('http://wk.zjer.cn/weike_video_play.jspx?id=%d' % x) for x in LESSON_IDs]
URLS.append('http://wk.zjer.cn/weike_view.jspx?id=4319')
THREAD_NUM=5
TIMES=1000

class clicker(threading.Thread):
    def __init__(self,headers,urls,times,name="clicker"):
        threading.Thread.__init__(self)
        self.headers=headers
        self.urls=urls
        self.times=times
        self.count=0
        self.thread_stop = False
    def run(self):
        opener = urllib2.build_opener()
        opener.addheaders = self.headers
        for i in range(self.times):
            while self.thread_stop==False:
                self.count+=1
                for url in self.urls:
                    result=opener.open(url)
#               print "%s\t%d times" % self.name,i
#               for header in result.headers.headers:
#                   print "\t",header
    def stop(self): 
        self.thread_stop = True

# __________ Entry point __________

def main():
    THREAD_NUM=int(raw_input('How many thread are you want to run? : '))
    threads=[]
    for i in range(THREAD_NUM):
        threads.append(clicker(headers=HEADERS,urls=URLS,times=TIMES,name=("thread_%d" % i)))
    for i in range(THREAD_NUM):
        threads[i].start()


    print "Input 'stop [thread num]' to stop threads,\n"
    print "'statu [thread num]' to get thread's statu,\n"
    print "and 'exit' to exit.(Example: stop 4)"

#Resolv commands:

    while True:
        __input=raw_input("Command>:")
        try:
            if __input=="exit":
                for i in range(THREAD_NUM):
                    threads[i].stop()

                print "Exiting..."
                break
            elif __input[0:5]=="stop ":
                print 'Stoping thread No.%d' % (int(__input[5:].strip())-1)
                try:
                    threads[int(__input[5:].strip())-1].stop()
                except IndexError:
                    print "No such thread."
                else: print 'OK'
            elif __input[0:6]=="statu ":
                try:
                    print 'Clicked: %d' % threads[int(__input[6:].strip())-1].count
                except IndexError:
                    print "No such thread."
            else:
                print 'Invalid command.'
        except ValueError:
            print 'Invalid command.'
        except :
            print 'Unknown Error'
    exit()
    return 0

if __name__=='__main__':
    main()

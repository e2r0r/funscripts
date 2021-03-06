#!/bin/env python

#Author:gfn (breeze.guangfeng@gmail.com)

#-*- encoding:utf-8-*-

import htmllib
import urllib2
import formatter,StringIO

class TrackParser(htmllib.HTMLParser):

    def __init__(self, writer, *args):
        htmllib.HTMLParser.__init__(self,*args)
        self.writer = writer
    
    def parse_starttag(self,i):
        index = htmllib.HTMLParser.parse_starttag(self,i)
        self.writer.index = index
        return index

    def parse_endtag(self,i):
        self.writer.index = i
        return htmllib.HTMLParser.parse_endtag(self,i)


class Para:

    def __init__(self):
        self.text = ''
        self.bytes = 0
        self.density = 0.0

class LineWirter(formatter.AbstractWriter):
    """
    a Formatter instance to get text in lines
    """

    def __init__(self):
        self.last_index = 0
        self.lines = [Para()]
        formatter.AbstractWriter.__init__(self)

    def send_flowing_data(self, data):
        t = len(data)
        self.index += t
        b = self.index - self.last_index
        self.last_index = self.index
        l = self.lines[-1]
        l.text += data
        l.bytes += b

    def send_paragraph(self,blankline):
        if self.lines[-1].text == '':
            return
        self.lines[-1].text += 'n'*(blankline+1)
        self.lines[-1].bytes += 2*(blankline+1)
        self.lines.append(Para()) #bug
        #print 'n'*(blankline+1)
        #midu.append([self.lines[-2].bytes ,len(self.lines[-2].text)])
        
    def send_literal_data(self,data):
        self.send_flowing_data(data)
    
    def send_line_break(self):
        self.send_paragraph(0)

    def compute_density(self):
        total = 0.0
        for l in self.lines:
            l.density = len(l.text) / float(l.bytes)
            total += l.density
        self.average = total / float(len(self.lines))
    
    def output(self):
        self.compute_density()
        output = StringIO.StringIO()
        lt = []
        for l in self.lines:
#            if l.density > 0.5:
#                output.write(l.text)
            lt.append(l.density)
        #return output.getvalue()
        return lt


def extract_text(html):
    """
    
    Arguments:
    - `html`:
    """
    writer = LineWirter()
    fmt = formatter.AbstractFormatter(writer)
    parser = TrackParser(writer,fmt)
    parser.feed(html)
    parser.close()
    writer.output()
    return writer.lines
#    return [[l.bytes,len(l.text)] for l in writer.lines]

        

htmls = urllib2.urlopen("http://news.sina.com.cn/c/2009-11-27/165619142166.shtml")
d =extract_text(htmls.read())
f = open("train_sina.txt","w+")
out = map(lambda x,y,z:[x,y,z],[Para()]+d[0:-1],d,d[1:]+[Para()])
f.write("%s %s %s\n"%(len(d),3,1))
line = 3*"%s "+"\n"
for x,y,z in out:
    f.write(line%(y.density,y.bytes,len(y.text)))
    #print x.density+z.density-2*y.density
    if (y.density > 0.5):
        f.write("1\n")
	print x.density+z.density-2*y.density
    else:
        f.write("0\n")

    

    

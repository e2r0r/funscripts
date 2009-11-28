#!/usr/bin env python
#-*- encoding:utf-8 -*-

"""
this program is used to extract text content from web pages.
It's algorithm is text-density and FDR(False Discovery Rate).
Author:gfn (breeze.guangfeng@gmail.com)
"""

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
        self.lines.append(Para())
        
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
        for l in self.lines:
            if l.density > 0.5:
                output.write(l.text)
        return output.getvalue()

    def output_fdr(self):
        self.compute_density()
        pvalue = map(lambda x:1.0/x.density ,self.lines)
        pvalue.sort(reverse=True)
        i = len(self.lines)
        m = [j for j in range(i) if pvalue[j] <= (j*5)/i][0]
        density = 1.0/pvalue[m]
        output = StringIO.StringIO()
        output.writelines(''.join([l.text for l in self.lines if l.density > density]))
        return output.getvalue()
        

def extract_text(html):

    writer = LineWirter()
    fmt = formatter.AbstractFormatter(writer)
    parser = TrackParser(writer,fmt)
    parser.feed(html)
    parser.close()

    return writer.output()

        

htmls = urllib2.urlopen("http://mil.news.sina.com.cn/s/2009-11-28/1139575478.html")
s = open('e.html','w+').write(extract_text(htmls.read()))

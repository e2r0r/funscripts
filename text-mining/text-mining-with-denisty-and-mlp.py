#!/bin/env python
#Author:gfn (breeze.guangfeng@gmail.com)
#-*- encoding:utf-8-*-

import htmllib
import urllib2
import formatter,StringIO
from pyfann import fann,libfann

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
        output.writelines(''.join(self.get_density_with_ann()))
        return output.getvalue()
    
    def get_density_with_ann(self):
        obj = libfann.fann_create_standard_array(2, (3, 1))
        ann = fann.fann_class(obj)
        patterns = fann.read_train_from_file('train_data.txt')
        ann.train_on_data(patterns, 1000, 1, 0.0)
        return [line[3] for line in map(lambda x:[x.density,x.bytes,len(x.text),x.text] , self.lines) if ann.run(line[0:2])[0] > 0]    

def text_mining(html):
    """
    
    Arguments:
    - `html`:web page html source code
    """
    writer = LineWirter()
    fmt = formatter.AbstractFormatter(writer)
    parser = TrackParser(writer,fmt)
    parser.feed(html)
    parser.close()
    return writer.output()
        

html = urllib2.urlopen("http://ent.hunantv.com/t/20091125/501015.html")
text = text_mining(html.read())

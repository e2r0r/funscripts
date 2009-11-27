#!-*- encoding:utf-8-*-
import htmllib
import urllib2
import formatter

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

    def send_para(self,blankline):
        if self.lines[-1].text == '':
            return
        self.lines[-1].text += 'n' * (blankline+1)
        self.lines[-1].bytes += 2*(blankline+1)
        self.lines.append(writer.para()) #bug
    
    def send_literal_data(self,data):
        self.send_flowing_data(data)
    
    def send_line_break(self):
        self.send_para(0)

# class AbstractWriter(formatter.AbstractWriter):
#     """
#     """

#     def __init__(self, *args):
#         """
#         """
#         formatter.AbstractWriter.__init__(self)    
 

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
    
    return writer.output()

        

htmls = urllib2.urlopen("http://ent.hunantv.com/t/20091125/501015.html")
extract_text(htmls.read())        
        
        

      
        
        
        


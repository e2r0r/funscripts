import web
from mmseg import seg_txt

urls = ('/','index')

class index:
        def GET(self):
            return "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/></head>INPUT:<form action=\"/\" method=post><textarea name=\"word\" cols=\"100\" rows=\"8\" style=\"background-color:#006E80;color:#FFFFFF\"></textarea><br/><input type=\"submit\" value=\"SUBMIT\"></form></html>"
        def POST(self):
            w = web.input()
            return "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/></head>OUTPUT:<br>"+"<textarea name=\"word\" cols=\"100\" rows=\"15\" style=\"background-color:#006E80;color:#FFFFFF\">"+'\n'.join([i for i in seg_txt(str(w.word.encode("utf8")))])+'</textarea><br/>YOUR INPUT:<br/><textarea name=\"word\" cols=\"100\" rows=\"8\" style=\"background-color:#006E80;color:#FFFFFF\">'+w.word.encode('utf8')+'</textarea></html>'
     
            
        
web.config.debug = True
app = web.application(urls,globals())

if __name__ == "__main__":    app.run()
        
    
    
    
        
        


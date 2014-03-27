#!/usr/bin/python
import httplib2
import os

print ("Content-Type: html/text")     # HTML is following
print ("")                            # blank line, end of headers

class AjaxCall(webapp.RequestHandler):
    def get(self):
        template_data = {}
        template_path = 'ajaxTest.html'
        self.response.out.write(template.render(template_path,template_data))

class ProcessAjax(webapp.RequestHandler):
    def get(self):
        inputdata = self.request.get("inputData")
        self.response.out.write(inputdata)


application = webapp.WSGIApplication(
                                     [('/processAjax',ProcessAjax),
                      ('/ajaxPage',AjaxCall)
                                    ],
                                     debug=True)

def main():
    run_wsgi_app(application)
print "hi0"
if __name__ == "__main__":
    print "hi"
    main()
    
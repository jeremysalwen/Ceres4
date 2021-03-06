

import os, os.path, string, tempfile, traceback,gtk,gtk.glade,sys


#sys.path.insert(0,"/usr/lib/pygtk1/lib/python"+sys.version[:3]+"/site-packages/gtk-1.2")
#sys.path.insert(0,os.path.abspath(os.path.dirname(sys.argv[0]))+"/../lib/python"+sys.version[:3]+"/site-packages/gtk-1.2")
#sys.path.insert(0, PYGTK1PLACEMENT  +"/../lib/python"+sys.version[:3]+"/site-packages/gtk-1.2")


def lrstrip(dasstring):
    dasstring=string.lstrip(dasstring)
    dasstring=string.rstrip(dasstring)
    return dasstring

class Config:
    def __init__(self,xmltree,conffilename):
        self.xmltree=xmltree
        self.vars={}
        self.conffilename=conffilename
        self.readConfFile(conffilename)
        self.fileselectors={}
        
    def setTempFileName(self,tempfilename):
        self.tempfilename=tempfilename

    def readConfFile(self,filename):
        try:
            file=open(filename,"r")
        except:
            return
        while 1:
            line=""
            while line=="" or line=="\n" or line[0:1]=="#":
                line=file.readline()
                if line=="":
                    file.close()
                    return
                line=lrstrip(line)
            
            splitline=string.split(line,"=",1)
            splitline[0]=lrstrip(splitline[0])
            splitline[1]=lrstrip(splitline[1])

            if isinstance(self.xmltree.get_widget(splitline[0]),gtk.Entry):
                self.vars[splitline[0]]=splitline[1]
            else:
                self.vars[splitline[0]]=int(splitline[1])

    def writeConfFile(self,filename):
        try:
            file=open(filename,"w")
        except:
            print "Could not write file "+filename

        varnames=self.vars.keys()
        varnames.sort()
        for varname in varnames:
            if isinstance(self.xmltree.get_widget(varname), gtk.Entry):
                file.write(varname+"="+self.vars[varname]+"\n")
            else:
                file.write("%s=%d\n" % (varname,self.vars[varname]))

        try:
            file.close()
        except:
            print "Could not write file "+filename
            

    def getVar(self,confname):
        if self.vars.has_key(confname):
            return self.vars[confname]
        widg=self.xmltree.get_widget(confname)
        if widg!=None:
            if isinstance(widg,gtk.Entry):
                return widg.get_text()
            else:
                return widg.props.active


    def generalHandler(self,widg):
        name=widg.get_name()

        if type(widg)== gtk.Button:
            if name=="Ok":
                self.writeConfFile(self.tempfilename)
                gtk.main_quit()
                return
            if name=="Cancel":
                gtk.main_quit()
                return
            if name=="Save":
                self.writeConfFile(self.conffilename)
                self.writeConfFile(self.tempfilename)
                if self.getVar("close_window_when_pressing_save")==1:
                    gtk.main_quit()
                return
            
            if name[:7]=="browse+":
                widgnamestrip=string.split(name,"+",1)
                widgname=widgnamestrip[1]
                self.fileselectors[widgname]=gtk.glade.XML(
                    os.path.abspath(os.path.dirname(sys.argv[0]))+"/../etc/ceresconfig.glade",widgname
                    )
                self.fileselectors[widgname].signal_autoconnect(handle_dict)
                widg=self.fileselectors[widgname].get_widget(widgname)
                textentry=self.xmltree.get_widget(widgname[3:])
                widg.set_filename(textentry.get_text())
            else:
                widgnamestrip=string.split(name,"-",1)
                widgname="fs_"+widgnamestrip[1]
                widg=self.fileselectors[widgname].get_widget(widgname)
                if widgnamestrip[1]=="fsok":
                    filename=widg.get_filename()
                    if widgname!="fs_frequency_file":
                        filename=os.path.dirname(filename)+"/"
                    textentry=self.xmltree.get_widget(widgnamestrip[1])
                    textentry.set_text(filename)
                    self.vars[widgnamestrip[1]]=filename
                widg.destroy()
                del self.fileselectors[widgname]
        else:
            if isinstance(widg,gtk.Entry):
                widgtext=widg.get_text()
                if name[:-1]=="temporary_path_":
                    if widgtext[-1]!="/":
                        widgtext=widgtext+"/"
                        widg.set_text(widgtext)
                self.vars[name]=widgtext
            else:
                self.vars[name]=widg.props.active
            
                
    def destroy(self):
        gtk.main_quit()

    def show(self):
        self.xmltree.signal_autoconnect(handle_dict)
        varnames=self.vars.keys()
        for varname in varnames:
            widget=self.xmltree.get_widget(varname)
            if isinstance(widget,  gtk.Entry):
                widget.set_text(self.vars[varname])
            else:
                widget.set_active(self.vars[varname])

        gtk.main()
        

def getVar(confname):
    try:
        return config.getVar(confname)
    except:
        traceback.print_exc(file=sys.stderr)

def generalHandler(obj):
    config.generalHandler(obj)


def destroy(obj):
    config.destroy()
    
def showConfig():
    try:
        tempfilename=tempfile.mktemp()
        config.writeConfFile(tempfilename)
        os.system(
            os.path.abspath(os.path.dirname(sys.argv[0]))
            + "/ceresconfig.py %s %s" % (config.conffilename,tempfilename)
            )
        config.readConfFile(config.conffilename)
        config.readConfFile(tempfilename)
        os.unlink(tempfilename)
    except:
        traceback.print_exc(file=sys.stderr)

handle_dict={
    "general":generalHandler,
    "on_Settings_destroy":destroy
    }


def ceresConfigStart(filename):
    global config
    a=sys.argv[0]
    b=os.path.dirname(a)
    c=os.path.abspath(b)
    d=c+"/../etc/ceresconfig.glade"
    config=Config(
        gtk.glade.XML(d,"Settings"),
        filename
        )
        

if __name__=="__main__":
    global config

    if len(sys.argv)>1 and (sys.argv[1]=="--help" or sys.argv[1]=="-h" or sys.argv[1]=="-help"):
        print
        print "Usage: %s [savefilename] [okfilename]" % sys.argv[0]
        print
        print "Default for both savefilename and okfilename is \"~/.ceres\""
        print "If only one argument is given, both savefilename and okfilename will be set to that value"
        print
        sys.exit(0)

    if len(sys.argv)==2:
        savefilename=sys.argv[1]
        okfilename=sys.argv[1]
    else:
        if len(sys.argv)==3:
            savefilename=sys.argv[1]
            okfilename=sys.argv[2]
        else:
            savefilename=os.path.expanduser("~/.ceres")
            okfilename=savefilename

    a=sys.argv[0]
    b=os.path.dirname(a)
    c=os.path.abspath(b)
    d=c+"/../etc/ceresconfig.glade"
    config=Config(
        gtk.glade.XML(d,"Settings"),
        savefilename
        )
    config.setTempFileName(okfilename)
    config.readConfFile(okfilename);
    config.show()






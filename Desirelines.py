# DesireLines.py
# Used for making desire lines from TOBS data
# Author: Andrew Rohne - arohne@oki.org - www.oki.org
# Date: 07-10-2012
# License: 2012 GPLv3

from Tkinter import *
from ttk import Combobox
import tkFileDialog, tkMessageBox
import arcpy, sys, os
from arcpy import env

class App:
    def __init__(self,master):
        #root.tk.call('wm','iconbitmap',self._w,'-default','iconfile.ico')
        #for above: http://www.jamesstroud.com/jamess-miscellaneous-how-tos/icons/creating-windows-icons
        #and http://www.jamesstroud.com/jamess-miscellaneous-how-tos/icons/tkinter-title-bar-icon
        self.titleText=Label(master,text="OKI Transit On-board Survey Processor").grid(row=0,column=0,columnspan=4)
        self.licenseText=Label(master,text="Licensed 2012 GPL v3").grid(row=1,column=0,columnspan=4)
        self.websiteText=Label(master,text="www.oki.org").grid(row=2,column=0,columnspan=4)
        
        self.workspaceLabel=Label(master,text="GIS Workspace:").grid(row=3,column=0)
        self.workspaceText=Text(master,height=1,width=50)
        self.workspaceText.grid(row=3,column=1)
        self.workspaceBrowse=Button(master,text="Browse MDB",command=self.loadTemplate).grid(row=3,column=2)
        self.workspaceFGDB=Button(master,text="Browse GDB",command=self.loadFolder).grid(row=3,column=3)
        
        self.tableLabel=Label(master,text="Table:").grid(row=4,column=0)
        self.tableLB=Combobox(master,values=["None yet"])
        self.tableLB.bind('<<ComboboxSelected>>',self.getFieldsFromTable)
        self.tableLB.grid(row=4,column=1)
        self.idLabel=Label(master,text="Survey IDs:").grid(row=4,column=2)
        self.idCombo=Combobox(master,values=["None yet"])
        self.idCombo.grid(row=4,column=3)
        
        self.oxLabel=Label(master,text="Origin X Field:").grid(row=5, column=0)
        self.oxCombo=Combobox(master,values=["None yet"])
        self.oxCombo.grid(row=5, column=1)
        self.oyLabel=Label(master,text="Origin Y Field:").grid(row=5, column=2)
        self.oyCombo=Combobox(master,values=["None yet"])
        self.oyCombo.grid(row=5,column=3)
        
        self.bxLabel=Label(master,text="Board X Field:").grid(row=6, column=0)
        self.bxCombo=Combobox(master,values=["None yet"])
        self.bxCombo.grid(row=6, column=1)
        self.byLabel=Label(master,text="Board Y Field:").grid(row=6, column=2)
        self.byCombo=Combobox(master,values=["None yet"])
        self.byCombo.grid(row=6,column=3)
        
        self.axLabel=Label(master,text="Alight X Field:").grid(row=7, column=0)
        self.axCombo=Combobox(master,values=["None yet"])
        self.axCombo.grid(row=7, column=1)
        self.ayLabel=Label(master,text="Alight Y Field:").grid(row=7, column=2)
        self.ayCombo=Combobox(master,values=["None yet"])
        self.ayCombo.grid(row=7,column=3)
        
        self.dxLabel=Label(master,text="Dest X Field:").grid(row=8, column=0)
        self.dxCombo=Combobox(master,values=["None yet"])
        self.dxCombo.grid(row=8, column=1)
        self.dyLabel=Label(master,text="Dest Y Field:").grid(row=8, column=2)
        self.dyCombo=Combobox(master,values=["None yet"])
        self.dyCombo.grid(row=8,column=3)
        
        self.goButton=Button(master,text="Go!",command=self.say_hi).grid(row=9,column=0)
        self.quitButton=Button(master,text="Quit",command=master.quit).grid(row=9,column=1)
        
    def say_hi(self):
        print "Do or do not.  There is no try"
        
    def loadTemplate(self):
        filename=tkFileDialog.askopenfilename(filetypes=(("Personal Geodatabases","*.mdb")))
        if(filename):
            try:
                self.workspaceText.insert(END,filename)
                env.workspace=filename
                
            except:
                tkMessageBox.showerror("Failed to read file")
                return
                
    def loadFolder(self):
        foldername=tkFileDialog.askdirectory()
        if(foldername):
            try:
                self.workspaceText.insert(END,foldername)
                env.workspace=foldername
                self.getTablesFromGdb()
            except:
                tkMessageBox.showerror("Failed to read folder")
                return
                
    def getTablesFromGdb(self):
        self.tableList=arcpy.ListTables()
        tl=()
        for table in self.tableList:
            tl=tl+(table,)
        self.tableLB['values']=tl
        
    def getFieldsFromTable(self,something):
        featClass=self.tableLB.get()
        try:
            fl=()
            if(featClass and featClass!=-1):
                fields=arcpy.ListFields(featClass)
                for field in fields:
                    fl=fl+(field.name,)
                self.oxCombo['values']=fl
                self.oyCombo['values']=fl
                self.bxCombo['values']=fl
                self.byCombo['values']=fl
                self.axCombo['values']=fl
                self.ayCombo['values']=fl
                self.dxCombo['values']=fl
                self.dyCombo['values']=fl
                self.idCombo['values']=fl
                
        except:
            return

root=Tk()
app=App(root)
root.mainloop()






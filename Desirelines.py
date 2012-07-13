# DesireLines.py
# Used for making desire lines from TOBS data
# Author: Andrew Rohne - arohne@oki.org - www.oki.org
# Date: 07-10-2012
# License: 2012 GPLv3

from Tkinter import *
from ttk import Combobox
import tkFileDialog, tkMessageBox
import arcpy, sys, os, math
from arcpy import env

class App:
    def __init__(self,master):
        #User Interface
        #TODO: Add progressbar so people know when the program is working
        root.title('Transit Survey Desire Lines')
        root.iconbitmap(default='busicon.ico')
        
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
        
        self.modeToLabel=Label(master,text="Mode To:").grid(row=5,column=0)
        self.modeToCombo=Combobox(master,values=["None yet"])
        self.modeToCombo.grid(row=5,column=1)
        self.modeFrLabel=Label(master,text="Mode From:").grid(row=5, column=2)
        self.modeFrCombo=Combobox(master,values=["None yet"])
        self.modeFrCombo.grid(row=5,column=3)
        
        self.oxLabel=Label(master,text="Origin X Field:").grid(row=6, column=0)
        self.oxCombo=Combobox(master,values=["None yet"])
        self.oxCombo.grid(row=6, column=1)
        self.oyLabel=Label(master,text="Origin Y Field:").grid(row=6, column=2)
        self.oyCombo=Combobox(master,values=["None yet"])
        self.oyCombo.grid(row=6,column=3)
        
        self.bxLabel=Label(master,text="Board X Field:").grid(row=7, column=0)
        self.bxCombo=Combobox(master,values=["None yet"])
        self.bxCombo.grid(row=7, column=1)
        self.byLabel=Label(master,text="Board Y Field:").grid(row=7, column=2)
        self.byCombo=Combobox(master,values=["None yet"])
        self.byCombo.grid(row=7,column=3)
        
        self.axLabel=Label(master,text="Alight X Field:").grid(row=8, column=0)
        self.axCombo=Combobox(master,values=["None yet"])
        self.axCombo.grid(row=8, column=1)
        self.ayLabel=Label(master,text="Alight Y Field:").grid(row=8, column=2)
        self.ayCombo=Combobox(master,values=["None yet"])
        self.ayCombo.grid(row=8,column=3)
        
        self.dxLabel=Label(master,text="Dest X Field:").grid(row=9, column=0)
        self.dxCombo=Combobox(master,values=["None yet"])
        self.dxCombo.grid(row=9, column=1)
        self.dyLabel=Label(master,text="Dest Y Field:").grid(row=9, column=2)
        self.dyCombo=Combobox(master,values=["None yet"])
        self.dyCombo.grid(row=9,column=3)
        
        self.breakerLabel=Label(master,text="The below are for graphing and are not needed for Desirelines").grid(row=10,column=0,columnspan=4)
        
        self.surveyBusLabel=Label(master,text="Survey Bus:").grid(row=11,column=0)
        self.surveyBusCombo=Combobox(master,values=["None yet"])
        self.surveyBusCombo.grid(row=11,column=1)
        self.firstBusLabel=Label(master,text="First Bus:").grid(row=11,column=2)
        self.firstBusCombo=Combobox(master,values=["None yet"])
        self.firstBusCombo.grid(row=11,column=3)
        
        self.goButton=Button(master,text="Create Desirelines!",command=self.buildDL).grid(row=12,column=0)
        self.quitButton=Button(master,text="Quit",command=master.quit).grid(row=12,column=1)
        self.graphOB=Button(master,text="Graph OB",command=self.graphOB).grid(row=12,column=2)
        self.graphAD=Button(master,text="Graph AD",command=self.graphAD).grid(row=12,column=3)
        
    def loadTemplate(self):
        #Loads a personal geodatabase file
        filename=tkFileDialog.askopenfilename(filetypes=(("Personal Geodatabases","*.mdb")))
        if(filename):
            try:
                self.workspaceText.insert(END,filename)
                env.workspace=filename
                
            except Exception as e:
                tkMessageBox.showerror("Failed to read file",e.message)
                return
                
    def loadFolder(self):
        #Loads a file geodatabase (looks like a folder to Windows Explorer, etc.)
        foldername=tkFileDialog.askdirectory()
        if(foldername):
            try:
                self.workspaceText.insert(END,foldername)
                env.workspace=foldername
                self.getTablesFromGdb()
            except Exception as e:
                tkMessageBox.showerror("Failed to read folder",e.message)
                return
                
    def getTablesFromGdb(self):
        #Gets a table list from the geodatabase and fills the table combobox
        self.tableList=arcpy.ListTables()
        tl=()
        for table in self.tableList:
            tl=tl+(table,)
        self.tableLB['values']=tl
        
    def getFieldsFromTable(self,something):
        #Gets the fields from the selected table and loads all (relevant) comboboxes
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
                self.modeToCombo['values']=fl
                self.modeFrCombo['values']=fl
                self.surveyBusCombo['values']=fl
                self.firstBusCombo['values']=fl
                
        except:
            return

    def buildDL(self):
        #this is the main process to build the desire lines
        try:
            #Check Inputs
            if self.idCombo.get() and self.modeToCombo.get() and self.modeFrCombo.get() and self.oxCombo.get() and self.oyCombo.get() and self.bxCombo.get() and self.byCombo.get() and self.axCombo.get() and self.ayCombo.get() and self.dxCombo.get() and self.dyCombo.get():
                SurveyIDField=self.idCombo.get()
                ModeToField=self.modeToCombo.get()
                ModeFrField=self.modeFrCombo.get()
                OXField=self.oxCombo.get()
                OYField=self.oyCombo.get()
                BXField=self.bxCombo.get()
                BYField=self.byCombo.get()
                AXField=self.axCombo.get()
                AYField=self.ayCombo.get()
                DXField=self.dxCombo.get()
                DYField=self.dyCombo.get()
                
                #Origin ~> Boarding 
                OutputFC="OBDesireLines"
                arcpy.CreateFeatureclass_management(env.workspace,OutputFC,"POLYLINE")
                arcpy.AddField_management(OutputFC,"SurveyID","LONG")
                arcpy.AddField_management(OutputFC,"ModeTo","LONG")
                arcpy.AddField_management(OutputFC,"ModeFrom","LONG")
                arcpy.AddField_management(OutputFC,"DistanceSL","DOUBLE")
                rows=arcpy.SearchCursor(self.tableLB.get())
                insRows=arcpy.InsertCursor(OutputFC)
                x=1
                for row in rows:
                    if(x % 100 == 0):
                        print "Working on ",x
                    insRow=insRows.newRow()
                    insRow.SurveyID=row.getValue(SurveyIDField)
                    insRow.ModeTo=row.getValue(ModeToField)
                    insRow.ModeFrom=row.getValue(ModeFrField)
                    lineArray=arcpy.Array()
                    pnt1=arcpy.Point()
                    pnt2=arcpy.Point()
                    if(row.getValue(OXField) and row.getValue(OYField) and row.getValue(BXField) and row.getValue(BYField)):
                        pnt1.X=row.getValue(OXField)
                        pnt1.Y=row.getValue(OYField)
                        lineArray.add(pnt1)
                        pnt2.X=row.getValue(BXField)
                        pnt2.Y=row.getValue(BYField)
                        lineArray.add(pnt2)
                        insRow.shape=lineArray
                        insRow.DistanceSL=math.sqrt(math.pow(pnt2.X-pnt1.X,2)+math.pow(pnt2.Y-pnt1.Y,2))
                    
                    insRows.insertRow(insRow)
                    x+=1
                    
                #Alight ~> Destination
                OutputFC="ADDesireLines"
                arcpy.CreateFeatureclass_management(env.workspace,OutputFC,"POLYLINE")
                arcpy.AddField_management(OutputFC,"SurveyID","LONG")
                arcpy.AddField_management(OutputFC,"ModeTo","LONG")
                arcpy.AddField_management(OutputFC,"ModeFrom","LONG")
                arcpy.AddField_management(OutputFC,"DistanceSL","DOUBLE")
                rows=arcpy.SearchCursor(self.tableLB.get())
                insRows=arcpy.InsertCursor(OutputFC)
                x=1
                for row in rows:
                    if(x % 100 == 0):
                        print "Working on ",x
                    insRow=insRows.newRow()
                    insRow.SurveyID=row.getValue(SurveyIDField)
                    insRow.ModeTo=row.getValue(ModeToField)
                    insRow.ModeFrom=row.getValue(ModeFrField)
                    lineArray=arcpy.Array()
                    pnt1=arcpy.Point()
                    pnt2=arcpy.Point()
                    if(row.getValue(AXField) and row.getValue(AYField) and row.getValue(DXField) and row.getValue(DYField)):
                        pnt1.X=row.getValue(AXField)
                        pnt1.Y=row.getValue(AYField)
                        lineArray.add(pnt1)
                        pnt2.X=row.getValue(DXField)
                        pnt2.Y=row.getValue(DYField)
                        lineArray.add(pnt2)
                        insRow.shape=lineArray
                        insRow.DistanceSL=math.sqrt(math.pow(pnt2.X-pnt1.X,2)+math.pow(pnt2.Y-pnt1.Y,2))
                    
                    insRows.insertRow(insRow)
                    x+=1
                    
                #TODO: add something about progress
            else:
                tkMessageBox.showerror("Error Creating Featureclass","You need to select a field for ALL input boxes!")
        except Exception as e:
            tkMessageBox.showerror("Error Creating Featureclass",e.message)
            
    def graphOB(self):
        #Graphs Origin-Boarding Locations
        try:
            #Check Inputs
            if 1==1: 
                #self.modeToCombo.get() and self.oxCombo.get() and self.oyCombo.get() and self.bxCombo.get() and self.byCombo.get() and self.surveyBusCombo.get() and self.firstBusCombo.get():
                ###Not needed
                #SurveyIDField=self.idCombo.get()
                #ModeFrField=self.modeFrCombo.get()
                #AXField=self.axCombo.get()
                #AYField=self.ayCombo.get()
                #DXField=self.dxCombo.get()
                #DYField=self.dyCombo.get()
                
                ## Debugging
                ##ModeToField=self.modeToCombo.get()
                ModeToField="OGET"
                ##OXField=self.oxCombo.get()
                OXField="OXCORD"
                ##OYField=self.oyCombo.get()
                OYField="OYCORD"
                ##BXField=self.bxCombo.get()
                BXField="BX"
                ##BYField=self.byCombo.get()
                BYField="BY_"
                ##sBusField=self.surveyBusCombo.get()
                sBusField="RTCODE"
                ##fBusField=self.firstBusCombo.get()
                fBusField="BUS1"
                #read all this stuff into an array
                rows=arcpy.SearchCursor(self.tableLB.get())
                x=1
                rowData=[]
                for row in rows:
                    if(x % 100 == 0):
                        print "Reading on ",x
                    if(row.getValue(sBusField)==row.getValue(fBusField)):
                        #iRow=[][] #mode, distance
                        if(row.getValue(OXField)>0 and row.getValue(BXField)>0 and row.getValue(OYField)>0 and row.getValue(BYField)>0):
                            iRow=[row.getValue(ModeToField),math.sqrt(math.pow(row.getValue(OXField)-row.getValue(BXField),2)+math.pow(row.getValue(OYField)-row.getValue(BYField),2))/5280]
                            rowData.append(iRow)
                fbefore=open('C:\\temp\\beforesort.txt','w')
                for item in rowData:
                    fbefore.write(str(item[1]))
                    fbefore.write('\n')
                fbefore.close()
                newRowData=self.sortList(rowData)
                fafter=open('C:\\temp\\aftersort.txt','w')
                for item in newRowData:
                    fafter.write(str(item[1]))
                    fafter.write('\n')
                fafter.close()
                
                print "DBG: graph creation"
                
                
                print "Completed for now"

        except Exception as e:
            tkMessageBox.showerror("Problem somewhere",e.message)
    
    def graphAD(self):
        print "This is not the subroutine you are looking for"
        #if self.idCombo.get() and self.modeToCombo.get() and self.modeFrCombo.get() and self.oxCombo.get() and self.oyCombo.get() and self.bxCombo.get() and self.byCombo.get() and self.axCombo.get() and self.ayCombo.get() and self.dxCombo.get() and self.dyCombo.get() and self.surveyBusCombo.get() and self.firstBusCombo.get():
                        
    def sortList(self,list):
        print "Sorting..."
        recs=len(list)
        outputlist=[]
        currentlowest=[]
        while len(outputlist)<recs:
            for item in list:
                if(currentlowest==[]):
                    currentlowest=item
                for itemcompare in list:
                    if(itemcompare[1]<item[1]):
                        item=itemcompare
                #At this point, item should be the smallest distance in list
                outputlist.append(item)
                list.remove(item)
        print "Sorting complete..."
        return outputlist
                
                
        
        
        ### This was the initial sort method.  It is SLOW ###
        #performs a bubble sort on the distance field maintaining the mode
        #outputlist=[]
        #spass=1
        #keepgoing=1
        #while keepgoing>0:
        #    print "DBG: Sorting pass ",spass
        #    spass+=1
        #    switched=0
        #    for tmp1 in list:
        #        a=list.index(tmp1)
        #        if(a<len(list)-1):
        #            tmp2=list[a+1]
        #            if(tmp1[1]<tmp2[1]):
        #                list.remove(tmp1)
        #                outputlist.append(tmp1)
        #                switched+=1
        #            else:
        #                list.remove(tmp2)
        #                outputlist.append(tmp2)
        #    if(switched==0):
        #        keepgoing=0
        #            
        #    list=outputlist
        #return list
        
            
root=Tk()
app=App(root)
root.mainloop()






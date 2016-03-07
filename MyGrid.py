#!/usr/bin/python
import wx
import wx.grid as gridlib
from wx.lib.pubsub import Publisher as pub
import project
from Dialouge import *
from GridTable import *
import globaldata

class MyGrid(gridlib.Grid):
    def __init__(self, parent, data, name):
        gridlib.Grid.__init__(self, parent, -1)
        self.data = data
        self.name = name
        tableBase = GenericTable(data, globaldata.rowLabels, globaldata.colLabels)
        self.SetTable(tableBase)                    
        # self.SetGridLineColour(wx.RED)
        self.SetRowLabelSize(-1) 
        self.SetColLabelSize(-1) 
        self.SetColMinimalAcceptableWidth(100)
        # self.SetColMinimalWidth(1,150)
        # self.EnableCellEditControl(False)   
        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnCellDoubleClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellDoubleClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.ShowPopupMenu)
        pub.subscribe(self.Resize, 'RESIZE_CELLS') 

    def OnLunchClick(self, i, j, e):
        print i, j
        self.dia = wx.Dialog(self, -1, 'Enter Lunch Details', size=(300,50))
        self.dia.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dia.mainSizer.AddSpacer(10)

        self.dia.label1 = wx.StaticText(self.dia, label='Enter Class:')
        # self.dia.field1 = wx.TextCtrl(self.dia, value="")
        self.dia.field1 = PromptingComboBox(self.dia, "Choose", globaldata.class_shortnames[1:], 'Class') 

        self.dia.mainSizer.Add(self.dia.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.dia.mainSizer.Add(self.dia.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)

        self.dia.okbutton = wx.Button(self.dia, label="OK", id=wx.ID_OK)
        self.dia.mainSizer.Add(self.dia.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.dia.mainSizer.AddSpacer(10)
        
        self.dia.SetSizer(self.dia.mainSizer)
        self.dia.result = None
        self.dia.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.dia.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.dia.ShowModal()
        # if self.dia.ShowModal()  == wx.ID_CANCEL:
        #     return
        # self.dia.result1
        try:
            project.insert_lunch(self.dia.result1, i, j)
            pub.sendMessage('UPDATE_VIEW', data = None)
        except Exception as e:
            s = 'Conflict with: '
            for t in e.value:
                for e in t:
                    if e != None:
                        s += str(e) + ' '
                s += '\n'
            dlg = wx.MessageDialog(None, s , "ERROR", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        e.Skip()

    def onOK(self, event):
        self.dia.result1 = self.dia.field1.res
        self.dia.Destroy()

    def onCancel(self, event):
        self.Destroy()

    def OnDeleteEntry(self, a, b, event):
        # print 'all_teachers', globaldata.all_teachers
        # print 'all_venues', globaldata.all_venues
        # print 'all_classes', globaldata.all_classes
        entry = self.data[a][b]
        itemId = event.GetId()
        menu = event.GetEventObject()
        menuItem = menu.FindItemById(itemId)
        deleteId = int(menuItem.GetLabel().split()[2]) - 1
        entryLength = len(entry[deleteId]) 
        print 'name and to delete', self.name, entry[deleteId]
        if entryLength < 3:
            if entry[deleteId][1] == None:
                project.remove_lunch(self.name, a, b)
            else:
                project.remove_lunch(self.name+'-'+entry[deleteId][1] , a, b)
        else:
            if entry[deleteId][3] == None:
                newname = self.name
            else:
                newname = self.name + '-' + str(entry[deleteId][3])

            f = str(entry[deleteId][0])
            if f.split("-")[0] not in globaldata.all_teachers:
                #it means its teachers table
                project.remove_all(newname, f, str(entry[deleteId][1]), a, b)
            else:
                g = str(entry[deleteId][1])
                if g.split("-")[0] not in globaldata.all_venues:
                    project.remove_all(f, newname, g, a, b)
                else:
                    project.remove_all(f, g, newname, a, b)
            # else:   #let's hope it is class's matrix due to use of batches
            #     project.remove_all(str(entry[deleteId][0]), str(entry[deleteId][1]), self.name+'-'+ str(entry[deleteId][3]), a, b)

        pub.sendMessage('UPDATE_VIEW', data = None)

    def ShowPopupMenu(self, evt):
        i = evt.GetRow()
        j = evt.GetCol()

        menu = wx.Menu()
        l = menu.Append(-1, "Insert Lunch")
        self.Bind(wx.EVT_MENU, lambda evt, a=i, b=j: self.OnLunchClick(a, b, evt) , l)

###### see how submenu works
   
        entry = self.data[i][j]
        # print entry
        # entry = entry.split('\n')[:-1]
        # print entry
        # imp = wx.Menu()        
        # for i in range(len(entry)):
            # imp.Append(-1,'Delete Entry '+ str(i+1))
        # m = menu.AppendMenu(104,'Delete Entry', imp)
        try:
            for n in range(len(entry)):
                l = menu.Append(-1, "Delete Entry " + str(n+1))
                self.Bind(wx.EVT_MENU, lambda evt, a=i, b=j: self.OnDeleteEntry(a, b, evt) , l)
            # self.Bind(wx.EVT_MENU, self.OnDeleteEntry , l)
#############
        except:
            pass

        self.PopupMenu(menu)
        menu.Destroy()

    def OnCellDoubleClick(self, evt):
        dlg = Dialoge(self)
        dlg.ShowModal()
        # if dlg.ShowModal()  == wx.ID_CANCEL:
        #     return 
        print (dlg.result1, dlg.result2, dlg.result3, dlg.result4, evt.GetRow(),evt.GetCol())

        try:
            project.insert_entry(dlg.result1, dlg.result2, dlg.result3, dlg.result4, evt.GetRow(),evt.GetCol())
            pub.sendMessage('UPDATE_VIEW', data = None)
        except Exception as e:
            print e
            s = 'Conflict with: '
            for t in e.value:
                for e in t:
                    if e != None:
                        s += str(e) + ' '
                s += '\n'
            dlg = wx.MessageDialog(None, s , "ERROR", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        evt.Skip()

    def Resize(self, evt):
        self.AutoSizeColumns()
        self.AutoSize()
        # evt.Skip()
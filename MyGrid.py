#!/usr/bin/python
import wx
import wx.grid as gridlib
from wx.lib.pubsub import pub
import project
from Dialouge import *
from GridTable import *
import globaldata
import copy

class MyGrid(gridlib.Grid):
    def __init__(self, parent, data, name, typeOf):
        gridlib.Grid.__init__(self, parent, -1)
        self.data = data
        self.name = name
        self.type = typeOf
        tableBase = GenericTable(data, globaldata.rowLabels, globaldata.colLabels)
        self.SetTable(tableBase)                    
        # self.SetGridLineColour(wx.RED)
        self.SetRowLabelSize(-1) 
        self.SetColLabelSize(-1) 
        self.SetColMinimalAcceptableWidth(100)
        # self.SetColMinimalWidth(1,150)
        # self.EnableCellEditControl(False) 
        wx.EVT_KEY_DOWN(self, self.KeyPressed)  
        # self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.HandelManualInput)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellDoubleClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.ShowPopupMenu)
        pub.subscribe(self.Resize, 'RESIZE_CELLS') 

    def OnSelectCell(self, event):
        
        self.rowSelect = event.GetRow()
        self.colSelect = event.GetCol()
        # print 'selected', self.rowSelect, self.colSelect
        event.Skip()

    def ParseIntoClipboard(self, clipboard):
        #make actual copy of it so as to not modify main table
        clip = copy.deepcopy(clipboard)
        if self.type == 'Teacher':
            for i in range(len(clip)):
                if clip[i][-1] != None:
                    temp = self.name + '-' + clip[i][-1]
                else:                    
                    temp = self.name
                clip[i] = (temp, ) + clip[i]
                # e = (temp,) + e 
            # globaldata.clipboard = clip
        if self.type == 'Venue':
            for i in range(len(clip)):
                if clip[i][-1] != None:
                    temp = self.name + '-' + clip[i][-1]
                else:                    
                    temp = self.name

                clip[i] = list(clip[i])
                clip[i].insert(1,temp)
                clip[i] = tuple(clip[i])

            # globaldata.clipboard = clip
        if self.type == 'Class':
            for i in range(len(clip)):
                if clip[i][-1] != None:
                    temp = self.name + '-' + clip[i][-1]
                else:                    
                    temp = self.name

                clip[i] = list(clip[i])
                clip[i].insert(2,temp)
                clip[i] = tuple(clip[i])
        globaldata.clipboard = copy.deepcopy(clip)
    def KeyPressed(self, event):
        
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            clipboard  = self.data[self.rowSelect][self.colSelect]
            self.ParseIntoClipboard(clipboard)
            print 'Copied', globaldata.clipboard
        
        # If Ctrl+V is pressed...
        if event.ControlDown() and event.GetKeyCode() == 86:
            self.HandelManualInput()
            print 'Pasted', globaldata.clipboard
        
        # If Ctrl+X is pressed...
        if event.ControlDown() and event.GetKeyCode() == 88:
            clipboard  = self.data[self.rowSelect][self.colSelect]
            self.ParseIntoClipboard(clipboard)
            #clear that cell from everywhere 
            #global delete
            for i in range(len(clipboard)):
                self.RemoveEntryFromTables(clipboard, 0)
            print 'Cut', globaldata.clipboard
        
        # If del is pressed...
        # if event.GetKeyCode() == 127:
        
        #Skip other Key events
        if event.GetKeyCode():
            event.Skip()
            return

    def HandelManualInput(self):
        i = self.rowSelect
        j = self.colSelect
        for e in globaldata.clipboard:
            if len(e) == 3:
                try:
                    project.insert_lunch(e[-1], i, j)
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
            else:
                t = e[0]
                v = e[1]
                c = e[2]
                s = e[3]            
                try:
                    project.insert_entry(t, v, c, s, i, j)
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
        return

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
        print 'name and to delete', self.name, entry[deleteId]

        self.RemoveEntryFromTables(entry, deleteId)

    def RemoveEntryFromTables(self, entry, deleteId):
        print entry
        print deleteId
        entryLength = len(entry[deleteId]) 
        a = self.rowSelect
        b = self.colSelect

        if entryLength < 3:
            if entry[deleteId][1] == None:
                project.remove_lunch(self.name, a, b)
            else:
                project.remove_lunch(self.name+'-'+entry[deleteId][-1] , a, b)

        elif entryLength == 5:
            t = entry[deleteId][0]
            v = entry[deleteId][1]
            c = entry[deleteId][2]
            project.remove_all(t, v, c, a, b)

        else:
            
            if entry[deleteId][3] == None:
                newname = self.name
            else:
                newname = self.name + '-' + str(entry[deleteId][3])

            f = str(entry[deleteId][0])
            if f.split("-")[0] not in globaldata.all_teachers:
                # it means its teachers table
                project.remove_all(newname, f, str(entry[deleteId][1]), a, b)
            else:
                g = str(entry[deleteId][1])
                if g.split("-")[0] not in globaldata.all_venues:
                    project.remove_all(f, newname, g, a, b)
                else:
                    project.remove_all(f, g, newname, a, b)

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
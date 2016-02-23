#!/usr/bin/python
import wx
import wx.grid as gridlib
from wx.lib.pubsub import Publisher as pub
import project
from Dialouge import *
from GridTable import *
import globaldata

class MyGrid(gridlib.Grid):
    def __init__(self, parent, data):
        gridlib.Grid.__init__(self, parent, -1)
        tableBase = GenericTable(data, globaldata.rowLabels, globaldata.colLabels)
        self.SetTable(tableBase)                    
        # self.SetGridLineColour(wx.RED)
        self.SetRowLabelSize(-1) 
        self.SetColLabelSize(-1) 
        self.SetColMinimalAcceptableWidth(150)
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

    def ShowPopupMenu(self, evt):
        menu = wx.Menu()
        i = evt.GetRow()
        j = evt.GetCol()
        l = menu.Append(-1, "Insert Lunch")
        self.Bind(wx.EVT_MENU, lambda evt, a=i, b=j: self.OnLunchClick(a, b, evt) , l)
        self.PopupMenu(menu)
        menu.Destroy()

    def OnCellDoubleClick(self, evt):
        dlg = Dialoge(self)
        dlg.ShowModal()
        # if dlg.ShowModal()  == wx.ID_CANCEL:
        #     return 
        try:
            project.insert_entry(dlg.result1, dlg.result2, dlg.result3, dlg.result4, evt.GetRow(),evt.GetCol())
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
        evt.Skip()

    def Resize(self, evt):
        self.AutoSize()
        # self.AutoSizeColumns()
        # evt.Skip()
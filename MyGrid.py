#!/usr/bin/python
import wx
import wx.grid as gridlib
from wx.lib.pubsub import Publisher as pub
import project
from Dialouge import *
from GridTable import *

class MyGrid(gridlib.Grid):
    def __init__(self, parent, data):
        gridlib.Grid.__init__(self, parent, -1)
        tableBase = GenericTable(data, rowLabels, colLabels)
        self.SetTable(tableBase)                    
        # self.SetGridLineColour(wx.RED)
        self.SetRowLabelSize(-1) 
        self.SetColLabelSize(-1) 
        self.SetColMinimalAcceptableWidth(100)
        # self.SetColMinimalWidth(1,150)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellDoubleClick)
        pub.subscribe(self.Resize, 'RESIZE_CELLS') 

    def OnCellDoubleClick(self, evt):
        dlg = Dialoge(self)
        dlg.ShowModal()
        try:
            project.insert_entry(dlg.result1, dlg.result2, dlg.result3, dlg.result4, evt.GetRow(),evt.GetCol())
            pub.sendMessage('UPDATE_VIEW', data = None)
        except:
            pass
        evt.Skip()

    def Resize(self, evt):
        # self.AutoSize()
        self.AutoSizeColumns(setAsMin=False)
        # evt.Skip()

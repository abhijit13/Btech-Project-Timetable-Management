#!/usr/bin/python

import project
import wx
import wx.grid as gridlib
from wx.lib.pubsub import Publisher as pub

class MyGrid(gridlib.Grid):
    backup = ''
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        self.CreateGrid(7, 11)
 
        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        # self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        pub.subscribe(self.set_value, 'ENTRY') 
    # def OnCellLeftClick(self, evt):
    #     print "OnCellLeftClick: (%d,%d) %s\n" % (evt.GetRow(),
    #                                              evt.GetCol(),
    #                                              evt.GetPosition())
    #     evt.Skip()
 
    def set_value(self, value):
        value = value.data
        self.SetCellValue(value[0], value[1], value[2])

    def OnLabelLeftClick(self, evt):
        print "OnLabelLeftClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                  evt.GetCol(),
                                                  evt.GetPosition())
        project.print_all_tables()
        evt.Skip()
 
    def OnCellChange(self, evt):
        # print "OnCellChange: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(), evt.GetPosition())
 
        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        self.value = self.GetCellValue(evt.GetRow(), evt.GetCol())
        if self.value == '':
            self.value = backup.split()
            self.value.extend([str(evt.GetRow()), str(evt.GetCol())])
            project.main('-'.join(self.value)) 
            pub.sendMessage('ENTRY', data = [evt.GetRow(), evt.GetCol(), ''])

        else: 
            try:
                project.main(self.value + ' ' +str(evt.GetRow()) + ' ' +str(evt.GetCol())) 
                # super(self).SetCellValue(evt.GetRow(), evt.GetCol(), '')                
            except:
                self.SetCellValue(evt.GetRow(), evt.GetCol(), '')
            else:
                pub.sendMessage('ENTRY', data = [evt.GetRow(), evt.GetCol(), self.value])

        # print value 
        # if value == 'no good':
        #     self.moveTo = evt.GetRow(), evt.GetCol()

    def OnSelectCell(self, evt):
        global backup   # very dirty fix this
        if evt.Selecting():
            print  'Selected'
        else:
            msg = 'Deselected'
        if self.GetCellValue(evt.GetRow(), evt.GetCol()) != '':
            backup = self.GetCellValue(evt.GetRow(), evt.GetCol())
            print 'backup', backup
        # print "OnSelectCell: %s (%d,%d) %s\n" % (msg, evt.GetRow(),
        #                                          evt.GetCol(), evt.GetPosition())
 

    #     # Another way to stay in a cell that has a bad value...
    #     row = self.GetGridCursorRow()
    #     col = self.GetGridCursorCol()
 
    #     if self.IsCellEditControlEnabled():
    #         self.HideCellEditControl()
    #         self.DisableCellEditControl()
 
    #     value = self.GetCellValue(row, col)
        
    #     if value == 'no good 2':
    #         return  # cancels the cell selection
 
        evt.Skip()
 
    # def OnEditorHidden(self, evt):
    #     if evt.GetRow() == 6 and evt.GetCol() == 3 and \
    #        wx.MessageBox("Are you sure you wish to  finish editing this cell?",
    #                     "Checking", wx.YES_NO) == wx.NO:
    #         evt.Veto()
    #         return
 
    #     print "OnEditorHidden: (%d,%d) %s\n" % (evt.GetRow(),
    #                                             evt.GetCol(),
    #                                             evt.GetPosition())
    #     evt.Skip()
 
class MyForm(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Timetable Management")
        self.tabbed = wx.Notebook(self, -1, style=(wx.NB_TOP))
            
        self.panel1 = wx.Panel(self.tabbed, -1)
        self.panel2 = wx.Panel(self.tabbed, -1)
        self.panel3 = wx.Panel(self.tabbed, -1)

    	self.teacher = MyGrid(self.panel1)
    	self.venue = MyGrid(self.panel2)
    	self.Class = MyGrid(self.panel3)

    	self.sizer1 = wx.BoxSizer(wx.VERTICAL)
    	self.sizer2 = wx.BoxSizer(wx.VERTICAL)
    	self.sizer3 = wx.BoxSizer(wx.VERTICAL)
    	
    	self.sizer1.Add(self.teacher, 1, wx.EXPAND)
    	self.sizer2.Add(self.venue, 1, wx.EXPAND)
    	self.sizer3.Add(self.Class, 1, wx.EXPAND)
            
    	self.panel1.SetSizer(self.sizer1)
        self.panel2.SetSizer(self.sizer2)
        self.panel3.SetSizer(self.sizer3)
            
    	self.tabbed.AddPage(self.panel1, "Teacher")
        self.tabbed.AddPage(self.panel2, "Venue")	
        self.tabbed.AddPage(self.panel3, "Class")	
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame1 = MyForm().Show()
    app.MainLoop()

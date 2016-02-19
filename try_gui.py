#!/usr/bin/python

import project
import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel
from wx.lib.pubsub import Publisher as pub

rowLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
colLabels = ['9-10','10-11', '11-12', '12-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7']

class Dialoge(wx.Dialog):
    def __init__(self, parent, id=-1, title="Enter Values"):
        wx.Dialog.__init__(self, parent, id, title,size=(600,50))
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.AddSpacer(10)
        self.label1 = wx.StaticText(self, label="Teacher:")
        self.field1 = wx.TextCtrl(self, value="")
        self.label2 = wx.StaticText(self, label="Venue:")
        self.field2 = wx.TextCtrl(self, value="")
        self.label3 = wx.StaticText(self, label="Class:")
        self.field3 = wx.TextCtrl(self, value="")
        self.label4 = wx.StaticText(self, label="Subject:")
        self.field4 = wx.TextCtrl(self, value="")
                
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)

        self.mainSizer.Add(self.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)

        self.SetSizer(self.mainSizer)
        self.result = None

    def onOK(self, event):
        self.result1 = self.field1.GetValue()
        self.result2 = self.field2.GetValue()
        self.result3 = self.field3.GetValue()
        self.result4 = self.field4.GetValue()
        self.Destroy()

    def onCancel(self, event):
        self.result = None
        self.Destroy()


class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
        
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
        
    def IsEmptyCell(self, row, col):
        return self.data[row][col] == None

    def GetValue(self, row, col):
        if self.data[row][col] == None:
            return ''
        else:
            res = ''
            for i in range(len(self.data[row][col])):
                for j in range(len(self.data[row][col][i])):
                    if self.data[row][col][i][j] != None:
                        t = str(self.data[row][col][i][j]) + ' '
                        res += t
                res += '\n'

        #to fix - there's some garbage at the end of line
            # print res    
            return res
            # return self.data[row][col]

    def SetValue(self, row, col, value):
        print 'set value', row, col, value
        #deletion not perfect - when cell has batch entries it wont work
        if value == '':
            data = self.data[row][col]
            if len(data) == 4:
                project.remove_all(data[0], data[1], data[2], row, col)
            else:
                project.remove_lunch(data[1], row, col)
        else:
            value = value.split(' ')
            try:
                project.insert_entry(value[0], value[1], value[2], value[3], row, col)
            except:
                print 'Cant update cell', row, col
        pub.sendMessage('UPDATE_VIEW', data = None)



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
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        pub.subscribe(self.Resize, 'RESIZE_CELLS') 


    def OnCellDoubleClick(self, evt):
        dlg = Dialoge(self)
        dlg.ShowModal()
        # print (dlg.result1 + '\n' + dlg.result2 + '\n' + dlg.result3 + '\n' + dlg.result4)
        try:
            project.insert_entry(dlg.result1, dlg.result2, dlg.result3, dlg.result4, evt.GetRow(),evt.GetCol())
            # print 'insrted'
            pub.sendMessage('UPDATE_VIEW', data = None)
        except:
            pass
        evt.Skip()

    def Resize(self, evt):
        # self.AutoSize()
        self.AutoSizeColumns(setAsMin=False)
        # evt.Skip()

    def OnLabelLeftClick(self, evt):
        # self.AutoSize()
        # print self.GetColMinimalWidth()
        project.print_all_tables()
        evt.Skip()
 
    def OnCellChange(self, evt):
        # print 'yo'
        # pub.sendMessage('UPDATE_VIEW', data = None)
        evt.Skip()

    def OnCellLeftClick(self, evt):
        evt.Skip()

class MyForm(wx.Frame):
    def update(self, value):
        # font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        # font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        # font.SetPointSize(11)
        
        for teacher in project.all_teachers:
            name = teacher.name
            if not hasattr(self, name):
                hfirst = wx.StaticText(self.panel1, label='College of Engineering, Pune - 05')
                hsecond = wx.StaticText(self.panel1, label='Department of Computer Engineering and IT')
                hthird = wx.StaticText(self.panel1, label='F.Y. Btech Computer Engineering')
                hfourth = wx.StaticText(self.panel1, label=teacher.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
                hfirst.SetFont(self.fonth1)
                hsecond.SetFont(self.fonth2)
                hthird.SetFont(self.fonth3)     
                hfourth.SetFont(self.fonth4)

                vbox = wx.BoxSizer(wx.VERTICAL)
                vbox.AddSpacer(150)
                vbox.Add(hfirst, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hsecond, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(2)
                vbox.Add(hthird, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hfourth, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(20)
                self.sizer1.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                self.temp = MyGrid(self.panel1, teacher.mat)
                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer1.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer1.AddSpacer(200)
                self.sizer1.Layout()

        for venue in project.all_venues:
            name = venue.name
            if not hasattr(self, name):
                self.temp = MyGrid(self.panel2, venue.mat)        
                hfirst = wx.StaticText(self.panel2, label='College of Engineering, Pune - 05')
                hsecond = wx.StaticText(self.panel2, label='Department of Computer Engineering and IT')
                hthird = wx.StaticText(self.panel2, label='F.Y. Btech Computer Engineering')
                hfourth = wx.StaticText(self.panel2, label=venue.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
                hfirst.SetFont(self.fonth1)
                hsecond.SetFont(self.fonth2)
                hthird.SetFont(self.fonth3)     
                hfourth.SetFont(self.fonth4)

                vbox = wx.BoxSizer(wx.VERTICAL)
                vbox.AddSpacer(150)
                vbox.Add(hfirst, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hsecond, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(2)
                vbox.Add(hthird, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hfourth, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(20)
                self.sizer2.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer2.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer2.AddSpacer(200)
                self.sizer2.Layout()

        for Class in project.all_classes:
            name = Class.name
            if not hasattr(self, name):
                self.temp = MyGrid(self.panel3, Class.mat)        
                hfirst = wx.StaticText(self.panel3, label='College of Engineering, Pune - 05')
                hsecond = wx.StaticText(self.panel3, label='Department of Computer Engineering and IT')
                hthird = wx.StaticText(self.panel3, label='F.Y. Btech Computer Engineering')
                hfourth = wx.StaticText(self.panel3, label=Class.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
                hfirst.SetFont(self.fonth1)
                hsecond.SetFont(self.fonth2)
                hthird.SetFont(self.fonth3)     
                hfourth.SetFont(self.fonth4)
                
                vbox = wx.BoxSizer(wx.VERTICAL)
                vbox.AddSpacer(150)
                vbox.Add(hfirst, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hsecond, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(2)
                vbox.Add(hthird, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hfourth, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(20)
                self.sizer3.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer3.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer3.AddSpacer(200)
                self.sizer3.Layout()

        self.panel1.SendSizeEvent()
        self.panel1.Layout()
        self.panel2.SendSizeEvent()
        self.panel2.Layout()
        self.panel3.SendSizeEvent()
        self.panel3.Layout()
        self.SendSizeEvent()        
        self.Layout()

        pub.sendMessage('RESIZE_CELLS', data = None)

    def __init__(self):

        wx.Frame.__init__(self, parent=None, title="Timetable Management")
        self.mainPanel = wx.Panel(self, -1)
        self.book = wx.Notebook(self.mainPanel, -1, style=(wx.NB_BOTTOM))

        self.panel1 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.book, id = -1)
        self.panel1.SetupScrolling()
        self.panel2 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.book, id = -1)
        self.panel2.SetupScrolling() 
        self.panel3 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.book, id = -1)
        self.panel3.SetupScrolling()

        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        dummy = [[None for i in range(10)] for j in range(7)]
        self.dummy = MyGrid(self.panel1, dummy)
        # html = wx.html.HtmlWindow(self.panel1)
        # text = wx.StaticText(self.panel1, label="Input:")
        # width = 200  # panel width
        # text.Wrap(width)

        # text = wx.StaticText(self.panel1, -1, 'College Of Engineering Pune', (20, 100))
        self.fonth1 = wx.Font(18, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.fonth2 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth4 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth4.SetUnderlined(True)

        # fonth4 = wx.Font(16, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        # text.SetFont(font)
        # hbox1.Add(st1, flag=wx.RIGHT, border=8)
        # font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        # font.SetPointSize(11)
        hfirst = wx.StaticText(self.panel1, label='College of Engineering, Pune - 05')
        hsecond = wx.StaticText(self.panel1, label='Department of Computer Engineering and IT')
        hthird = wx.StaticText(self.panel1, label='S.Y. Btech Computer Engineering')
        hthird.SetForegroundColour(wx.Colour(255,55,125))
        hfourth = wx.StaticText(self.panel1, label='Global Input:')

        hfirst.SetFont(self.fonth1)
        hsecond.SetFont(self.fonth2)
        hthird.SetFont(self.fonth3)
        hfourth.SetFont(self.fonth4)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.dummy, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(150)
        vbox.Add(hfirst, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(hsecond, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(2)
        vbox.Add(hthird, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(hfourth, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(20)
        self.sizer1.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer1.Add(vbox1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer1.AddSpacer(200)


        self.panel1.SetSizer(self.sizer1)
        self.panel2.SetSizer(self.sizer2)
        self.panel3.SetSizer(self.sizer3)
            
        self.book.AddPage(self.panel1, "Teacher")
        self.book.AddPage(self.panel2, "Venue") 
        self.book.AddPage(self.panel3, "Class")

        self.mainSizer.Add(self.book, 1, wx.EXPAND)
        self.mainPanel.SetSizer(self.mainSizer)

        pub.subscribe(self.update, 'UPDATE_VIEW') 
        # self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.update)    

        self.Maximize(True)
        self.sizer1.Layout()
        self.sizer2.Layout()
        self.sizer3.Layout()
        self.mainSizer.Layout()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()
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
        # self.SetRowMinimalAcceptableWidth(100)
        # self.SetColMinimalWidth(1,150)
        # self.EnableCellEditControl(False) 
        wx.EVT_KEY_DOWN(self, self.KeyPressed)  
        # self.EnableEditing(False)
#////////////////////////////////
        #trying to fix the white overflow (bleed) that appears on windows
        panelcolour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        self.SetDefaultCellBackgroundColour(panelcolour) 
#///////////////////////////////////
        self.InvalidateBestSize();
#        ///////////////////////////////////
        # SetClientSize(self.GetBestSize());
        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnCellDoubleClick)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.onDragSelection)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellDoubleClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.ShowPopupMenu)
        # self.ShowScrollbars(wx.SHOW_SB_DEFAULT,wx.SHOW_SB_NEVER)
        self.SetMargins(0,0)        
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
        pub.subscribe(self.Resize, 'RESIZE_CELLS') 

    def onDragSelection(self, event):
        if self.GetSelectionBlockTopLeft():
            top_left = self.GetSelectionBlockTopLeft()[0]
            bottom_right = self.GetSelectionBlockBottomRight()[0]
            globaldata.selection_left = top_left
            globaldata.selection_right = bottom_right
            print top_left
            print bottom_right

            # self.printSelectedCells(top_left, bottom_right)
 
    def getHTML(self, justStub=True, tableHeaders=True):
        ''' Get HTML suitable for printing out the data in
            this grid via wxHtmlEasyPrinting.
           
            If justStub is False, make it like a standalone
            HTML file complete with <HTML><HEAD> etc...
        '''
        cols = self.GetNumberCols()
        rows = self.GetNumberRows()
       
        # # if justStub:
        # #     html = ["<HTML><BODY>"]
        # # else:
        #     html = []

        html = []   
        footer = {}
        html.append('<h1 ALIGN="center"> %s </h1>' % globaldata.header1)
        html.append('<h2 ALIGN="center"> %s </h2>' % globaldata.header2)
        html.append('<h3 ALIGN="center"> %s </h3>' % globaldata.header3)

        hfourth = 'Timetable For ' + self.type + ':' + self.name
        if self.type == 'Class':
            try:
                hfourth += '&nbsp&nbspVenue:' + globaldata.class_venue_map[self.name]
            except:
                hfourth += ' '
        if self.type == 'Venue':
            try:
                hfourth += '&nbsp&nbspClass:' + globaldata.venue_class_map[self.name]
            except:
                hfourth += ' '
        html.append('<h3 ALIGN="center"> %s </h3>' % hfourth)
        html.append("<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0>")
       
        if tableHeaders:
            html.append("<TR>")
            html.append("<TD ALIGN='center'> </TD>")
            for col in range(cols):
                html.append("<TD ALIGN='center' VALIGN='top' WIDTH=%s><B>%s</B></TD>"
                                % (self.GetColSize(col), self.GetColLabelValue(col)))
            html.append("</TR>")
       
        for row in range(rows):
            html.append("<TR>")
            html.append("<TD ALIGN='center' VALIGN='top' WIDTH=%s><B>%s</B></TD>"
                                % (self.GetRowSize(row), self.GetRowLabelValue(row)))
            for col in range(cols):
                if self.type == 'Teacher':
                    val = self.data[row][col]
                    res = ''
                    if val == None:
                        html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % res)
                    else:
                        for e in val:
                            v = e[0]
                            c = e[1]
                            s = e[2]
                            b = e[3]
                            s += ' '
                            if b != None:
                                s +=  '- ' + str(b)  + ' '
                            s += str(c) + ' '
                            s +=  '['+ str(v) + ']'
                            res += s + '<br>'
                        html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % res)
                        t = self.name
                if self.type == 'Venue':
                    val = self.data[row][col]
                    res = ''
                    if val == None:
                        html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % res)
                    else:
                        for e in val:
                            t = e[0]
                            c = e[1]
                            s = e[2]
                            b = e[3]
                            s += ' '
                            if b != None:
                                s +=  '- ' + str(b)  + ' '
                            try:
                                if c != globaldata.venue_class_map[self.name]:
                                    s +=  '['+ str(c) + ']'
                            except:
                                s +=  '['+ str(c) + ']'

                            res += s + '<br>'
                        html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % res)

                if self.type == 'Class':
                    val = self.data[row][col]
                    res = ''
                    if val == None:
                        html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % res)
                    else:
                        for e in val:
                            t = e[0]
                            v = e[1]
                            s = e[2]
                            b = e[3]
                            s += ' '
                            if b != None:
                                s +=  '- ' + str(b)  + ' '
                            footer[s] = t
                            try:
                                if v != globaldata.class_venue_map[self.name]:
                                    s +=  '['+ str(v) + ']'
                            except:
                                s +=  '['+ str(v) + ']'
                            res += s + '<br>'
                        html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % res)
                        
            html.append("</TR>")
        html.append("</TABLE>")
        html.append("<br><br><br>")

        if self.type == 'Class':
            html.append("<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0>")
            html.append("<TR>")
            html.append("<TD ALIGN='center' VALIGN='top'><B>Subject / Batch </B></TD>")
            html.append("<TD ALIGN='center' VALIGN='top'><B>Teacher</B></TD>")
            html.append("</TR>")
            for e in footer:
                print e, footer[e]
                html.append("<TR>")
                html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % e)
                html.append("<TD ALIGN='center' VALIGN='top'>%s</TD>" % footer[e])
                html.append("</TR>")
            html.append("</TABLE>")

        return "\n".join(html) 

    # def getHTMLs(self):
    #     # docstart = "<HTML><BODY>"
    #     # docend = "</BODY></HTML>"
    #     # out = [docstart, "<TABLE BORDER CELLPADDING=0 CELLSPACING=0>"]
    #     out = ["<TABLE BORDER CELLPADDING=0 CELLSPACING=0>"]

    #     cols = self.GetNumberCols()
    #     # add headers to table
    #     _row = []
    #     _row.extend( [self.GetColLabelValue(x) for x in range(cols)] )
    #     out.append(self.addrow(_row))
                         
    #     for r in xrange(self.GetNumberRows()):
    #         _row = [self.GetRowLabelValue(r)]
    #         for c in range(cols):
    #             _row.append(self.GetCellValue(r, c))

    #         out.append(self.addrow(_row))

    #     out.append("</TABLE>")
    #     # out.append(docend)
    #     return "\n".join(out)

    # def addcell(self, s):
    #     return "<TD>%s</TD>"%s

    # def addrow(self, ls):
    #     # adds a list of strings as a row
    #     return "<TR>%s</TR>"%"\n\t".join([self.addcell(x) for x in ls])

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
        
        # If Ctrl+M is pressed...
        if event.ControlDown() and event.GetKeyCode() == 77:
            # clipboard  = self.data[self.rowSelect][self.colSelect]
            # self.ParseIntoClipboard(clipboard)
            i, j = globaldata.selection_left
            k, l = globaldata.selection_right
            self.SetCellSize(i, j, k-i+1, l-j+1);
            print 'Merge Cells',

        # If Ctrl+U is pressed...
        if event.ControlDown() and event.GetKeyCode() == 85:
            # clipboard  = self.data[self.rowSelect][self.colSelect]
            # self.ParseIntoClipboard(clipboard)
            i, j = globaldata.selection_left
            k, l = globaldata.selection_right
            self.SetCellSize(i, j, 1, 1);
            print 'UnMerge Cells'
            self.SendSizeEvent()
            self.Layout()
        
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
            i = self.rowSelect
            j = self.colSelect
            if self.GetCellSize(i, j) == (1,1):
                for i in range(len(clipboard)):
                    self.RemoveEntryFromTables(clipboard, 0)
            else:
                p, q = i, j
                x, y = self.GetCellSize(p, q)
                for l in range(x):
                    for m in range(y):
                        self.rowSelect = p+l
                        self.colSelect = q+m
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

        if self.GetCellSize(i, j) == (1,1):
            for e in globaldata.clipboard:
                if len(e) == 3:
                    try:
                        if self.type == 'Class':
                            project.insert_lunch(e[-1], i, j, self.type)
                        elif self.type == 'Teacher':
                            project.insert_lunch(e[0], i, j, self.type)  
                                                      
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

        else:
            p, q = i, j
            x, y = self.GetCellSize(p, q)
            for l in range(x):
                for m in range(y):
                    i = p+l
                    j = q+m

                    for e in globaldata.clipboard:
                        if len(e) == 3:
                            try:
                                if self.type == 'Class':
                                    project.insert_lunch(e[-1], i, j, self.type)
                                elif self.type == 'Teacher':
                                    project.insert_lunch(e[0], i, j, self.type)                                    
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
                                self.SetCellSize(p, q, 1,1)
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
                                self.SetCellSize(p, q, 1,1)
        return

    def OnLunchClick(self, i, j, evt):
        print i, j
        self.dia = wx.Dialog(self, -1, 'Enter Lunch Details', size=(300,50))
        self.dia.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dia.mainSizer.AddSpacer(10)

        if self.type == "Class":
            self.dia.label1 = wx.StaticText(self.dia, label='Enter Class:')
            # self.dia.field1 = wx.TextCtrl(self.dia, value="")
            self.dia.field1 = PromptingComboBox(self.dia, "Choose", globaldata.class_shortnames[1:], 'Class') 
        elif self.type == "Teacher":
            self.dia.label1 = wx.StaticText(self.dia, label='Enter Teacher:')
            # self.dia.field1 = wx.TextCtrl(self.dia, value="")
            self.dia.field1 = PromptingComboBox(self.dia, "Choose", globaldata.teacher_shortnames[1:], 'Teacher') 

        self.dia.field1.SetValue(self.name)
        self.dia.field1.res = self.name
        self.dia.mainSizer.Add(self.dia.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.dia.mainSizer.Add(self.dia.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)

        self.dia.okbutton = wx.Button(self.dia, label="OK", id=wx.ID_OK)
        self.dia.mainSizer.Add(self.dia.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.dia.mainSizer.AddSpacer(10)
        
        self.dia.SetSizer(self.dia.mainSizer)
        self.dia.result = None
        self.dia.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.dia.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.dia.Bind(wx.EVT_CLOSE, self.Closed)
        self.dia.ShowModal()

        if hasattr(self.dia, 'result1'):
            if self.GetCellSize(i,j) == (1,1):
                try:
                    project.insert_lunch(self.dia.result1, i, j, self.type)
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
                x, y = self.GetCellSize(i,j)
                l = i
                m = j
                for i in range(x):
                    for j in range(y):
                        p = l+i
                        q = m+j
                        try:
                            project.insert_lunch(self.dia.result1, p, q, self.type)
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
                            self.SetCellSize(l, m, 1,1)
        evt.Skip()

    def onOK(self, event):
        self.dia.result1 = self.dia.field1.res
        self.dia.Destroy()

    def onCancel(self, event):
        self.dia.Destroy()

    def Closed(self, event):
        print 'Close pressed'
        self.dia.Destroy()

    def OnDeleteEntry(self, a, b, event):
        # print 'all_teachers', globaldata.all_teachers
        # print 'all_venues', globaldata.all_venues
        # print 'all_classes', globaldata.all_classes
        entry = self.data[a][b]
        itemId = event.GetId()
        menu = event.GetEventObject()
        menuItem = menu.FindItemById(itemId)
        deleteId = int(menuItem.GetLabel().split()[2]) - 1
        if self.GetCellSize(a, b) == (1,1):
            print 'name and to delete', self.name, entry[deleteId]
            self.RemoveEntryFromTables(entry, deleteId)
        else:
            p, q = a, b
            x, y = self.GetCellSize(p, q)
            for l in range(x):
                for m in range(y):
                    self.rowSelect = p+l
                    self.colSelect = q+m
                    print 'name and to delete', self.name, entry[deleteId]
                    self.RemoveEntryFromTables(entry, deleteId)

    def RemoveEntryFromTables(self, entry, deleteId):
        print entry
        print deleteId
        entryLength = len(entry[deleteId]) 
        #if has no attribute that means you haven't selected the cell yet
        a = self.rowSelect
        b = self.colSelect

        if entryLength < 3:
            if entry[deleteId][1] == None:
                project.remove_lunch(self.name, a, b, self.type)
            else:
                project.remove_lunch(self.name+'-'+entry[deleteId][-1] , a, b, self.type)

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

        self.rowSelect = i
        self.colSelect = j

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
        if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3') and hasattr(dlg, 'result4'):
            if self.GetCellSize(evt.GetRow(), evt.GetCol()) == (1,1):
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
            else:
                x, y = self.GetCellSize(evt.GetRow(), evt.GetCol())
                l = evt.GetRow()
                m = evt.GetCol()
                for i in range(x):
                    for j in range(y):
                        p = l+i
                        q = m+j
                        try:
                            project.insert_entry(dlg.result1, dlg.result2, dlg.result3, dlg.result4, p, q)
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
                            self.SetCellSize(l, m, 1,1)
        evt.Skip()

    def Resize(self, evt):
        # self.AutoSizeColumns()
        # self.AutoSizeRows()
        self.AutoSize()
        # evt.Skip()
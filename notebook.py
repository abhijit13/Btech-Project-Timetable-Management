import wx
class TabPanel(wx.Panel):    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.Panel(Employee.EmployeeViewAllFrame(self).show())

        self.sizer.Add(txtOne, 0, wx.ALL , 50)

        self.SetSizer(self.sizer)


class NotebookDemo(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                         wx.BK_DEFAULT
                         #wx.BK_TOP 
                         #wx.BK_BOTTOM
                         #wx.BK_LEFT
                         #wx.BK_RIGHT
                         )

        # Create the first tab and add it to the notebook
        tabOne = TabPanel(self)
        tabOne.SetBackgroundColour("BLUE")
        self.AddPage(tabOne, "Main")

        # Create and add the second tab
        tabTwo = TabPanel(self)
        self.AddPage(tabTwo, "Employees")

        # Create and add the third tab
        self.AddPage(TabPanel(self), "Tasks")
a = NotebookDemo(0)
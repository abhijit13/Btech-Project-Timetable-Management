import wx
import wx.grid as gridlib
from wx.lib.pubsub import Publisher as pub
import project
import globaldata

class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = globaldata.rowLabels
        self.colLabels = globaldata.colLabels
        
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

#m_controller
import wx
import wx.grid
import os
import view
import model
import threading
import sys


class HugeTableGrid(wx.grid.Grid):
    def __init__(self, parent, title, data, rows, cols):
        wx.grid.Grid.__init__(self, parent, -1)
        
        table = model.HugeTable(title, data, rows, cols)
        
        self.SetTable(table, True)
        
        
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightDown)
    '''
    def SetReadOnly(self, *args, **kwargs):
        return True
    '''
    
        
        
    
    def OnRightDown(self, e):
        print 'hello'

class Controller:
    def __init__(self, app):
        self.m_view = view.View(None)
        self.m_model = model.Model()
        
        #grid parameter
        self.grid_max_colume_number = 0
        self.grid_max_row_number = 8192
        
        #event bind
        self.m_view.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirSelected, self.m_view.m_dirpicker)
        #treectrl
        self.m_view.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.m_view.m_treectrl)


        self.m_view.Show()
        
    def OnDirSelected(self, evt):
        tree = self.m_view.m_treectrl
        tree.DeleteAllItems()
        root = tree.AddRoot(self.m_view.m_dirpicker.GetPath())
        tree.SetItemImage(root, tree.fldridx, wx.TreeItemIcon_Normal)
        tree.SetItemImage(root, tree.fldropenidx, wx.TreeItemIcon_Expanded)
        tree.SetItemHasChildren(root, True)    
        pass
    
    def OnItemCollapsed(self, evt):
        pass
    
    def OnItemActivated(self, evt):
        tree = self.m_view.m_treectrl
        itemName = self.m_view.m_treectrl.GetItemText(evt.GetItem())
        itemPath = self.mGetPathOnItem(evt.GetItem())
        if os.path.isdir(itemPath):
            pass
        else:
            _sql = model.Sqlite()
            if _sql.is_sqlite_file(itemPath):
                parse = model.LogParse()
                projName = parse.find_current_project(itemPath)
                self.m_view.m_statusBar.SetStatusText(projName)
                
                _model = model.Model()
                data = _model.SetDataToGrid(itemPath, self.grid_max_row_number)
                self.mAddGridPage(projName, data[0], data, self.grid_max_row_number, len(data[0]))
        pass
    
    def OnItemExpanded(self, evt):
        pass
    
    def OnItemExpanding(self, evt):
        item = evt.GetItem()
        tree = self.m_view.m_treectrl
        path = self.mGetPathOnItem(item)
        
        if os.path.isdir(path):
            for dirPath, dirNames, fileNames in os.walk(path):
                for dirName in dirNames:
                    newNode = tree.AppendItem(item, dirName)
                    tree.SetItemImage(newNode, tree.fldridx, wx.TreeItemIcon_Normal)
                    tree.SetItemImage(newNode, tree.fldropenidx, wx.TreeItemIcon_Expanded)
                    tree.SetItemHasChildren(newNode, True)
                
                for fileName in fileNames:
                    newItem = tree.AppendItem(item, fileName)
                    tree.SetItemImage(newItem, tree.fileidx, wx.TreeItemIcon_Normal)
                break
        else:
            pass
        pass
    
    
    
    #@staticmethod
    def mGetPathOnItem(self, item):
        tree = self.m_view.m_treectrl
        currentPath = tree.GetItemText(item)
        traceItem = item
        if item == tree.GetRootItem():
            pass
        else:
            while traceItem != tree.GetRootItem():
                currentPath = os.path.join(tree.GetItemText(tree.GetItemParent(traceItem)), currentPath)
                traceItem = tree.GetItemParent(traceItem)
        return currentPath
                
    
    '''arg , page_name, col_title, data, row_szie, col_size'''
    def mAddGridPage(self, page_name, col_title, data, row_size, col_size):
        mParent = self.m_view.m_auimanager
        mPanel = wx.Panel(mParent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Panel_Sizer = wx.BoxSizer(wx.VERTICAL)
        
       
        
        mGrid = HugeTableGrid(mPanel, col_title, data, row_size, col_size)
       
                
        
        '''
        mGrid = wx.grid.Grid(mPanel)
        mGrid.CreateGrid(row_size, col_size)
        
        for i in range(0, len(col_title)):
            mGrid.SetColLabelValue(i, col_title[i])
        
        
        #data 0~1024 1025
        for row in range(0, row_size): #0~1023
            for col in range(0, len(data[row+1])):
                mGrid.SetCellValue(row, col, "%s"%data[row+1][col])
                #mGrid.SetReadOnly(row, col, True)
                pass
            mGrid.AutoSizeColumn(col, True)
            pass
        #'''
        Panel_Sizer.Add( mGrid, 1, wx.ALL|wx.EXPAND, 5 )
        mPanel.SetSizer(Panel_Sizer)
        mPanel.Layout()
        self.m_view.m_auimanager.AddPage(mPanel, page_name, False)
        pass
    
    
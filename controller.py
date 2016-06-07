#m_controller
import wx
import wx.grid
import wx.aui
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
        
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightDown)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelDClick)
        
    def OnCellRightDown(self, e):
        print 'hello'
    
    def OnLabelDClick(self, evt):
        col = evt.GetCol()
        col_size = self.GetColSize(col)
        #self.AutoSizeColumn(col, True)
        #'''
        if col_size == 80:
            self.AutoSizeColumn(col, True)
        else:   
            self.SetColSize(col, 80)
        #'''
        pass

class Controller:
    def __init__(self, app):
        self.m_view = view.View(None)
        self.m_model = model.Model()
        
        self.show_current_file = None
        self.current_select_page = None
        self.current_select_project_name = None
        self.current_select_file_name = None
        self.current_select_file_path = None
        self.current_select_file_daytime = None
        
        #grid parameter
        self.grid_max_colume_number = 0
        self.grid_max_preview_row_number = 1024
        
        #event bind
        #auimanager
        self.m_view.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnANBPageChanged, self.m_view.m_auimanager)
        
        
        #treectrl
        self.m_view.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirSelected, self.m_view.m_dirpicker)
        self.m_view.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated, self.m_view.m_treectrl)
        self.m_view.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.m_view.m_treectrl)
        
        
        #notebook_panel_01
        self.hl_hr = 0
        self.hl_mm = 0
        self.ll_hr = 0
        self.ll_mm = 0
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPHLchoice, self.m_view.m_np1_choice_03)
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPHLchoice, self.m_view.m_np1_choice_04)
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPLLchoice, self.m_view.m_np1_choice_01)
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPLLchoice, self.m_view.m_np1_choice_02)
        
        self.m_view.Bind(wx.EVT_CHECKBOX, self.OnNPcheckBox, self.m_view.m_np1_checkBox_01)
        self.m_view.Bind(wx.EVT_BUTTON, self.OnNPbutton, self.m_view.m_np1_button_01)

        self.m_view.Show()
      
    
    #evt aui notebook
    def OnANBPageChanged(self, evt):
        pageID = evt.GetSelection()
        pageName = self.m_view.m_auimanager.GetPageText(pageID)
        
        self.current_select_page = pageName
        self.m_view.m_statusBar.SetStatusText(self.current_select_page, 1)
        
        #print pageName, pageID
        pass
    
    #evt dir picker
    def OnDirSelected(self, evt):
        tree = self.m_view.m_treectrl
        tree.DeleteAllItems()
        root = tree.AddRoot(self.m_view.m_dirpicker.GetPath())
        tree.SetItemImage(root, tree.fldridx, wx.TreeItemIcon_Normal)
        tree.SetItemImage(root, tree.fldropenidx, wx.TreeItemIcon_Expanded)
        tree.SetItemHasChildren(root, True)    
        pass
    
    def OnSelChanged(self, evt):
        itemPath = self.mGetPathOnItem(evt.GetItem())
        itemName = self.m_view.m_treectrl.GetItemText(evt.GetItem())
        
        _sql = model.Sqlite()
        if _sql.is_sqlite_file(itemPath):
            self.current_select_file_path = itemPath
            parse = model.LogParse()
            self.current_select_project_name = parse.find_current_project(itemPath)
            self.current_select_file_name = itemName
            self.current_select_file_path = itemPath
            self.show_current_file = '%s: %s'%(self.current_select_project_name, itemName)
            self.m_view.m_statusBar.SetStatusText(self.show_current_file, 0)
            _parse = model.LogParse()
            self.current_select_file_daytime = _parse.find_current_project_daytime(itemPath)
        else:
            pass  
        pass
    
    def OnItemCollapsed(self, evt):
        item = evt.GetItem()
        self.m_view.m_treectrl.DeleteChildren(item)
        pass
    
    def OnItemActivated(self, evt):
        tree = self.m_view.m_treectrl
        itemName = self.m_view.m_treectrl.GetItemText(evt.GetItem())
        itemPath = self.mGetPathOnItem(evt.GetItem())
        
        
        self.current_select_file_path = itemPath
        self.current_select_file_name = itemName
        
        if os.path.isdir(itemPath):
            pass
        else:
            _sql = model.Sqlite()
            if _sql.is_sqlite_file(itemPath):
                parse = model.LogParse()
                projName = parse.find_current_project(itemPath)
                self.current_select_project_name = projName
                self.show_current_file = '%s: %s'%(projName, itemName)
                page_name = '%s: %s [preview]'%(projName, itemName)
                self.m_view.m_statusBar.SetStatusText(self.show_current_file, 0)
                
                data = self.m_model.GetDataOnItemActivated(itemPath, self.grid_max_preview_row_number)
                if len(data) >=1:
                    self.mAddGridPage(page_name, data[0], data, len(data), len(data[0]))
                else:
                    pass
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
    #evt notebook panel 01
    
    def OnNPHLchoice(self, evt):
        self.hl_hr = int(self.m_view.m_np1_choice_03.GetStringSelection().split(' ')[0])
        self.hl_mm = int(self.m_view.m_np1_choice_04.GetStringSelection().split(' ')[0])
        
        pass
    def OnNPLLchoice(self, evt):
        self.ll_hr = int(self.m_view.m_np1_choice_01.GetStringSelection().split(' ')[0])
        self.ll_mm = int(self.m_view.m_np1_choice_02.GetStringSelection().split(' ')[0])
        
        pass
    
    def OnNPbutton(self, evt):
        if not self.current_select_file_path:
            pass
        else:
            string_split = self.current_select_file_daytime.split('-')
            yy = int(string_split[0])
            MM = int(string_split[1])
            dd = int(string_split[2])
            
            parse = model.LogParse()
            ts_hl = parse.unixtime_covert(yy, MM, dd, self.hl_hr, self.hl_mm, 00)
            ts_ll = parse.unixtime_covert(yy, MM, dd, self.ll_hr, self.ll_mm, 00)
        
            if ts_hl >= ts_ll:
                data = self.m_model.GetTimeRangeData(self.current_select_file_path, ts_hl, ts_ll)
                if data == None:
                    pass
                else:
                    page_name = "%s: %s [%s:%s ~ %s:%s]"%(self.current_select_project_name, 
                                                          self.current_select_file_name,
                                                          self.ll_hr, self.ll_mm,
                                                          self.hl_hr, self.hl_mm)
                    self.mAddGridPage(page_name, data[0], data, len(data), len(data[0]))
            else:
                pass
        pass
    
    
    def OnNPcheckBox(self, evt):
        if evt.IsChecked():
            self.m_view.m_np1_staticText_01.Enable()
            self.m_view.m_np1_choice_03.Enable()
            self.m_view.m_np1_choice_04.Enable()
            pass
        else:
            self.m_view.m_np1_staticText_01.Disable()
            self.m_view.m_np1_choice_03.Disable()
            self.m_view.m_np1_choice_04.Disable()
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
    
    
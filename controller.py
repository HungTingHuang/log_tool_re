#m_controller
import wx
import wx.grid
import wx.aui
#import wx.lib.agw.aui as wx_aui
import os
import view
import model
import threading
import sys
import time
from wx import SpinButton
from model import Model
from view import View
import openpyxl
import openpyxl.styles as xl_sty
from openpyxl.styles import Font, Color
from openpyxl.styles import colors
from collections import OrderedDict
from bsddb.dbtables import LikeCond

class GridDataPage(wx.Panel):
    def __init__(self, parent, page_name, filename, cmd, grid_row_limit, args, args_index):
         
        ##Panel Setting
        self.mPage = wx.Panel(parent, 
                         wx.ID_ANY, 
                         wx.DefaultPosition, 
                         wx.DefaultSize, 
                         wx.TAB_TRAVERSAL)
        
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer = wx.BoxSizer(wx.VERTICAL)
        spinnerSizer = wx.BoxSizer(wx.HORIZONTAL)
        exportSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add( statusSizer, 0, wx.EXPAND, 5 )
        pageSizer.Add( gridSizer, 0, wx.EXPAND, 5 )
        statusSizer.Add(spinnerSizer, 1, wx.EXPAND, 5)
        statusSizer.Add(exportSizer, 0, 0, 5)
        
        
        self.m_model = Model()
        
        self.m_progress = args
        self.parse = model.LogParse(filename)
        
        self.mPage.cmd = cmd
        self.mPage.page_name = page_name
        #mPage.m_id = 
        #init data preview
        self.mPage.filename = filename
        self.mPage.m_data_offset = 0
        self.mPage.m_data_row_limit = grid_row_limit
        
        self.mPage.m_data = self.m_model.GetRowRangeData(self.mPage.filename,
                                                         self.mPage.cmd,
                                                         self.mPage.m_data_row_limit, 
                                                         self.mPage.m_data_offset)
        
        self.mPage.m_data_len = self.parse.find_total_row_number(self.mPage.filename, self.mPage.cmd)
        self.mPage.m_grid_title = self.mPage.m_data[0]
        self.mPage.m_grid_title_len = len(self.mPage.m_data[0])
        #self.mPage.m_data = self.mPage.m_data[1]
        
        self.mPage.m_current_page_number = 1
        self.mPage.m_max_page_number = 0
        
        if self.mPage.m_data_len > self.mPage.m_data_row_limit:
            self.mPage.m_max_page_number = self.mPage.m_data_len//self.mPage.m_data_row_limit
            if not self.mPage.m_data_len/self.mPage.m_data_row_limit == 0:
                self.mPage.m_max_page_number += 1
            else:
                pass
        else:
            pass 
        
        self.mPage.m_min_page_number = 1
        
        self.spinText = wx.TextCtrl(self.mPage,
                                    wx.ID_ANY,
                                    wx.EmptyString,
                                    wx.DefaultPosition,
                                    wx.DefaultSize,
                                    wx.TE_READONLY)
        
        self.spinText.SetValue(str(self.mPage.m_current_page_number))
        
        self.spinButton = wx.SpinButton(self.mPage, 
                                        wx.ID_ANY,
                                        wx.DefaultPosition, 
                                        wx.DefaultSize,
                                        wx.SP_WRAP)
        '''
        spinCtrl = wx.SpinCtrl(mPage, 
                                 wx.ID_ANY, wx.EmptyString, 
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 wx.SP_WRAP, 
                                 1, mPage.m_data_len, 1)
        '''
        
        self.staticText = wx.StaticText( self.mPage, 
                                         wx.ID_ANY, 
                                         u"Total Rows: " + str(self.mPage.m_data_len), 
                                         wx.DefaultPosition, 
                                         wx.DefaultSize, 0 )
        
        exportButton = wx.Button( self.mPage, 
                                  wx.ID_ANY, 
                                  u"EXPORT", 
                                  wx.DefaultPosition, 
                                  wx.DefaultSize, 0 )
        
        
        spinnerSizer.Add(self.spinText, 0, wx.EXPAND, 5)
        spinnerSizer.Add(self.spinButton, 0, wx.EXPAND, 5)
        spinnerSizer.Add(self.staticText, 0, wx.ALL, 5)
        exportSizer.Add(exportButton, 0, wx.ALIGN_RIGHT, 5)
        
        #row_size = len(data)
        #col_size = len(data[0])
        self.mGrid = HugeTableGrid(self.mPage, 
                                   self.mPage.m_data[0], 
                                   self.mPage.m_data,
                                   len(self.mPage.m_data), 
                                   len(self.mPage.m_data[0]))
        
        gridSizer.Add( self.mGrid, 1, wx.EXPAND, 5 )
        self.mPage.SetSizer(pageSizer)
        self.mPage.Layout()
        parent.AddPage(self.mPage, page_name, False)     
        
        
        parent.Bind(wx.EVT_SPIN_UP, self.OnSpinUp, self.spinButton)
        parent.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown, self.spinButton)
        parent.Bind(wx.EVT_BUTTON, self.OnExportExcel, exportButton)
        pass
            
    
    #callback export excel
    def OnExportExcel(self, evt):
        
        projectName = self.mPage.page_name.partition('.d')[0] 
        #exportFileName = projectName.replace(': ', '_') + '.xlsx'
        exportFileName = projectName.replace(': ', '_') + '.csv'
        #excel_rows_max_limit = 8192
        #excel_offset = 0
        #sheet_count = 0
        #progress_value = 10
        #progress_value_offset = 0
        #sheet_index = 0
        
        #start_row = 0
        #start_col = 0
        #self.m_progress.SetValue(int(10))
        
        doc = open(exportFileName, 'w')
        
        data_total_rows = self.parse.find_total_row_number(self.mPage.filename, 
                                                           self.mPage.cmd)
        
        
        #self.m_progress.SetValue(int(20))
        data = self.m_model.GetRowRangeData(self.mPage.filename,
                                                self.mPage.cmd,
                                                data_total_rows, 
                                                0)
        #self.m_progress.SetValue(int(70))
        
        for row in data:
            for value in row:
                doc.write(str(value))
                doc.write(str(','))
            doc.write(str('\n'))
        
        #self.m_progress.SetValue(int(90))
        doc.close()
        
        
        
        '''
        data_total_rows = self.parse.find_total_row_number(self.mPage.filename, 
                                                           self.mPage.cmd)
        
        if data_total_rows >= excel_rows_max_limit:
            sheet_count = data_total_rows/excel_rows_max_limit
            if not data_total_rows % excel_rows_max_limit == 0:
                sheet_count+=1
            else:
                pass
        else:
            sheet_count = 1
            pass
        progress_value_offset = 80/sheet_count
        
        doc = openpyxl.Workbook()
        sht_active = doc.active
        for sht_index in range(sheet_count):
            sht_active.title = str(sht_index)
            
            data = self.m_model.GetRowRangeData(self.mPage.filename,
                                                self.mPage.cmd,
                                                excel_rows_max_limit, 
                                                excel_offset)
            
            for row_index, row_data in enumerate(data):
                
                for col_index, value_t in enumerate(row_data):
                    sht_active.cell(column = start_col + col_index + 1,
                                    row= start_row + row_index + 1,
                                    value = value_t)
            excel_offset += excel_rows_max_limit
            sht_active = doc.create_sheet()
            progress_value += progress_value_offset
            self.m_progress.SetValue(progress_value)
        
        doc.save(exportFileName)
        '''
       
        #self.m_progress.SetValue(int(100))
        pass
    
    def OnSpinUp(self, evt):
        
        row_limit = self.mPage.m_data_row_limit
        if self.mPage.m_current_page_number <= self.mPage.m_max_page_number and self.mPage.m_current_page_number >= self.mPage.m_min_page_number:
            if self.mPage.m_current_page_number == self.mPage.m_max_page_number:
                self.mPage.m_current_page_number = self.mPage.m_min_page_number
            else:
                self.mPage.m_current_page_number += 1
                #self.mPage.m_data_offset += self.mPage.m_data_row_limit
        else:
            pass
        self.mPage.m_data_offset = (self.mPage.m_current_page_number-1)*self.mPage.m_data_row_limit
        
        if self.mPage.m_current_page_number == self.mPage.m_max_page_number:
            row_limit = (self.mPage.m_current_page_number * self.mPage.m_data_row_limit) - self.mPage.m_data_len
            
        else:
            pass
        
        self.mPage.m_data = self.m_model.GetRowRangeData(self.mPage.filename,
                                                         self.mPage.cmd, 
                                                         row_limit, 
                                                         self.mPage.m_data_offset)
        self.spinText.SetValue(str(self.mPage.m_current_page_number))
        
        self.mGrid.OnUpdate(self.mPage.m_data[0], 
                           self.mPage.m_data, 
                           len(self.mPage.m_data), 
                           len(self.mPage.m_data[0]))
        
        pass
    
    def OnSpinDown(self, evt):
        row_limit = self.mPage.m_data_row_limit
        if self.mPage.m_current_page_number <= self.mPage.m_max_page_number and self.mPage.m_current_page_number >= self.mPage.m_min_page_number:
            if self.mPage.m_current_page_number == self.mPage.m_min_page_number:
                self.mPage.m_current_page_number = self.mPage.m_max_page_number
                
            else:
                self.mPage.m_current_page_number -= 1
        else:
            pass
        
        self.mPage.m_data_offset = (self.mPage.m_current_page_number-1)*self.mPage.m_data_row_limit
        
        if self.mPage.m_current_page_number == self.mPage.m_max_page_number:
            row_limit = (self.mPage.m_current_page_number * self.mPage.m_data_row_limit) - self.mPage.m_data_len
            
        else:
            pass
        
        self.mPage.m_data = self.m_model.GetRowRangeData(self.mPage.filename,
                                                         self.mPage.cmd, 
                                                         row_limit, 
                                                         self.mPage.m_data_offset)
        
        self.spinText.SetValue(str(self.mPage.m_current_page_number))
        self.mGrid.OnUpdate(self.mPage.m_data[0], 
                            self.mPage.m_data,
                            len(self.mPage.m_data), 
                            len(self.mPage.m_data[0]))
        
        
        
        
        
        pass

class HugeTableGrid(wx.grid.Grid):
    def __init__(self, parent, title, data, rows, cols):
        wx.grid.Grid.__init__(self, parent, -1)
        
        
        self.table = model.HugeTable(title, data, rows, cols)
        self.SetTable(self.table, True)
        
        self.cols = self.GetNumberCols() 
        self.rows = self.GetNumberRows()
        
        
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightDown)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelDClick)
    '''
    def Update(self, *args, **kwargs):
        return wx.grid.Grid.Update(self, *args, **kwargs)
    '''
    def OnUpdate(self, title, data, rows, cols):
        self.table.Clear()
        self.table = model.HugeTable(title, data, rows, cols)
        self.SetTable(self.table, True)
        
        
        #self.table.UpdateData(title, data, rows, cols)     
        '''
        if rows != self.rows:
            if rows < self.rows:
                #cc = 
                self.table.DeleteRows(rows, (self.rows - rows))
                
            elif rows > self.rows:
                self.table.AppendRows(self.rows, rows)
            else:
                pass
        else:
            pass
        ''' 
        
        self.Refresh()
        
    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            self.copy()
        # If Ctrl+V is pressed...
        if event.ControlDown() and event.GetKeyCode() == 86:
            self.paste('clip')
        # If Ctrl+Z is pressed...
        if event.ControlDown() and event.GetKeyCode() == 90:
            if self.data4undo[2] != '':
                self.paste('undo')
        # If del is pressed...
        if event.GetKeyCode() == 127:
            # Call delete method
            self.delete()
        # Skip other Key events
        if event.GetKeyCode():
            event.Skip()
            return
    def copy(self):
        # Number of rows and cols
        #print self.GetSelectionBlockBottomRight()
        #print self.GetGridCursorRow()
        #print self.GetGridCursorCol()
        if self.GetSelectionBlockTopLeft() == []:
            rows = 1
            cols = 1
            iscell = True
        else:
            rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
            cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
            iscell = False
        # data variable contain text that must be set in the clipboard
        data = ''
        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                if iscell:
                    data += str(self.GetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c))
                else:
                    data += str(self.GetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c))
                if c < cols - 1:
                    data += '\t'
            data += '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")

    def paste(self, stage):
        if stage == 'clip':
            clipboard = wx.TextDataObject()
            if wx.TheClipboard.Open():
                wx.TheClipboard.GetData(clipboard)
                wx.TheClipboard.Close()
            else:
                wx.MessageBox("Can't open the clipboard", "Error")
            data = clipboard.GetText()
            if self.GetSelectionBlockTopLeft() == []:
                rowstart = self.GetGridCursorRow()
                colstart = self.GetGridCursorCol()
            else:
                rowstart = self.GetSelectionBlockTopLeft()[0][0]
                colstart = self.GetSelectionBlockTopLeft()[0][1]
        elif stage == 'undo':
            data = self.data4undo[2]
            rowstart = self.data4undo[0]
            colstart = self.data4undo[1]
        else:
            wx.MessageBox("Paste method "+stage+" does not exist", "Error")
        text4undo = ''
        # Convert text in a array of lines
        for y, r in enumerate(data.splitlines()):
            # Convert c in a array of text separated by tab
            for x, c in enumerate(r.split('\t')):
                if y + rowstart < self.NumberRows and x + colstart < self.NumberCols :
                    text4undo += str(self.GetCellValue(rowstart + y, colstart + x)) + '\t'
                    self.SetCellValue(rowstart + y, colstart + x, c)
            text4undo = text4undo[:-1] + '\n'
        if stage == 'clip':
            self.data4undo = [rowstart, colstart, text4undo]
        else:
            self.data4undo = [0, 0, '']

    def delete(self):
        # print "Delete method"
        # Number of rows and cols
        if self.GetSelectionBlockTopLeft() == []:
            rows = 1
            cols = 1
        else:
            rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
            cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
        # Clear cells contents
        for r in range(rows):
            for c in range(cols):
                if self.GetSelectionBlockTopLeft() == []:
                    self.SetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c, '')
                else:
                    self.SetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c, '')

    
    def OnCellRightDown(self, e):
        print 'hello'
    
    def OnLabelDClick(self, evt):
        col = evt.GetCol()
        if not col >= 0:
            return
        col_size = self.GetColSize(col)
        #self.AutoSizeColumn(col, True)
        #'''
        if col_size == 80:
            self.AutoSizeColumn(col, True)
        else:   
            self.SetColSize(col, 80)
        #'''
        pass

'''
class HugeAuiNoteBook(wx.Panel):
    def __init__(self, parent, ID_ANY, DefaultPosition, DefaultSize, 0, AUI_NB_DEFAULT_STYLE, "AuiNotebook"):
        wx.Panel(self, parent, ID_ANY, DefaultPosition, DefaultSize, 0, AUI_NB_DEFAULT_STYLE, "AuiNotebook")
        pass
    pass
'''
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
        
        #self.lock = threading.Lock()
        
        self.cmd = 'SELECT * FROM log_raw'
        #grid parameter
        self.grid_max_colume_number = 0
        self.grid_max_row_number = 8192
        
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
        #ctrl panel_01 1f
        self.src_fifter = ''
        self.state_fifter = ''
        self.level_fifter = ''
        self.m_view.Bind(wx.EVT_TEXT, self.OntcSrcChanged, self.m_view.m_np1_1f_tc_src)
        self.m_view.Bind(wx.EVT_TEXT, self.OntcStateChanged, self.m_view.m_np1_1f_tc_state)
        self.m_view.Bind(wx.EVT_TEXT, self.OnLevelSrcChanged, self.m_view.m_np1_1f_tc_level)
        #ctrl panel_01 2f
        self.hl_hr = 0
        self.hl_mm = 0
        self.ll_hr = 0
        self.ll_mm = 0
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPHLchoice, self.m_view.m_np1_choice_03)
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPHLchoice, self.m_view.m_np1_choice_04)
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPLLchoice, self.m_view.m_np1_choice_01)
        self.m_view.Bind(wx.EVT_CHOICE, self.OnNPLLchoice, self.m_view.m_np1_choice_02)
        
        self.m_view.Bind(wx.EVT_CHECKBOX, self.OnNPcheckBox, self.m_view.m_np1_checkBox_01)
        #self.m_view.Bind(wx.EVT_BUTTON, self.OnNPbutton, self.m_view.m_np1_button_01)
        #ctrl panel_01 3f
        self.m_view.m_np1_3f_tc_cmd.SetValue(self.cmd)
        self.like_fifter = ''
        self.m_view.Bind(wx.EVT_TEXT, self.OntcLIKEChanged, self.m_view.m_np1_3f_tc_like)
        
        self.m_view.Bind(wx.EVT_CHECKBOX, self.OncbCMDOnlyReady, self.m_view.m_np1_3f_cb_cmd)
        self.m_view.Bind(wx.EVT_TEXT, self.OntcCMDChanged, self.m_view.m_np1_3f_tc_cmd)
        
        self.m_view.Bind(wx.EVT_BUTTON, self.OnbtnReset, self.m_view.m_np1_3f_btn_reset)
        self.m_view.Bind(wx.EVT_BUTTON, self.OnbtnQuery, self.m_view.m_np1_3f_btn_query)
        
        #self.m_view.Bind(wx.EVT_TEXT, self.OntcCMDChanged, self.m_view.m_np1_3f_tc_cmd)
        
        self.m_view.Show()
      
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
            parse = model.LogParse(itemPath)
            self.current_select_project_name = parse.find_current_project(itemPath)
            self.current_select_file_name = itemName
            self.current_select_file_path = itemPath
            self.show_current_file = '%s: %s'%(self.current_select_project_name, itemName)
            self.m_view.m_statusBar.SetStatusText(self.show_current_file, 0)
            log = model.LogParse(itemPath)
            self.current_select_file_daytime = log.find_current_project_daytime(itemPath)
        else:
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
                log = model.LogParse(itemPath)
                projName = log.curProj
                self.current_select_project_name = projName
                self.show_current_file = '%s: %s'%(projName, itemName)
                page_name = '%s: %s [preview]'%(projName, itemName)
                self.m_view.m_statusBar.SetStatusText(self.show_current_file, 0)
                
                
                GridDataPage(self.m_view.m_auimanager, 
                             page_name, 
                             itemPath,
                             self.m_model.GetFullDataCmd(itemPath),
                             self.grid_max_row_number,
                             self.m_view.m_progress,
                             0)
                
                
                '''
                data_len = parse.find_total_row_number(itemPath)
                row_limit = self.grid_max_row_number
                page_number = 1
                
                
                if data_len > row_limit:
                    page_number = data_len/row_limit
                    if not data_len%row_limit == 0:
                        page_number += 1
                    else:
                        pass
                else:
                    pass 
                
                
                offset = 0
                for num in range(0, page_number):
                    page_name_text =  page_name + '_#' + str(num)
                    data = self.m_model.GetRowRangeData(itemPath, row_limit, offset)
                    offset += (row_limit+1)
                    
                    if data and len(data) >1:
                        self.mAddMultiGridPage(page_name, data[0], data)
                        #self.mAddGridPage(page_name_text, data[0], data)
                    else:
                        pass
                pass
                '''
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

    
    
    
    def OntcSrcChanged(self, evt):
        
        text = evt.GetString()
        self.src_fifter = ''
        if text:
            for value in text.split(','):
                if not value == '' :
                    self.src_fifter += 'src=%s'%value
                    self.src_fifter += ' OR '
                else:
                    pass
            self.src_fifter = self.src_fifter[:-4]
        
        self.OntcCMDUpdate()
        
        pass
    def OntcStateChanged(self, evt):
        
        text = evt.GetString()
        self.state_fifter = ''
        if text:
            for value in text.split(','):
                if not value == '' :
                    self.state_fifter += 'state=%s'%value
                    self.state_fifter += ' OR '
                else:
                    pass
            self.state_fifter = self.state_fifter[:-4]
        
        self.OntcCMDUpdate()
        pass
    def OnLevelSrcChanged(self, evt):
        
        text = evt.GetString()
        self.level_fifter = ''
        if text:
            for value in text.split(','):
                if not value == '' :
                    self.level_fifter += 'level=%s'%value
                    self.level_fifter += ' OR '
                else:
                    pass
            self.level_fifter = self.level_fifter[:-4]
        
        self.OntcCMDUpdate()
        pass
    
    def OntcLIKEChanged(self, evt):
        text = evt.GetString()
        self.like_fifter = ''
        if text:
            for value in text.split(','):
                if not value == '' :
                    self.like_fifter += "msg LIKE '%%%s%%'"%value
                    self.like_fifter += ' OR '
                else:
                    pass
            self.like_fifter = self.like_fifter[:-4]
        
        self.OntcCMDUpdate()
        
        pass
    
    def OncbCMDOnlyReady(self, evt):
        #if evt.getValue()
        if evt.IsChecked():
            self.m_view.m_np1_1f_tc_src.SetEditable(False)
            self.m_view.m_np1_1f_tc_state.SetEditable(False)
            self.m_view.m_np1_1f_tc_level.SetEditable(False)
            self.m_view.m_np1_3f_tc_like.SetEditable(False)
            
            self.m_view.m_np1_3f_tc_cmd.SetEditable(True)
        else:
            
            self.m_view.m_np1_1f_tc_src.SetEditable(True)
            self.m_view.m_np1_1f_tc_state.SetEditable(True)
            self.m_view.m_np1_1f_tc_level.SetEditable(True)
            self.m_view.m_np1_3f_tc_like.SetEditable(True)
            
            self.m_view.m_np1_3f_tc_cmd.SetEditable(False)
        
        pass
    def OntcCMDUpdate(self):
        text = self.m_view.m_np1_3f_tc_cmd.GetValue()
        
        src = self.src_fifter
        state = self.state_fifter
        lev = self.level_fifter
        
        like = self.like_fifter
        
        _list =[src, state, lev ] 
        
        base = text.partition(' WHERE ')[0]
        
        
        fifter = ''
        for value in _list:
            if not value =='':
                if not fifter =='':
                    fifter += ' AND '
                fifter += value
        
        
        
        
        
        if like:
            if src or state or lev:
                base = base + ' WHERE ' + '(' + fifter + ')' + ' AND ' + '(' + like + ')'
            else:
                base = base + ' WHERE ' + like
        else:
            if src or state or lev:
                base = base + ' WHERE ' + fifter
            else:
                pass
            
        
        self.m_view.m_np1_3f_tc_cmd.SetValue(base)
        
        pass
    def OntcCMDChanged(self, evt):
        
        text = evt.GetString()
        self.cmd = text
        pass
    
    def OnbtnReset(self, evt):
        self.cmd = 'SELECT * FROM log_raw'
        
        self.src_fifter = ''
        self.state_fifter = ''
        self.level_fifter = ''
        self.m_view.m_np1_1f_tc_src.SetValue('')
        self.m_view.m_np1_1f_tc_state.SetValue('')
        self.m_view.m_np1_1f_tc_level.SetValue('')
        self.m_view.m_np1_1f_tc_src.SetEditable(True)
        self.m_view.m_np1_1f_tc_state.SetEditable(True)
        self.m_view.m_np1_1f_tc_level.SetEditable(True)
        
        self.like_fifter = ''
        self.m_view.m_np1_3f_tc_like.SetValue('')
        self.m_view.m_np1_3f_cb_cmd.SetValue(False)
        self.m_view.m_np1_3f_tc_cmd.SetEditable(False)
        self.m_view.m_np1_3f_tc_cmd.SetValue(self.cmd)
        
        pass
    def OnbtnQuery(self, evt):
        if not self.current_select_file_path:
            pass
        else:
            page_name = "%s: %s"%(self.current_select_project_name, 
                                  self.current_select_file_name)
            GridDataPage(self.m_view.m_auimanager, 
                             page_name, 
                             self.current_select_file_path, 
                             self.cmd, 
                             self.grid_max_row_number,
                             0,
                             0)
        pass
        
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
            
            parse = model.LogParse(self.current_select_file_path)
            ts_hl = parse.unixtime_covert(yy, MM, dd, self.hl_hr, self.hl_mm, 00)
            ts_ll = parse.unixtime_covert(yy, MM, dd, self.ll_hr, self.ll_mm, 00)
        
            if ts_hl >= ts_ll:
                #data = self.m_model.GetTimeRangeData(self.current_select_file_path, ts_hl, ts_ll)
                cmd = self.m_model.GetTimeRangeCmd(self.current_select_file_path, ts_hl, ts_ll)
                page_name = "%s: %s [%s:%s ~ %s:%s]"%(self.current_select_project_name, 
                                                      self.current_select_file_name,
                                                      self.ll_hr, self.ll_mm,
                                                      self.hl_hr, self.hl_mm)
                '''
                if  not data and len(data) > 1:
                    pass
                else:
                    page_name = "%s: %s [%s:%s ~ %s:%s]"%(self.current_select_project_name, 
                                                          self.current_select_file_name,
                                                          self.ll_hr, self.ll_mm,
                                                          self.hl_hr, self.hl_mm)
                
                    self.mAddGridPage(page_name, data[0], data)
                '''
                GridDataPage(self.m_view.m_auimanager, 
                             page_name, 
                             self.current_select_file_path, 
                             cmd, 
                             self.grid_max_row_number,
                             self.m_view.m_progress,
                             0)

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
                
    """
    def mAddGridPage(self, page_name, col_title, data):
       
        self.lock.acquire()
        mParent = self.m_view.m_auimanager
        
        mPanel = wx.Panel(mParent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Panel_Sizer = wx.BoxSizer(wx.VERTICAL)
        
        row_size = len(data)
        col_size = len(col_title)
        
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
        self.lock.release()
       
        pass
    """
    """
    def mAddMultiGridPage(self, filename, page_name):
        mParent = self.m_view.m_auimanager
        mPanel = wx.Panel(mParent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Panel_Sizer = wx.BoxSizer(wx.VERTICAL)
        
        mPanel.yy = 'ssssssssssssssssssssssssssssssssssssssssssss'
        
        status_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_Sizer = wx.BoxSizer(wx.VERTICAL)
        Panel_Sizer.Add( status_Sizer, 0, 0, 5 )
        Panel_Sizer.Add( grid_Sizer, 0, wx.EXPAND, 5 )
            
        
        parse = model.LogParse()
        data_len = parse.find_total_row_number(filename)
        row_limit = self.grid_max_row_number
        page_number = 1
                
                
        if data_len > row_limit:
            page_number = data_len/row_limit
            if not data_len%row_limit == 0:
                page_number += 1
            else:
                pass
        else:
            pass 
        
        
        spinCtrl = wx.SpinCtrl(mPanel, 
                                 wx.ID_ANY, u'454545', 
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 wx.SP_WRAP, 
                                 1, page_number, 1)
        '''
        spinCtrl = wx.SpinButton(mPanel, 
                                 wx.ID_ANY,
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 wx.SP_WRAP)
        '''
        staticText = wx.StaticText( mPanel, 
                                    wx.ID_ANY, 
                                    u"Total Rows: " + str(data_len), 
                                    wx.DefaultPosition, 
                                    wx.DefaultSize, 0 )
        status_Sizer.Add(spinCtrl, 1, wx.EXPAND|wx.RIGHT, 5)
        status_Sizer.Add(staticText, 1, wx.ALL, 5)        
                
        offset = 0
        '''
        for num in range(0, page_number):
            page_name_text =  page_name + '_#' + str(num)
            data = self.m_model.GetRowRangeData(filename, row_limit, offset)
            offset += (row_limit+1)
                    
            if data and len(data) >1:
                self.mAddMultiGridPage(page_name, data[0], data)
                        #self.mAddGridPage(page_name_text, data[0], data)
            else:
                pass
        pass
        '''
        
        self.m_view.Bind(wx.EVT_SPINCTRL, self.mTest, spinCtrl)
        data = self.m_model.GetRowRangeData(filename, row_limit, offset)
        
        
        row_size = len(data)
        col_size = len(data[0])
        mGrid = HugeTableGrid(mPanel, data[0], data, row_size, col_size)
        
        grid_Sizer.Add( mGrid, 1, wx.EXPAND, 5 )
        mPanel.SetSizer(Panel_Sizer)
        mPanel.Layout()
        self.m_view.m_auimanager.AddPage(mPanel, page_name, False)
        pass
    """
        
   
    
    
    
    






























if __name__ == '__main__':
    app = wx.App()
    ctrl = Controller(None)
    app.MainLoop()
    pass
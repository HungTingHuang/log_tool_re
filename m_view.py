#wxPython
import wx



class View(wx.Frame):
    #override
    def __init__(self, parent):
        
        
        #init component
        dirpicker = None
        #dir tree
        treectrl = None
        notebook = None
        
        wx.Frame.__init__ ( self, 
                            parent, 
                            id = wx.ID_ANY, 
                            title='DataisBeautiful', 
                            pos = wx.Point( 0,0 ), 
                            size = wx.Size( 800, 600 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
       
        hSizer_all = wx.BoxSizer( wx.HORIZONTAL )
        #right side
        vSizer_dirpicker = wx.BoxSizer( wx.VERTICAL )
        
        #DirPicker
        dirpicker = wx.DirPickerCtrl( self, 
                                      wx.ID_ANY, 
                                      wx.EmptyString, 
                                      u"Select a folder", 
                                      wx.DefaultPosition, 
                                      wx.DefaultSize, 
                                      wx.DIRP_DEFAULT_STYLE )
        vSizer_dirpicker.Add(dirpicker, 0, 0, 5 )
        #DirTree
        treectrl = wx.TreeCtrl(self,
                               wx.ID_ANY,
                               wx.DefaultPosition,
                               wx.DefaultSize)
        
        #Add picture
        treectrl.il = wx.ImageList( 16, 16)
        treectrl.fldridx = treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        treectrl.fldropemidx = treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16)))
        treectrl.fileidx = treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16,16)))
        treectrl.AssignImageList(treectrl.il)
        
        vSizer_dirpicker.Add(treectrl, 1, wx.EXPAND, 5)
        
        hSizer_all.Add(vSizer_dirpicker, 0, wx.EXPAND, 5)
        
        vSizer_notebook = wx.BoxSizer( wx.VERTICAL )
        vSizer_notebook_t = wx.BoxSizer( wx.VERTICAL )
        
        notebook = wx.Notebook( self, 
                                wx.ID_ANY, 
                                wx.DefaultPosition,
                                wx.DefaultSize,
                                0)
        
        
        
        #panel #01
        notebook.panel_01 = wx.Panel(notebook, 
                                       wx.ID_ANY, 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 
                                       wx.TAB_TRAVERSAL)
        vSizer_panel_01 = wx.BoxSizer(wx.VERTICAL)
        notebook.panel_01.SetSizer(vSizer_panel_01)
        notebook.panel_01.Layout()
        vSizer_panel_01.Fit(notebook.panel_01)
        notebook.AddPage(notebook.panel_01,
                         u"a page",
                         False)
        
        #panel #02
        notebook.panel_02 = wx.Panel(notebook,
                                     wx.ID_ANY,
                                     wx.DefaultPosition, 
                                     wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        vSizer_panel_02 = wx.BoxSizer( wx.VERTICAL )
        notebook.panel_02.filepicker = wx.FilePickerCtrl(notebook.panel_02,
                                                         wx.ID_ANY,
                                                         wx.EmptyString,
                                                         u"Select a file",
                                                         u"*.*",
                                                         wx.DefaultPosition,
                                                         wx.DefaultSize,
                                                         wx.FLP_DEFAULT_STYLE)
        vSizer_panel_02.Add(notebook.panel_02.filepicker, 0, wx.ALL, 5)
        notebook.panel_02.SetSizer(vSizer_panel_02)
        notebook.panel_02.Layout()
        vSizer_panel_02.Fit(notebook.panel_02)
        notebook.AddPage(notebook.panel_02, u"a page", False)
        
        #panel #03
        notebook.panel_03 = wx.Panel(notebook,
                                     wx.ID_ANY,
                                     wx.DefaultPosition,
                                     wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        gSizer_panel_03 = wx.GridSizer( 0, 2, 0, 0 )
        notebook.panel_03.radio_01 = wx.RadioButton(notebook.panel_03,
                                                    wx.ID_ANY,
                                                    u"RadioBtn",
                                                    wx.DefaultPosition,
                                                    wx.DefaultSize,
                                                    0)
        notebook.panel_03.radio_02 = wx.RadioButton(notebook.panel_03,
                                                    wx.ID_ANY,
                                                    u"RadioBtn",
                                                    wx.DefaultPosition,
                                                    wx.DefaultSize,
                                                    0)
        notebook.panel_03.radio_03 = wx.RadioButton(notebook.panel_03,
                                                    wx.ID_ANY,
                                                    u"RadioBtn",
                                                    wx.DefaultPosition,
                                                    wx.DefaultSize,
                                                    0)
        notebook.panel_03.radio_04 = wx.RadioButton(notebook.panel_03,
                                                    wx.ID_ANY,
                                                    u"RadioBtn",
                                                    wx.DefaultPosition,
                                                    wx.DefaultSize,
                                                    0)
        gSizer_panel_03.Add(notebook.panel_03.radio_01, 0, wx.ALL, 5)
        gSizer_panel_03.Add(notebook.panel_03.radio_02, 0, wx.ALL, 5)
        gSizer_panel_03.Add(notebook.panel_03.radio_03, 0, wx.ALL, 5)
        gSizer_panel_03.Add(notebook.panel_03.radio_04, 0, wx.ALL, 5)
        notebook.panel_03.SetSizer(gSizer_panel_03)
        notebook.panel_03.Layout()
        gSizer_panel_03.Fit(notebook.panel_03)
        notebook.AddPage(notebook.panel_03, u"a page", False)
        
        #panel 04
        notebook.panel_04 = wx.Panel(notebook,
                                     wx.ID_ANY,
                                     wx.DefaultPosition,
                                     wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        vSizer_panel_04 = wx.BoxSizer(wx.VERTICAL)
        notebook.panel_04.Layout()
        vSizer_panel_04.Fit(notebook.panel_04)
        notebook.AddPage(notebook.panel_04, u"a page", True)
        
        vSizer_notebook_t.Add(notebook, 0, wx.EXPAND, 5)
        vSizer_notebook.Add( vSizer_notebook_t, 0, wx.EXPAND, 5)
        
        #aui notebook
        vSizer_auinotebook = wx.BoxSizer(wx.VERTICAL)
        
        
        vSizer_notebook.Add(vSizer_auinotebook, 1, wx.EXPAND, 5)
        hSizer_all.Add(vSizer_notebook, 1, wx.EXPAND, 5)
        
        self.SetSizer(hSizer_all)
        self.Layout()
        
        statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        
        menubar = wx.MenuBar(0)
        menu_01 = wx.Menu()
        menubar.Append(menu_01, u"&File")
        menu_02 = wx.Menu()
        menubar.Append(menu_02, u"&Setting")
        menu_03 = wx.Menu()
        menubar.Append(menu_03, u"&About")
        self.SetMenuBar(menubar)
        
        self.Center(wx.BOTH)
        
        self.m_dirpicker = dirpicker
        self.m_treectrl = treectrl
        
        pass
        
   
        
        
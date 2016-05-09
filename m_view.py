#wxPython
import wx


class mainFrame(wx.Frame):
    #override
    def __init__(self, parent):
        #init component
        self.m_dirpicker = None
        #dir tree
        self.m_treectrl = None
        self.m_notebook = None
        
        wx.Frame.__init__ ( self, 
                            parent, id = wx.ID_ANY, 
                            title='DataisBeautiful', 
                            pos = wx.Point( 0,0 ), 
                            size = wx.Size( 800, 600 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
       
        hSizer = wx.BoxSizer( wx.HORIZONTAL )
        #right side
        vSizer_rs = wx.BoxSizer( wx.VERTICAL )
        
        #DirPicker
        self.m_dirpicker = wx.DirPickerCtrl( self, 
                                             wx.ID_ANY, 
                                             wx.EmptyString, 
                                             u"Select a folder", 
                                             wx.DefaultPosition, 
                                             wx.DefaultSize, 
                                             wx.DIRP_DEFAULT_STYLE )
        vSizer_rs.Add(self.m_dirpicker, 0, 0, 5)
        #DirTree
        self.m_treectrl = wx.TreeCtrl(self,
                                      wx.ID_ANY,
                                      wx.DefaultPosition,
                                      wx.DefaultSize)
        #Add picture
        self.m_treectrl.il = wx.ImageList( 16, 16)
        self.m_treectrl.fldridx = self.m_treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.m_treectrl.fldropemidx = self.m_treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16)))
        self.m_treectrl.fileidx = self.m_treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16,16)))
        self.m_treectr.AssignImageList(self.m_treectrl.il)
        
        vSizer_rs.Add(self.m_treectrl, wx.EXPAND, 5)
        
        hSizer.Add(vSizer_rs, 0, wx.EXPAND, 5)
        
        bSizer55 = wx.BoxSizer( wx.VERTICAL )
        bSizer78 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_notebook = wx.Notebook( self, 
                                       wx.ID_ANY, 
                                       wx.DefaultPosition,
                                       wx.DefaultSize,
                                       0)
        
        
        
        
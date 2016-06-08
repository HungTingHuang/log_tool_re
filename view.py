#wxPython
import wx
import wx.grid
import wx.aui
#import wx.lib.agw.aui as wx_aui

#import EnhancedStatusBar as statusBar

# Horizontal Alignment Constants
ESB_ALIGN_CENTER_VERTICAL = 1
ESB_ALIGN_TOP = 2
ESB_ALIGN_BOTTOM = 3

# Vertical Alignment Constants
ESB_ALIGN_CENTER_HORIZONTAL = 11
ESB_ALIGN_LEFT = 12
ESB_ALIGN_RIGHT = 13

# Exact Fit (Either Horizontal Or Vertical Or Both) Constant
ESB_EXACT_FIT = 20



# Horizontal Alignment Constants
ESB_ALIGN_CENTER_VERTICAL = 1
ESB_ALIGN_TOP = 2
ESB_ALIGN_BOTTOM = 3

# Vertical Alignment Constants
ESB_ALIGN_CENTER_HORIZONTAL = 11
ESB_ALIGN_LEFT = 12
ESB_ALIGN_RIGHT = 13

# Exact Fit (Either Horizontal Or Vertical Or Both) Constant
ESB_EXACT_FIT = 20


# ---------------------------------------------------------------
# Class EnhancedStatusBar
# ---------------------------------------------------------------
# This Is The Main Class Implementation. See The Demo For Details
# ---------------------------------------------------------------
class EnhancedStatusBarItem(object):
    def __init__(self, widget, pos, horizontalalignment=ESB_ALIGN_CENTER_HORIZONTAL, verticalalignment=ESB_ALIGN_CENTER_VERTICAL):
        self.__dict__.update( locals() )

class EnhancedStatusBar(wx.StatusBar):

    def __init__(self, parent, id=wx.ID_ANY, style=wx.ST_SIZEGRIP,
                 name="EnhancedStatusBar"):
        """Default Class Constructor.

        EnhancedStatusBar.__init__(self, parent, id=wx.ID_ANY,
                                   style=wx.ST_SIZEGRIP,
                                   name="EnhancedStatusBar")
        """
        
        wx.StatusBar.__init__(self, parent, id, style, name)
        
        self._items = {}
        self._curPos = 0
        self._parent = parent
        
        wx.EVT_SIZE(self, self.OnSize) 
        wx.CallAfter(self.OnSize, None)

            
    def OnSize(self, event):
        """Handles The wx.EVT_SIZE Events For The StatusBar.

        Actually, All The Calculations Linked To HorizontalAlignment And
        VerticalAlignment Are Done In This Function."""

        for pos, item in self._items.items():
            widget, horizontalalignment, verticalalignment = item.widget, item.horizontalalignment, item.verticalalignment
           
            rect = self.GetFieldRect(pos)
            widgetpos = widget.GetPosition()
            widgetsize = widget.GetSize()

            rect = self.GetFieldRect(pos)
            
            if horizontalalignment == ESB_EXACT_FIT:
                
                if verticalalignment == ESB_EXACT_FIT:
                    widget.SetSize((rect.width-2, rect.height-2))
                    widget.SetPosition((rect.x-1, rect.y-1))
                elif verticalalignment == ESB_ALIGN_CENTER_VERTICAL:
                    if widgetsize[1] < rect.width - 1:
                        diffs = (rect.height - widgetsize[1])/2
                        widget.SetSize((rect.width-2, widgetsize[1]))
                        widget.SetPosition((rect.x-1, rect.y+diffs))
                    else:
                        widget.SetSize((rect.width-2, widgetsize[1]))
                        widget.SetPosition((rect.x-1, rect.y-1))
                elif verticalalignment == ESB_ALIGN_TOP:
                    widget.SetSize((rect.width-2, widgetsize[1]))
                    widget.SetPosition((rect.x-1, rect.y))
                elif verticalalignment == ESB_ALIGN_BOTTOM:
                    widget.SetSize((rect.width-2, widgetsize[1]))
                    widget.SetPosition((rect.x-1, rect.height-widgetsize[1]))

            elif horizontalalignment == ESB_ALIGN_LEFT:
                
                xpos = rect.x - 1
                if verticalalignment == ESB_EXACT_FIT:
                    widget.SetSize((widgetsize[0], rect.height-2))
                    widget.SetPosition((xpos, rect.y-1))
                elif verticalalignment == ESB_ALIGN_CENTER_VERTICAL:
                    if widgetsize[1] < rect.height - 1:
                        diffs = (rect.height - widgetsize[1])/2
                        widget.SetPosition((xpos, rect.y+diffs))
                    else:
                        widget.SetSize((widgetsize[0], rect.height-2))
                        widget.SetPosition((xpos, rect.y-1))
                elif verticalalignment == ESB_ALIGN_TOP:
                    widget.SetPosition((xpos, rect.y))
                elif verticalalignment == ESB_ALIGN_BOTTOM:
                    widget.SetPosition((xpos, rect.height-widgetsize[1]))
                
            elif horizontalalignment == ESB_ALIGN_RIGHT:
                
                xpos = rect.x + rect.width - widgetsize[0] - 1
                if verticalalignment == ESB_EXACT_FIT:
                    widget.SetSize((widgetsize[0], rect.height-2))
                    widget.SetPosition((xpos, rect.y-1))
                elif verticalalignment == ESB_ALIGN_CENTER_VERTICAL:
                    if widgetsize[1] < rect.height - 1:
                        diffs = (rect.height - widgetsize[1])/2
                        widget.SetPosition((xpos, rect.y+diffs))
                    else:
                        widget.SetSize((widgetsize[0], rect.height-2))
                        widget.SetPosition((xpos, rect.y-1))
                elif verticalalignment == ESB_ALIGN_TOP:
                    widget.SetPosition((xpos, rect.y))
                elif verticalalignment == ESB_ALIGN_BOTTOM:
                    widget.SetPosition((xpos, rect.height-widgetsize[1]))

            elif horizontalalignment == ESB_ALIGN_CENTER_HORIZONTAL:
                
                xpos = rect.x + (rect.width - widgetsize[0])/2 - 1
                if verticalalignment == ESB_EXACT_FIT:
                    widget.SetSize((widgetsize[0], rect.height))
                    widget.SetPosition((xpos, rect.y))
                elif verticalalignment == ESB_ALIGN_CENTER_VERTICAL:
                    if widgetsize[1] < rect.height - 1:
                        diffs = (rect.height - widgetsize[1])/2
                        widget.SetPosition((xpos, rect.y+diffs))
                    else:
                        widget.SetSize((widgetsize[0], rect.height-1))
                        widget.SetPosition((xpos, rect.y+1))
                elif verticalalignment == ESB_ALIGN_TOP:
                    widget.SetPosition((xpos, rect.y))
                elif verticalalignment == ESB_ALIGN_BOTTOM:
                    widget.SetPosition((xpos, rect.height-widgetsize[1]))

                
        if event is not None:
            event.Skip()
        
        
    def AddWidget(self, widget, horizontalalignment=ESB_ALIGN_CENTER_HORIZONTAL,
                  verticalalignment=ESB_ALIGN_CENTER_VERTICAL, pos = -1):
        """Add A Widget To The EnhancedStatusBar.

        Parameters:

        - horizontalalignment: This Can Be One Of:
          a) ESB_EXACT_FIT: The Widget Will Fit Horizontally The StatusBar Field Width;
          b) ESB_ALIGN_CENTER_HORIZONTAL: The Widget Will Be Centered Horizontally In
             The StatusBar Field;
          c) ESB_ALIGN_LEFT: The Widget Will Be Left Aligned In The StatusBar Field;
          d) ESB_ALIGN_RIGHT: The Widget Will Be Right Aligned In The StatusBar Field;

        - verticalalignment:
          a) ESB_EXACT_FIT: The Widget Will Fit Vertically The StatusBar Field Height;
          b) ESB_ALIGN_CENTER_VERTICAL: The Widget Will Be Centered Vertically In
             The StatusBar Field;
          c) ESB_ALIGN_BOTTOM: The Widget Will Be Bottom Aligned In The StatusBar Field;
          d) ESB_ALIGN_TOP: The Widget Will Be TOP Aligned In The StatusBar Field;

        """

        if pos == -1:
            pos = self._curPos
            self._curPos += 1
        
        if self.GetFieldsCount() <= pos:
            raise "\nERROR: EnhancedStatusBar has a max of %d items, you tried to set item #%d" % (self.GetFieldsCount(), pos)

        if horizontalalignment not in [ESB_ALIGN_CENTER_HORIZONTAL, ESB_EXACT_FIT,
                                       ESB_ALIGN_LEFT, ESB_ALIGN_RIGHT]:
            raise '\nERROR: Parameter "horizontalalignment" Should Be One Of '\
                  '"ESB_ALIGN_CENTER_HORIZONTAL", "ESB_ALIGN_LEFT", "ESB_ALIGN_RIGHT"' \
                  '"ESB_EXACT_FIT"'

        if verticalalignment not in [ESB_ALIGN_CENTER_VERTICAL, ESB_EXACT_FIT,
                                     ESB_ALIGN_TOP, ESB_ALIGN_BOTTOM]:
            raise '\nERROR: Parameter "verticalalignment" Should Be One Of '\
                  '"ESB_ALIGN_CENTER_VERTICAL", "ESB_ALIGN_TOP", "ESB_ALIGN_BOTTOM"' \
                  '"ESB_EXACT_FIT"'
        

        try:
            self.RemoveChild(self._items[pos].widget)
            self._items[pos].widget.Destroy()
        except KeyError: pass
        
        self._items[pos] = EnhancedStatusBarItem(widget, pos, horizontalalignment, verticalalignment)
        
        wx.CallAfter(self.OnSize, None)






class View(wx.Frame):
    #override
    def __init__(self, parent):
        
        
        #init component
        dirpicker = None
        #dir tree
        treectrl = None
        notebook = None
        #aui manager
        auimanager = None
        
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
        treectrl.fldropenidx = treectrl.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16)))
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
        '''
        notebook.panel_01.fgSizer_1 = wx.FlexGridSizer(0, 2, 0, 50)
        notebook.panel_01.fgSizer_1.SetFlexibleDirection( wx.BOTH )
        notebook.panel_01.fgSizer_1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        notebook.panel_01.active_proj = wx.StaticText(notebook.panel_01, 
                                                      wx.ID_ANY, 
                                                      u'', 
                                                      wx.DefaultPosition, 
                                                      wx.DefaultSize, 
                                                      0)
        notebook.panel_01.active_proj.Wrap(-1)
        notebook.panel_01.fgSizer_1.Add(notebook.panel_01.active_proj, 
                                        1, 
                                        wx.EXPAND)
        
        notebook.panel_01.sql_command = wx.StaticText(notebook.panel_01,
                                                      wx.ID_ANY,
                                                      u'',
                                                      wx.DefaultPosition,
                                                      wx.DefaultSize,
                                                      0)
        notebook.panel_01.sql_command.Wrap(-1)
        notebook.panel_01.fgSizer_1.Add(notebook.panel_01.sql_command, 
                                        1, 
                                        wx.EXPAND)
        
        vSizer_panel_01.Add(notebook.panel_01.fgSizer_1, 0, 0, 5)
        '''
        notebook.panel_01.fgSizer_2 = wx.FlexGridSizer( 0, 8, 0, 0 )
        notebook.panel_01.fgSizer_2.SetFlexibleDirection( wx.BOTH )
        notebook.panel_01.fgSizer_2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        notebook.panel_01.checkBox = wx.CheckBox( notebook.panel_01, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
        notebook.panel_01.checkBox.SetValue(False)
        notebook.panel_01.fgSizer_2.Add( notebook.panel_01.checkBox, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        m_choice_hr = []
        for hh in range(0, 24):
            m_choice_hr.append('%s hr'%hh)
        
        m_choice_mm = []
        for mm in range(0, 60):
            m_choice_mm.append('%s min'%mm)
        
        notebook.panel_01.choice1 = wx.Choice( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_hr, wx.NO_BORDER )
        notebook.panel_01.choice1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        notebook.panel_01.choice1.SetSelection( 0 )
        notebook.panel_01.fgSizer_2.Add( notebook.panel_01.choice1, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        notebook.panel_01.choice2 = wx.Choice( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_mm, wx.NO_BORDER )
        notebook.panel_01.choice2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        notebook.panel_01.choice2.SetSelection( 0 )
        notebook.panel_01.fgSizer_2.Add( notebook.panel_01.choice2, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        notebook.panel_01.fgSizer_2.AddSpacer( ( 15, 0), 0, 0, 5 )
        
        notebook.panel_01.staticText_1 = wx.StaticText( notebook.panel_01, wx.ID_ANY, u"to", wx.DefaultPosition, wx.DefaultSize, 0 )
        notebook.panel_01.staticText_1.Wrap( -1 )
        notebook.panel_01.staticText_1.Disable()
        notebook.panel_01.fgSizer_2.Add( notebook.panel_01.staticText_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        notebook.panel_01.fgSizer_2.AddSpacer( ( 15, 0), 0, 0, 5 )
        
        notebook.panel_01.choice3 = wx.Choice( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_hr, wx.NO_BORDER )
        notebook.panel_01.choice3.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        notebook.panel_01.choice3.SetSelection( 0 )
        notebook.panel_01.choice3.Disable()
        notebook.panel_01.fgSizer_2.Add( notebook.panel_01.choice3, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        notebook.panel_01.choice4 = wx.Choice( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_mm, wx.NO_BORDER )
        notebook.panel_01.choice4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        notebook.panel_01.choice4.SetSelection( 0 )
        notebook.panel_01.choice4.Disable()
        notebook.panel_01.fgSizer_2.Add( notebook.panel_01.choice4, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        vSizer_panel_01.Add(notebook.panel_01.fgSizer_2, 0, 0, 5)
        
        notebook.panel_01.vSizer = wx.BoxSizer( wx.VERTICAL )
        notebook.panel_01.button_01 = wx.Button( notebook.panel_01, wx.ID_ANY, u"send", wx.DefaultPosition, wx.Size(60, 15), 0 )
        notebook.panel_01.vSizer.Add( notebook.panel_01.button_01, 1, wx.ALIGN_RIGHT, 5 )
        vSizer_panel_01.Add( notebook.panel_01.vSizer, 1, wx.ALIGN_RIGHT, 5 )
        
        
        
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
        auimanager = wx.aui.AuiNotebook(self,
                                        wx.ID_ANY,
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        wx.aui.AUI_NB_DEFAULT_STYLE)
        vSizer_auinotebook.Add(auimanager, 1, wx.EXPAND, 5)
        vSizer_notebook.Add(vSizer_auinotebook, 1, wx.EXPAND, 5)
        hSizer_all.Add(vSizer_notebook, 1, wx.EXPAND, 5)
        
        self.SetSizer(hSizer_all)
        self.Layout()
        
        status_bar = EnhancedStatusBar(self, -1)
        status_bar.SetFieldsCount(4)
        self.SetStatusBar(status_bar)
        self.m_progress = wx.Gauge(status_bar, range=100)
        status_bar.AddWidget(self.m_progress, pos=3, wx.EXPAND)
        
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
        self.m_auimanager = auimanager
        
        self.m_np1_checkBox_01 = notebook.panel_01.checkBox
        self.m_np1_staticText_01 = notebook.panel_01.staticText_1
        self.m_np1_choice_01 = notebook.panel_01.choice1
        self.m_np1_choice_02 = notebook.panel_01.choice2
        self.m_np1_choice_03 = notebook.panel_01.choice3
        self.m_np1_choice_04 = notebook.panel_01.choice4
        self.m_np1_button_01 = notebook.panel_01.button_01
        #self.m_active_proj = notebook.panel_01.active_proj
        #self.m_sql_command = notebook.panel_01.sql_command
        self.m_statusBar = status_bar
        pass
        
   
        
        
#wxPython
import wx
import wx.grid
import wx.aui
import wx.propgrid as pg
import wx.lib.agw.aui

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


#view global variables
g_progress = None




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
        
        
        
        #panel #01 Data Mining
#===================================================================================================================#      
        
        
        notebook.panel_01 = wx.Panel(notebook, 
                                     wx.ID_ANY, 
                                     wx.DefaultPosition, 
                                     wx.DefaultSize, 
                                     wx.TAB_TRAVERSAL)
        
        vSizer_panel_01 = wx.BoxSizer(wx.VERTICAL)
        hSizer_nb1_1f = wx.BoxSizer( wx.HORIZONTAL )
        hSizer_nb1_2f = wx.BoxSizer( wx.HORIZONTAL )
        hSizer_nb1_3f = wx.BoxSizer( wx.HORIZONTAL )
        
        vSizer_panel_01.Add( hSizer_nb1_1f, 1, wx.EXPAND, 5 )
        vSizer_panel_01.Add( hSizer_nb1_2f, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
        vSizer_panel_01.Add( hSizer_nb1_3f, 0, wx.BOTTOM|wx.EXPAND|wx.ALIGN_RIGHT, 1 )
        #hSizer_nb1_1f ==============================================================================================
        #hSizer_nb1_1f_src start
        hSizer_nb1_1f_table = wx.BoxSizer( wx.HORIZONTAL )
        
        m_choice_proj = ['Project Name', 
                         'DEV_iRide',
                         'FujiQ_iRide',
                         'Zoo_Emmem',
                         'SSM_AOT',
                         'SSM_Odyssey',
                         'SSM_Trex',
                         'SSM_Balloon']
        
        c_nb1_1f_proj = wx.Choice( notebook.panel_01, 
                                       wx.ID_ANY, 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 
                                       m_choice_proj, 0 )
        
        c_nb1_1f_proj.SetSelection(0)
        
        hSizer_nb1_1f_table.Add( c_nb1_1f_proj, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        
        m_choice_table = ['Table Name']
        
        c_nb1_1f_table = wx.Choice( notebook.panel_01, 
                                       wx.ID_ANY, 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 
                                       m_choice_table, 0 )
        
        c_nb1_1f_table.SetSelection(0)
        
        hSizer_nb1_1f_table.Add( c_nb1_1f_table, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        hSizer_nb1_1f.Add( hSizer_nb1_1f_table, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        vst_nb1_1f_0 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_1f.Add( vst_nb1_1f_0, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        
        hSizer_nb1_1f_src = wx.BoxSizer( wx.HORIZONTAL )
        st_nb1_1f_src = wx.StaticText( notebook.panel_01, 
                                       wx.ID_ANY, 
                                       u"SRC", 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 0 )
        st_nb1_1f_src.Wrap( -1 )
        hSizer_nb1_1f_src.Add( st_nb1_1f_src, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        tc_nb1_1f_sc = wx.TextCtrl( notebook.panel_01, 
                                    wx.ID_ANY, 
                                    wx.EmptyString, 
                                    wx.DefaultPosition, 
                                    wx.DefaultSize, 0 )
        
        hSizer_nb1_1f_src.Add( tc_nb1_1f_sc, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        hSizer_nb1_1f.Add( hSizer_nb1_1f_src, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        #hSizer_nb1_1f_src end
        vst_nb1_1f_1 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_1f.Add( vst_nb1_1f_1, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_1f_state start
        hSizer_nb1_1f_state = wx.BoxSizer( wx.HORIZONTAL )
        
        st_nb1_1f_state = wx.StaticText( notebook.panel_01, 
                                         wx.ID_ANY, 
                                         u"STATE", 
                                         wx.DefaultPosition, 
                                         wx.DefaultSize, 0 )
        st_nb1_1f_state.Wrap( -1 )
        hSizer_nb1_1f_state.Add( st_nb1_1f_state, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        tc_nb1_1f_state = wx.TextCtrl( notebook.panel_01, 
                                            wx.ID_ANY, 
                                            wx.EmptyString, 
                                            wx.DefaultPosition, 
                                            wx.DefaultSize, 0 )
        
        hSizer_nb1_1f_state.Add( tc_nb1_1f_state, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        hSizer_nb1_1f.Add( hSizer_nb1_1f_state, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_1f_state end
        vst_nb1_1f_2 = wx.StaticLine( notebook.panel_01,  wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_1f.Add( vst_nb1_1f_2, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_1f_level start
        hSizer_nb1_1f_level = wx.BoxSizer( wx.HORIZONTAL )
        
        st_nb1_1f_level = wx.StaticText( notebook.panel_01, 
                                         wx.ID_ANY, 
                                         u"LEVEL", 
                                         wx.DefaultPosition, 
                                         wx.DefaultSize, 0 )
        st_nb1_1f_level.Wrap( -1 )
        hSizer_nb1_1f_level.Add( st_nb1_1f_level, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        tc_nb1_1f_level = wx.TextCtrl( notebook.panel_01, 
                                       wx.ID_ANY, 
                                       wx.EmptyString, 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 0 )
        
        hSizer_nb1_1f_level.Add( tc_nb1_1f_level, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        hSizer_nb1_1f.Add( hSizer_nb1_1f_level, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_1f_level end
        vst_nb1_1f_3 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_1f.Add( vst_nb1_1f_3, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_1f_bk1 start
        hSizer_nb1_1f_bk1 = wx.BoxSizer( wx.HORIZONTAL )
        hSizer_nb1_1f_bk1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        hSizer_nb1_1f.Add( hSizer_nb1_1f_bk1, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_1f_bk1 end
        #hSizer_nb1_1f_bk2 start
        hSizer_nb1_1f_count = wx.BoxSizer( wx.HORIZONTAL )
        
        st_nb1_1f_count = wx.StaticText( notebook.panel_01, 
                                         wx.ID_ANY, 
                                         u"PAGE MAX ROWS:", 
                                         wx.DefaultPosition, 
                                         wx.DefaultSize, 0 )
        st_nb1_1f_count.Wrap( -1 )
        hSizer_nb1_1f_count.Add( st_nb1_1f_count, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        slider_nb1_1f_count = wx.Slider( notebook.panel_01, 
                                         wx.ID_ANY, 
                                         8192, 8192, 32768, 
                                         wx.DefaultPosition, 
                                         wx.Size( -1,10 ), 
                                         wx.SL_HORIZONTAL|wx.SL_LABELS)
        hSizer_nb1_1f_count.Add( slider_nb1_1f_count, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        
        
        hSizer_nb1_1f.Add( hSizer_nb1_1f_count, 1, wx.EXPAND, 5 )
        #hSizer_nb1_2f_count end
        
        
        
        #hSizer_nb1_1f_bk2 end
        #hSizer_nb1_2f ==============================================================================================
        #hSizer_nb1_2f_timezone start
        hSizer_nb1_2f_timezone = wx.BoxSizer( wx.HORIZONTAL )
        m_choice_timezone = []
        
        for utc_offset in range(0, 11):
            m_choice_timezone.append('UTC -%s:00'%(11-utc_offset))
        for utc_offset in range(0, 13):
            m_choice_timezone.append('UTC +%s:00'%utc_offset)
        
        
        c_nb1_2f_timezone = wx.Choice( notebook.panel_01, 
                                       wx.ID_ANY, 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 
                                       m_choice_timezone, 0 )
        c_nb1_2f_timezone.SetSelection( 11 )
        hSizer_nb1_2f_timezone.Add( c_nb1_2f_timezone, 0, wx.RIGHT, 5)
        hSizer_nb1_2f.Add( hSizer_nb1_2f_timezone, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        #hSizer_nb1_2f_timezone end
        vst_nb1_2f_0 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_2f.Add( vst_nb1_2f_0, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        #hSizer_nb1_2f_range start
        
        hSizer_nb1_2f_range = wx.BoxSizer( wx.HORIZONTAL )
        
        cb_nb1_2f_range = wx.CheckBox( notebook.panel_01, 
                                       wx.ID_ANY, 
                                       u"  SINGLE", 
                                       wx.DefaultPosition, 
                                       wx.DefaultSize, 0 )
        cb_nb1_2f_range.SetValue(False) 
        hSizer_nb1_2f_range.Add( cb_nb1_2f_range, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        m_choice_hr = []
        for hh in range(0, 24):
            m_choice_hr.append('%s hr'%hh)
        m_choice_mm = []
        for mm in range(0, 60):
            m_choice_mm.append('%s min'%mm)
        
        
        
        c_nb1_2f_lh = wx.Choice( notebook.panel_01, 
                                 wx.ID_ANY, 
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 m_choice_hr, 0 )
        c_nb1_2f_lh.SetSelection( 0 )
        hSizer_nb1_2f_range.Add( c_nb1_2f_lh, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        c_nb1_2f_lm = wx.Choice( notebook.panel_01, 
                                 wx.ID_ANY, 
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 m_choice_mm, 0 )
        c_nb1_2f_lm.SetSelection( 0 )
        hSizer_nb1_2f_range.Add( c_nb1_2f_lm, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        tc_nb1_2f_l = wx.TextCtrl( notebook.panel_01, 
                                   wx.ID_ANY, 
                                   wx.EmptyString, 
                                   wx.DefaultPosition, 
                                   wx.DefaultSize, 0 )
        hSizer_nb1_2f_range.Add( tc_nb1_2f_l, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        st_nb1_2f_between = wx.StaticText( notebook.panel_01, wx.ID_ANY, u"OFFSET", wx.DefaultPosition, wx.DefaultSize, 0 )
        st_nb1_2f_between.Wrap( -1 )
        hSizer_nb1_2f_range.Add( st_nb1_2f_between, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
            
        c_nb1_2f_hh = wx.Choice( notebook.panel_01, 
                                 wx.ID_ANY, 
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 m_choice_hr, 0 )
        c_nb1_2f_hh.SetSelection( 0 )
        hSizer_nb1_2f_range.Add( c_nb1_2f_hh, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        c_nb1_2f_hm = wx.Choice( notebook.panel_01, 
                                 wx.ID_ANY, 
                                 wx.DefaultPosition, 
                                 wx.DefaultSize, 
                                 m_choice_mm, 0 )
        c_nb1_2f_hm.SetSelection( 0 )
        hSizer_nb1_2f_range.Add( c_nb1_2f_hm, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        tc_nb1_2f_h = wx.TextCtrl( notebook.panel_01, 
                                   wx.ID_ANY, 
                                   wx.EmptyString, 
                                   wx.DefaultPosition, 
                                   wx.DefaultSize, 0 )
        hSizer_nb1_2f_range.Add( tc_nb1_2f_h, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        
        hSizer_nb1_2f.Add( hSizer_nb1_2f_range, 3, wx.EXPAND, 5 )
        #hSizer_nb1_2f_range end
        vst_nb1_2f_1 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_2f.Add( vst_nb1_2f_1, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        #hSizer_nb1_2f_count start
        hSizer_nb1_2f_bk1 = wx.BoxSizer( wx.HORIZONTAL )
        hSizer_nb1_2f_bk1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        hSizer_nb1_2f.Add( hSizer_nb1_2f_bk1, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_3f ==============================================================================================
        #hSizer_nb1_3f_like start
        hSizer_nb1_3f_like = wx.BoxSizer( wx.HORIZONTAL )
        
        st_nb1_3f_like = wx.StaticText( notebook.panel_01, 
                                        wx.ID_ANY, 
                                        u"MSG LIKE", 
                                        wx.DefaultPosition, 
                                        wx.DefaultSize, 0 )
        st_nb1_3f_like.Wrap( -1 )
        hSizer_nb1_3f_like.Add( st_nb1_3f_like, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        tc_nb1_3f_like = wx.TextCtrl( notebook.panel_01, 
                                      wx.ID_ANY, 
                                      wx.EmptyString, 
                                      wx.DefaultPosition, 
                                      wx.DefaultSize, 0 )
        hSizer_nb1_3f_like.Add( tc_nb1_3f_like, 1, wx.RIGHT|wx.LEFT, 5 )
        
        
        hSizer_nb1_3f.Add( hSizer_nb1_3f_like, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_3f_like end
        vst_nb1_3f_1 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        hSizer_nb1_3f.Add( vst_nb1_3f_1, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        #hSizer_nb1_3f_cmd start
        hSizer_nb1_3f_cmd = wx.BoxSizer( wx.HORIZONTAL )
        
        cb_nb1_3f_cmd = wx.CheckBox( notebook.panel_01, 
                                     wx.ID_ANY, 
                                     wx.EmptyString, 
                                     wx.DefaultPosition, 
                                     wx.DefaultSize, 0 )
        cb_nb1_3f_cmd.SetValue(False)
        hSizer_nb1_3f_cmd.Add( cb_nb1_3f_cmd, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        tc_nb1_3f_cmd = wx.TextCtrl( notebook.panel_01, 
                                     wx.ID_ANY, 
                                     wx.EmptyString, 
                                     wx.DefaultPosition, 
                                     wx.DefaultSize, 0)
        tc_nb1_3f_cmd.SetEditable(False)
        #tc_nb1_3f_cmd.SetStyle(tc_nb1_3f_cmd.GetRange, wx.TE_READONLY)
        #tc_nb1_3f_cmd.SetBackgroundColour((255,23,23))
        
        hSizer_nb1_3f_cmd.Add( tc_nb1_3f_cmd, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        hSizer_nb1_3f_cmd.AddSpacer( ( 15, 0), 0, wx.EXPAND, 5 )
        
        hSizer_nb1_3f.Add( hSizer_nb1_3f_cmd, 4, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
        #hSizer_nb1_3f_cmd end
        #vst_nb1_3f_2 = wx.StaticLine( notebook.panel_01, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        #hSizer_nb1_3f.Add( vst_nb1_3f_2, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        #hSizer_nb1_3f_btn start
        hSizer_nb1_3f_btn = wx.BoxSizer( wx.HORIZONTAL )
        #hSizer_nb1_3f_btn.AddSpacer( ( 15, 0), 0, wx.EXPAND, 5 )
        btn_nb1_3f_reset = wx.Button( notebook.panel_01, 
                                      wx.ID_ANY, 
                                      u"RESET", 
                                      wx.DefaultPosition, 
                                      wx.DefaultSize, 0 )
        hSizer_nb1_3f_btn.Add( btn_nb1_3f_reset, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        btn_nb1_3f_query = wx.Button( notebook.panel_01, 
                                      wx.ID_ANY, 
                                      u"QUERY", 
                                      wx.DefaultPosition, 
                                      wx.DefaultSize, 0 )
        hSizer_nb1_3f_btn.Add( btn_nb1_3f_query, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        hSizer_nb1_3f.Add( hSizer_nb1_3f_btn, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        #hSizer_nb1_3f_btn end
        
        
        
       
        
        notebook.panel_01.SetSizer(vSizer_panel_01)
        notebook.panel_01.Layout()
        vSizer_panel_01.Fit(notebook.panel_01)
        notebook.AddPage(notebook.panel_01,
                         u"Data Mining",
                         False)
        
        #ctrl panel_01
        #ctrl panel_01 1f
        #m_choice_table
        self.m_np1_1f_proj = c_nb1_1f_proj
        self.m_np1_1f_table = c_nb1_1f_table
        self.m_np1_1f_tc_src = tc_nb1_1f_sc
        self.m_np1_1f_tc_state = tc_nb1_1f_state
        self.m_np1_1f_tc_level =tc_nb1_1f_level
        #ctrl panel_01 2f
        self.m_np1_2f_timezone = c_nb1_2f_timezone
        self.m_np1_checkBox_01 = cb_nb1_2f_range
        self.m_np1_st_offset = st_nb1_2f_between
        self.m_np1_st_range = cb_nb1_2f_range
        self.m_np1_2f_tc_ll = tc_nb1_2f_l
        self.m_np1_2f_tc_hh = tc_nb1_2f_h
        
        self.m_np1_choice_01 = c_nb1_2f_lh
        self.m_np1_choice_02 = c_nb1_2f_lm
        self.m_np1_choice_03 = c_nb1_2f_hh
        self.m_np1_choice_04 = c_nb1_2f_hm
        
        self.m_np1_1f_slider = slider_nb1_1f_count
        
        #ctrl panel_01 3f
        self.m_np1_3f_tc_like = tc_nb1_3f_like
        self.m_np1_3f_cb_cmd = cb_nb1_3f_cmd
        self.m_np1_3f_tc_cmd = tc_nb1_3f_cmd
        self.m_np1_3f_btn_reset = btn_nb1_3f_reset
        self.m_np1_3f_btn_query = btn_nb1_3f_query
        
#===================================================================================================================#
        #panel #02
        notebook.panel_02 = wx.Panel(notebook,
                                     wx.ID_ANY,
                                     wx.DefaultPosition, 
                                     wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        vSizer_panel_02 = wx.BoxSizer( wx.VERTICAL )
        
        self.btn_nb2_test = wx.Button( notebook.panel_02, 
                                      wx.ID_ANY, 
                                      u"Test", 
                                      wx.DefaultPosition, 
                                      wx.DefaultSize, 0 )
        vSizer_panel_02.Add(self.btn_nb2_test, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        
        notebook.panel_02.SetSizer(vSizer_panel_02)
        notebook.panel_02.Layout()
        vSizer_panel_02.Fit(notebook.panel_02)
        notebook.AddPage(notebook.panel_02, u"Parsing", False)
        
        #panel #03
        notebook.panel_03 = wx.Panel(notebook,
                                     wx.ID_ANY,
                                     wx.DefaultPosition,
                                     wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
       
        notebook.panel_03.Layout()
        notebook.AddPage(notebook.panel_03, u"Data Visualization", False)
        
        #panel 04
        notebook.panel_04 = wx.Panel(notebook,
                                     wx.ID_ANY,
                                     wx.DefaultPosition,
                                     wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        vSizer_panel_04 = wx.BoxSizer(wx.VERTICAL)
        notebook.panel_04.Layout()
        vSizer_panel_04.Fit(notebook.panel_04)
        notebook.AddPage(notebook.panel_04, u"Report", True)
        
        vSizer_notebook_t.Add(notebook, 0, wx.EXPAND, 5)
        vSizer_notebook.Add( vSizer_notebook_t, 0, wx.EXPAND, 5)
        
        #aui notebook
        vSizer_auinotebook = wx.BoxSizer(wx.VERTICAL)
        
        
        
        
        auinotebook = wx.wx.lib.agw.aui.AuiNotebook(self,
                                                    wx.ID_ANY,
                                                    wx.DefaultPosition,
                                                    wx.DefaultSize,
                                                    wx.aui.AUI_NB_DEFAULT_STYLE)
        
        #auimanager_t = wx.lib.agw.aui.AuiManager(auinotebook)
        
        vSizer_auinotebook.Add(auinotebook, 1, wx.EXPAND, 5)
        vSizer_notebook.Add(vSizer_auinotebook, 1, wx.EXPAND, 5)
        hSizer_all.Add(vSizer_notebook, 1, wx.EXPAND, 5)
        
        
        self.SetSizer(hSizer_all)
        self.Layout()
        
        status_bar = EnhancedStatusBar(self, -1)
        status_bar.SetFieldsCount(4)
        self.SetStatusBar(status_bar)
        self.m_progress = wx.Gauge(status_bar, range=100)
        global g_progress
        g_progress = self.m_progress
        
        
        status_bar.AddWidget(self.m_progress, 
                             ESB_EXACT_FIT, 
                             ESB_EXACT_FIT,
                             pos=3)
        
       
        self.Center(wx.BOTH)
        
        self.m_dirpicker = dirpicker
        self.m_treectrl = treectrl
        self.m_auinotebook = auinotebook
        self.m_notebook = notebook
        
        #self.m_auimanager_t = auimanager_t
        
        #self.m_np1_button_01 = notebook.panel_01.button_01
        #self.m_active_proj = notebook.panel_01.active_proj
        #self.m_sql_command = notebook.panel_01.sql_command
        self.m_statusBar = status_bar
        
        pass
        
    
    
    
    
    @staticmethod
    def Info(text):
        dial = wx.MessageDialog(None, text, 'Info', wx.OK)
        dial.ShowModal()
        dial.Destroy()
        
    @staticmethod
    def Warring(text):
        dial = wx.MessageDialog(None, text, 'Error', 
            wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        dial.Destroy()
        
    
    @staticmethod    
    def Question(text):
        dial = wx.MessageDialog(None, text, 'Question', 
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        return dial.ShowModal().GetValue()
        dial.Destroy()
    
    @staticmethod
    def Alert(text):
        dial = wx.MessageDialog(None, text, 'Exclamation', 
            wx.OK | wx.ICON_EXCLAMATION)
        dial.ShowModal()
        dial.Destroy()
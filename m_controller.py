#m_controller
import wx
import m_view
import m_model


class Controller:
    def __init__(self, app):
        self.view = m_view.View(None)
        self.model = m_model.Model()

        #event bind
        self.view.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirSelected, self.view.m_dirpicker)


        self.view.Show()
        
    def OnDirSelected(self, evt):
        tree = self.view.m_treectrl
        tree.DeleteAllItems()
        root = tree.AddRoot(self.view.m_dirpicker.GetPath())
        tree.SetItemImage(root, tree.fldridx, wx.TreeItemIcon_Normal)
        tree.SetItemImage(root, tree.fldropenidx, wx.TreeItemIcon_Expanded)
        tree.SetItemHasChildren(root, True)    
        
        pass
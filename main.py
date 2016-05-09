import wx
import m_view


if __name__ == '__main__':
    app = wx.App()
    view = m_view.mainFrame(None)
    view.Show()
    app.MainLoop()
    pass
    
    

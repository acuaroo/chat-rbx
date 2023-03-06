import wx
import win32gui

selection = {'top': 258, 'left': 5, 'width': 400, 'height': 25}

class Desktop(wx.Frame):
    def __init__(self):
        super(Desktop,self).__init__(None,-1,'')
        self.AssociateHandle(win32gui.GetDesktopWindow())
        dc = wx.WindowDC(self)
        dc.SetPen(wx.Pen('red', 2))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle( selection['left'], selection['top'], selection['width'], selection['height'] )
        

app = wx.App(0)
mf = Desktop()
app.MainLoop()
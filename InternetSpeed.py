import wx.adv
import wx
from PIL import Image, ImageDraw,ImageFont
import speedtest   

hasInternet = False
font_type  = ImageFont.truetype("arial.ttf", 36)
image= "pil_text.ico"

TRAY_TOOLTIP = 'Internet Speed' 
TRAY_ICON = image

try:
    st = speedtest.Speedtest()
    hasInternet = True
except:
    print("No Internet")    

def reqSpeedNChangeImg(disText):
    if disText==":(" or disText==".....":
        global img        
        img = Image.new('RGBA', (30, 42), color = (255, 255, 255, 1))  # color background =  white  with transparency
    else:      
        img = Image.new('RGBA', (60, 42), color = (255, 255, 255, 1))  # color background =  white  with transparency
        
    global d
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 1000), (1000, 1000)], fill=(0, 0, 0), outline=None)  #  color = blue
    
    txt = disText
            
    d.text((0,0), f"{txt}", fill=(255,255,255), font = font_type)

    img.save(image)
    
    TRAY_ICON = image

    print(txt)



def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        if hasInternet:
            reqSpeedNChangeImg(st.download())
            self.set_icon(TRAY_ICON)
        else:
            reqSpeedNChangeImg(":(")
            self.set_icon(TRAY_ICON)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Test', self.on_hello)
        create_menu_item(menu, 'Reconnect', self.reconnect_internet)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):      
        print ('Tray icon was left-clicked.')

    def on_hello(self, event):

        reqSpeedNChangeImg(".....")
        self.set_icon(TRAY_ICON)
        

        if hasInternet:
            reqSpeedNChangeImg(st.download())
            self.set_icon(TRAY_ICON)
        else:
            reqSpeedNChangeImg(":(")
            self.set_icon(TRAY_ICON)

    def reconnect_internet(self, event):
        reqSpeedNChangeImg(".....")
        self.set_icon(TRAY_ICON)
        try:
            st = speedtest.Speedtest()
            hasInternet = True
            reqSpeedNChangeImg(st.download())
            self.set_icon(TRAY_ICON)            
        except:
            reqSpeedNChangeImg(":(")
            self.set_icon(TRAY_ICON)
            print("No Internet")    

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
    
    

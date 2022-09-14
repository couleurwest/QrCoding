import dataclasses
import tkinter
from tkinter import ttk, font

"""style = ttk.Style()
style.theme_use('clam')
style.map('TEntry', lightcolor=[('focus', 'white')])

"""
class MeConfig:
    projet_path: str
    generation_path: str
    font_name = 'Book Antiqua'
    font_normal = (font_name, 12)
    font_normal_bold = (font_name, 12, "bold")
    font_normal_italic = (font_name, 12, "italic")

    font_h1 = (font_name, 18, 'bold')
    font_h2 = (font_name, 16, 'bold')

    max_width = 800
    max_height = 600
    color_primary = "#017396"
    color_secondary = "Ivory"
    color_focus = "#700070"
    color_focus_light = "#ff99ff"
    color_light = "white"


class MeLabel(tkinter.Label):
    def __init__(self, *args, **kwargs):
        kwargs['background'] = "#017396"
        kwargs['foreground'] = "#ffffff"
        kwargs['borderwidth'] = 0
        kwargs['font'] = MeConfig.font_normal_bold
        super(MeLabel, self).__init__(*args, **kwargs)


class MeEntry(tkinter.Entry):
    def __init__(self, *args, **kwargs):
        kwargs['selectbackground'] = "#017396"
        kwargs['highlightbackground'] = "#700070"
        kwargs['foreground'] =  "#017396"
        kwargs['borderwidth'] = 0
        kwargs['font'] = ('courier', 12, 'normal')
        kwargs['relief'] = tkinter.FLAT
        kwargs['highlightthickness'] = 0

        super(MeEntry, self).__init__(*args, **kwargs)
        self.config(highlightbackground="red", highlightcolor="red")


class MeButton(tkinter.Button):
    def __init__(self, *args, **kwargs):
        kwargs['foreground'] = "#ffffff"
        kwargs['borderwidth'] = 1
        kwargs['background'] = MeConfig.color_focus
        kwargs['font'] = MeConfig.font_normal_bold
        kwargs['relief'] = tkinter.GROOVE
        kwargs['padx'] = 20
        kwargs['pady'] = 5
        super(MeButton, self).__init__(*args, **kwargs)


class RichText(tkinter.Text):
    def __init__(self, *args, **kwargs):
        kwargs['padx'] = 30
        kwargs['pady'] = 20
        super().__init__(*args, **kwargs)
        default_font = font.nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = font.Font(**default_font.configure())
        italic_font = font.Font(**default_font.configure())

        h1_font = font.Font(**default_font.configure())
        h2_font = font.Font(**default_font.configure())

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        h1_font.configure(size=int(default_size*2), weight="bold")
        h2_font.configure(size=int(default_size*1.5), weight="bold")

        self.tag_configure("bold", font=bold_font)
        self.tag_configure("italic", font=italic_font)
        self.tag_configure("h1", font=h1_font, spacing3=default_size)
        self.tag_configure("h2", font=h2_font, spacing3=default_size)

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")



"""def resizer(e):
    global src, resized, bg, canvas
    src = os.path.join(project_path, r'.src\pics\bg.png')
    image = Image.open(src)
    resized = image.resize ((e.width, e.height), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(resized)
    canvas.create_image(0, 0, image=bg, anchor = tkinter.NW)
    canvas.create_text( 120, 20, text="QRCoding", fill='pink')
    canvas.pack()"""
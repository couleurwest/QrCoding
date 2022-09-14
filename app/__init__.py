import os
from tkinter import  Tk

from PIL import Image, ImageTk

from app.mewidget import formulaire, toolbox

from app.mewidget import *

class QRCoding(Tk):
    wtitle = "QRCoding 3.0"
    wbg = "#017396"
    max_width = 800
    max_height = 640
    wsize = f'{max_width}x{max_height}'


    def __init__(self, *arg, **kwargs):
        super(QRCoding, self).__init__("qrcoding", *arg, **kwargs)
        self.title(self.wtitle)
        self.geometry(self.wsize)
        self.iconphoto(False, tkinter.PhotoImage(file=os.path.join(MeConfig.projet_path, r'.src\pics\qrcondingico.png')))
        #self.config(bg=self.bg)
        self.page_run()

    def visuel(self):
        src = os.path.join(MeConfig.projet_path, r'.src\pics\qrcode.png')
        image = Image.open(src)
        resized = image.resize((150, 150), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized)

    def header(self):
        canvas = tkinter.Canvas(self, width=self.max_width, height=100, bg='white')
        canvas.create_image(20, 0, image=self.visuel(), anchor = tkinter.NW)
        canvas.create_line(75, 0, 75, 140)
        canvas.create_text( 120, 20, text="QRCoding", fill='pink')
        canvas.pack()

    def page_run(self):
        src = os.path.join(MeConfig.projet_path, r'.src\pics\qrcode.png')
        image = Image.open(src)
        resized = image.resize((100, 100), Image.Resampling.LANCZOS)
        bg= ImageTk.PhotoImage(resized)

        canvas = tkinter.Canvas(self, width=self.max_width, height=100, bg='white')
        canvas.create_image(10, 0, image=bg, anchor=tkinter.NW)
        canvas.create_line(120, 10, 120, 80)
        canvas.create_text(200, 30, text="QRCoding", fill=self.wbg, font=MeConfig.font_h1)
        canvas.create_text(260, 65, text="Génération de QRCode vCard et URL", fill=self.wbg, font=MeConfig.font_normal_italic)

        src2 = os.path.join(MeConfig.projet_path, r'.src\pics\wwgf.png')
        image2 = Image.open(src2)
        resized2 = image2.resize((150, 90), Image.Resampling.LANCZOS)
        bg2 = ImageTk.PhotoImage(resized2)
        canvas.create_image(800, 0, image=bg2, anchor=tkinter.NE)

        canvas.pack()

        formulaire.QRForms(self).pack()
        footer = tkinter.Canvas(self, width=self.max_width, height=30, bg=MeConfig.color_primary)
        footer.create_text(230, 15,
                           text="Besoin de plus, d'un produit adapté, à votre image : contact@couleurwest-it.com",
                           fill="Ivory")

        footer.create_text(670, 15,
                           text="(c) 2022- Couleur West IT | couleurwest-it.com",
                           fill=MeConfig.color_secondary)
        footer.pack(side=tkinter.BOTTOM)

        self.config(menu=self.create_menu_bar())
        self.mainloop()



    def __show_info(self):
        d = MyDialog(self)
        self.wait_window(d.top)

    def create_menu_bar(self):
        menu_bar =tkinter.Menu(self)

        menu_bar.add_command(label="Informations", command=self.__show_info)
        menu_bar.add_cascade(label="Fermer", command=self.destroy)

        return menu_bar

class MyDialog():
    def __init__(self, parent):
        self.top = tkinter.Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.title("Informations")
        self.top.bind("<Escape>", self.cancel)
        self.top.bind("<Return>", self.cancel)
        # Create the text widget
        text_widget = RichText(self.top, height=250, width=100)
        scroll_bar = tkinter.Scrollbar(self.top)

        scroll_bar.pack(side=tkinter.RIGHT)
        text_widget.pack(side=tkinter.LEFT)
        long_text = """##This is a multiline string.
        We can write this in multiple lines too!
        Hello from AskPython. This is the third line.
        This is the fourth line. Although the length of the text is longer than
        the width, we can use tkinter's scrollbar to solve this problem!
        """

        # Insert text into the text widget
        text_widget.insert(tkinter.END, "QRCoding 3.0\n","h1")
        text_widget.insert(tkinter.END, """==================================================\n""")

        text_widget.insert(tkinter.END, "Auteur : ","bold")
        text_widget.insert(tkinter.END, "Ketsia LENTIN\n")
        text_widget.insert(tkinter.END, "Copyright : ","bold")
        text_widget.insert(tkinter.END, "2022 - Couleur West IT (973GF)\n")
        text_widget.insert(tkinter.END, "Contact : ","bold")
        text_widget.insert(tkinter.END, "contact@couleurwest-it.com\n")
        text_widget.insert(tkinter.END, "Site web : ","bold")
        text_widget.insert(tkinter.END, "https://couleurwest-it.com\n\n\n")

        text_widget.insert(tkinter.END, "Condition Générale\n", "h2")
        text_widget.insert(tkinter.END,
                           """Cet outils vous est proposé par Couleur West IT, conception et réalisation de solution numérique adaptée.\nL'exploitation de cet outils est limité uniquement à son utilisation ; il est strictement interdit de reproduire, fabriquer, vendre ou commercialisé QRCoding 3.0.\nLes images et logos sont la proriété de Couleur West IT\n\n""")
        text_widget.insert(tkinter.END, "Données personnelles\n", "h2")
        text_widget.insert(tkinter.END,
                           """Aucunes données n'est enregistrées, récupérées ou traitées en dehors du context si ce n'est le QR Code, dans le répertoire "génération" (repertoire d'installation)\nLes données (QRCode) enregistrées sur le poste utilisateur sont, de ce fait, soumises à la responsabilité de l'utilsateur.\n""")

        text_widget.insert(tkinter.END, "Utilisation\n", "h2")
        text_widget.insert(tkinter.END, 'vCard QRCode\n', "bold")
        text_widget.insert(tkinter.END, """1 - Indiquer à minima : un nom et l'adresse mail\n""", "bullet")
        text_widget.insert(tkinter.END, """2 - Cliquer sur "vCard QRCode"\n""", "bullet")

        text_widget.insert(tkinter.END, 'URL QRCod\n', "bold")
        text_widget.insert(tkinter.END, """1 - Saisir uniquement un lien pour le site web\n""", "bullet")
        text_widget.insert(tkinter.END, """2 - Cliquer sur "URL QRCode"\n\n""", "bullet")


        text_widget.insert(tkinter.END, """                      =======================================================\n""", "bold")
        text_widget.insert(tkinter.END, """        CLIQUER ECHAP ou ENTRER POUR SORTIR\n""", "h1")
        text_widget.insert(tkinter.END, """                      =======================================================\n""", "bold")


        tkinter.mainloop()

    def cancel(self, event=None):
        self.top.destroy()

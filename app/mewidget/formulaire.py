import dataclasses
import re
import tkinter
from tkinter import messagebox

from PIL import Image

from . import MeLabel, MeConfig, MeEntry, MeButton, toolbox


@dataclasses.dataclass
class formvalidation():
    lastname: bool = False
    website: bool = True
    email: bool = False
    phone1: bool = True
    phone2: bool = True

    @property
    def is_valid(self):

        for k, v in self.__dict__.items():
            if v == False:
                break
        return v

    @property
    def is_urlvalid(self):
       return self.website

class QRForms(tkinter.Frame):
    firstname_entry = None
    lastname_entry = None
    corp_entry = None
    website_entry = None
    email_entry = None
    phone1_entry = None
    phone2_entry = None
    btn_vcard = None
    btn_ucard = None
    tracker = None

    formvalidation = formvalidation()
    formcard = None

    class CCard:

        def __init__(self,lastname, firstname, email, corp, phone1, phone2, website):
            self.lastname = toolbox.clean_space(lastname).upper()
            self.firstname = toolbox.clean_space(firstname).capitalize()
            self.email = toolbox.clean_allspace(email).lower()
            self.corp = toolbox.clean_space(corp).upper()
            self.phone1 = toolbox.clean_space(phone1).capitalize()
            self.phone2 = toolbox.clean_space(phone2).lower()
            self.website = toolbox.clean_allspace(website).lower()

        @property
        def card_name(self):
            """Mise en forme identité"""
            return ','.join([self.lastname, self.firstname])

        @property
        def fn(self):
            """Mise en forme identité"""
            return ';'.join([self.lastname, self.firstname])

        @property
        def dn(self):
            """Mise en forme identité"""
            return ' '.join([self.lastname, self.firstname])

        @property
        def card_phone(self):
            return list(map(lambda d: toolbox.clean_space(d), filter(lambda d: d, [self.phone1, self.phone2])))

        @property
        def mecard_data(self):
            """Donnes au foram MeCard"""
            dcm = {
                'email': self.email,
                'nickname': self.corp,
                'url': self.website,
                'phone': self.card_phone,
                'name': self.card_name,
            }
            return {k: v for (k, v) in dcm.items() if v}

        @property
        def vcard_data(self):
            """Donnes au foram MeCard"""
            dcm = {
                'email': self.email,
                'org': self.corp,
                'url': self.website,
                'phone': self.card_phone,
            }
            return {k: v for (k, v) in dcm.items() if v}

        @property
        def mecard(self):
            """schement de validation """
            dcm = {
                'email': self.email,
                'url': self.website,
                'phone_1': self.phone1,
                'phone_2': self.phone2,
                'name': self.lastname,
                'surname': self.firstname,
            }

    def load_value (self):
        self.formcard = self.CCard(
            self.lastname_entry.get(),
            self.firstname_entry.get(),
            self.email_entry.get(),
            self.corp_entry.get(),
            self.phone1_entry.get(),
            self.phone2_entry.get(),
            self.website_entry.get())


    def vcard_qrcoding(self):
        if self.formvalidation.is_valid:
            from segno import helpers

            self.load_value()

            qrcode = helpers.make_vcard(self.formcard.fn, self.formcard.dn, **self.formcard.vcard_data)
            src = toolbox.path_build(MeConfig.generation_path,"/qrcode_vcard.png" )
            qrcode.save(src, dark=MeConfig.color_primary, scale=4)
            #self.tracker = f"QRCode generated : {path_build(self.export, 'qrcode_vcard.png')}"

            messagebox.showinfo("QRCoding: Generation", 'generation/qrcode_vcard.png')

        else:
            messagebox.showinfo("QRCoding: Generation", 'Formulaire non valide, vérifiez votre saisie')

    def url_entry_qrcoding(self):
        if self.url_validation(self.website_entry.get()) :
            self.load_value()
            if  self.formcard.website:
                import qrcode

                src = toolbox.path_build(MeConfig.projet_path, ".src/pics/qrcoding.png")
                logo = Image.open(src)

                basewidth = 100

                # adjust image size
                wpercent = (basewidth / float(logo.size[0]))
                hsize = int((float(logo.size[1]) * float(wpercent)))

                logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

                QRcode = qrcode.QRCode(
                    error_correction=qrcode.constants.ERROR_CORRECT_H
                )

                # adding URL or text to QRcode
                QRcode.add_data( self.formcard.website)

                # generating QR code
                QRcode.make()

                # taking color name from user
                QRcolor = MeConfig.color_primary

                # adding color to QR code
                QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGB')

                # set size of QR code
                pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
                QRimg.paste(logo, pos)

                # save the QR code generated
                src = toolbox.path_build(MeConfig.generation_path, "qrcode_uri.png")

                QRimg.save(src)
                messagebox.showinfo("QRCoding: Generation", 'generation/qrcode_uri.png')
                return
        messagebox.showinfo("QRCoding: Generation", 'URL non valide, vérifiez votre saisie')


    def __init__(self, master, *args, **kwargs):
        kwargs['borderwidth'] = 0
        kwargs['relief'] = tkinter.SOLID
        kwargs['bg'] = MeConfig.color_primary

        super(QRForms, self).__init__(master, *args, **kwargs)

        self.pack(side=tkinter.TOP, padx=30, pady=30, ipadx=20)

        label = MeLabel(self, text="Nom de famille", font=MeConfig.font_normal_bold)
        label.grid(row=1, column=1, sticky='W', padx=10, pady=10)

        vcmd = (self.register(self.name_validation), '%P')
        ivcmd = (self.register(self.name_invalid))

        self.lastname_entry = MeEntry(self, width=33)
        self.lastname_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.lastname_entry.grid(row=2, column=1, ipadx=10, pady=0)

        label = MeLabel(self, text="Prénom")
        label.grid(row=1, column=2, sticky='W', padx=10)

        self.firstname_entry = MeEntry(self, width=33)
        self.firstname_entry.grid(row=2, column=2, ipadx=10, pady=0)

        label = MeLabel(self, text="Entreprise", )
        label.grid(row=3, column=1, sticky='W', padx=10, pady=10)

        self.corp_entry = MeEntry(self, width=72)
        self.corp_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=0)

        label = MeLabel(self, text="Adresse electronique")
        label.grid(row=5, column=1, sticky='W', padx=10, pady=10)

        vcmd = (self.register(self.email_validation), '%P')
        ivcmd = (self.register(self.email_invalid),)

        self.email_entry = MeEntry(self, width=72)
        self.email_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.email_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

        label = MeLabel(self, text="téléphone 1")
        label.grid(row=7, column=1, sticky='W', padx=10)

        vcmd = (self.register(self.phone_validation), '%P', '%W')
        ivcmd = (self.register(self.phone_invalid), '%W')
        self.phone1_entry = MeEntry(self, width=33, name="phone1")
        self.phone1_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.phone1_entry.grid(row=8, column=1, ipadx=10, pady=0)

        label = MeLabel(self, text="Téléphone 2", )
        label.grid(row=7, column=2, sticky='W', padx=10)

        vcmd = (self.register(self.phone_validation), '%P', '%W')
        ivcmd = (self.register(self.phone_invalid), '%W')
        self.phone2_entry = MeEntry(self, width=33, name="phone2")
        self.phone2_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.phone2_entry.grid(row=8, column=2, ipadx=10, pady=10)

        label = MeLabel(self, text="Site Web")
        label.grid(row=9, column=1, sticky='W', padx=10, pady=10)

        vcmd = (self.register(self.url_validation), '%P')
        ivcmd = (self.register(self.url_invalid))
        self.website_entry = MeEntry(self, width=72)
        self.website_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.website_entry.grid(row=10, column=1, columnspan=2, padx=10, pady=0)

        self.btn_vcard = MeButton(self, text="vCard QRCoding", command=self.vcard_qrcoding, state=tkinter.DISABLED)
        self.btn_vcard.grid(row=11, column=1, padx=20, pady=20)

        self.btn_ucard = MeButton(self, text="URL QRCoding", command=self.url_entry_qrcoding, state=tkinter.DISABLED)
        self.btn_ucard.grid(row=11, column=2, padx=20, pady=20)

    def name_validation(self, value):
        self.lastname_entry.config(bg=MeConfig.color_light)
        value = toolbox.clean_space(value)
        valid = (value != "")
        self.formvalidation.lastname = valid

        self.btn_vcard.configure(state= tkinter.NORMAL if self.formvalidation.is_valid else tkinter.DISABLED)

        return valid

    def name_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.lastname_entry.config(bg=MeConfig.color_focus_light)

    def email_validation(self, value):
        self.email_entry.config(bg=MeConfig.color_light)
        value = toolbox.clean_allspace(value).lower()
        regex = re.compile(r"""([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+""")
        valid = regex.fullmatch(value) is not None
        self.formvalidation.email = valid

        print(self.formvalidation.is_valid)
        self.btn_vcard.configure(state= tkinter.NORMAL if self.formvalidation.is_valid else tkinter.DISABLED)

        return valid

    def email_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.email_entry.config(bg=MeConfig.color_focus_light)

    def url_validation(self, value):
        self.website_entry.config(bg=MeConfig.color_light)
        regex = re.compile(r"""^http(s)?://(\w[\w.-]*[/]?)+[.]\w{2,3}$""")
        value = toolbox.clean_allspace(value).lower()

        if value:
            valid = regex.fullmatch(value) is not None
        else:
            valid = True

        self.formvalidation.website = valid and value
        self.btn_vcard.configure(state= tkinter.NORMAL if self.formvalidation.is_valid else tkinter.DISABLED)
        self.btn_ucard.configure(state= tkinter.NORMAL if self.formvalidation.is_urlvalid else tkinter.DISABLED)

        return valid

    def url_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.website_entry.config(bg=MeConfig.color_focus_light)

    def phone_validation(self, value, elm):
        if "phone1" in elm:
            self.phone1_entry.config(bg=MeConfig.color_light)
        elif "phone2" in elm:
            self.phone2_entry.config(bg=MeConfig.color_light)

        value = toolbox.clean_allspace(value)
        if value:
            regex = re.compile(r"""([+]\d+|0)\d{9,}""")  # chaines commençant par b ou B
            valid = regex.fullmatch(value) is not None
        else:
            valid = True

        self.btn_vcard.configure(state = tkinter.NORMAL if self.formvalidation.is_valid else tkinter.DISABLED)

        return valid

    def phone_invalid(self, elm):
        """
        Show the error message if the data is not valid
        :return:
        """
        name = elm.split('.')
        name = name[-1]
        if name == "phone1":
            self.phone1_entry.config(bg=MeConfig.color_focus_light)
        elif name == "phone2":
            self.phone2_entry.config(bg=MeConfig.color_focus_light)

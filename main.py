'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
val = Validator(request, rules)
result = val.validate() # True
'''
import dataclasses

import kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from validator import validate

from work.validation import UrlRule, PhoneRule

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from PIL import Image
import qrcode

Window.size = (800, 480)
Window.borderless = 1
@dataclasses.dataclass
class UCard():
    name: str
    surname: str

    email: str

    phone_1: str = None
    phone_2: str = None

    url: str = None
    corp: str = None

    @property
    def card_name(self):
        if self.name and self.surname.capitalize():
            return self.name.upper() + ',' + self.surname.capitalize()
        else:
            return self.name or self.surname

    @property
    def card_data(self):

        dcm = {
            'email': self.email,
            'nickname': self.corp,
            'url': self.url,
            'phone': list(filter(lambda d: d, [self.phone_1, self.phone_1])),
            'name': self.card_name,
        }
        return { k:v for (k,v) in dcm.items() if v}


    @property
    def card_validation(self):

        dcm = {
            'email': self.email,
            'url': self.url,
            'phone_1': self.phone_1,
            'phone_2':  self.phone_2,
            'name': self.name,
            'surname': self.surname,
        }
        return { k:v or '' for (k,v) in dcm.items()}




class QRCoder(Screen):
    name = StringProperty()
    surname = StringProperty()
    corp = StringProperty()
    url = StringProperty()
    email = StringProperty()
    phone_1 = StringProperty()
    phone_2 = StringProperty()
    tracker = StringProperty()

    def __vcard(self, **kwargs):
        from segno import helpers
        card = UCard(**kwargs)
        dcm = card.card_validation
        if dcm:
            result, _, errors = validate(dcm, self.card_rules, return_info=True)  # True

            if result:
                qrcode = helpers.make_mecard(**card.card_data)
                qrcode.save('qrcode_vcard.png', dark='#165868', scale=4)
                self.tracker = " QR code generated!"
            else:
                for field, err in errors.items():
                    self.ids[field].background_color =  (0.5, 0, 0, 0.3)# if self.focus else (0, 0, 1, 1)
                self.tracker = "Vérifiez le formulaire"

        else:
            self.tracker = "Renseignez le formulaire"



    def __uri(self,url):

        logo_link = 'logo.png'
        logo = Image.open(logo_link)

        basewidth = 100

        # adjust image size
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))

        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        # adding URL or text to QRcode
        QRcode.add_data(url)

        # generating QR code
        QRcode.make()

        # taking color name from user
        QRcolor = '#165868'

        # adding color to QR code
        QRimg = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')

        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

        # save the QR code generated
        QRimg.save('qrcode_uri.png')

        return True

    def reset_form(self):
        for field in ['name', 'surname', 'email', 'phone_1','phone_2', 'url']:
            self.ids[field].background_color = (1,1,1,1)

    def generate_vcard(self):
        self.reset_form()
        ids = self.ids
        self.__vcard(
            name=ids.name.text,
            surname=ids.surname.text,
            email=ids.email.text,
            phone_1=ids.phone_1.text,
            corp=ids.corp.text,
            phone_2=ids.phone_2.text,
            url=ids.url.text)

    def generate_url(self):
        self.reset_form()
        gen = False
        url = self.ids.url.text.lower()
        if url:
            result, _, errors = validate({'url': self.ids.url.text}, self.url_rules, return_info=True) # True

            if result:
                gen = self.__uri(url)
        self.tracker = "QRCode généré" if gen else "Saisir une URL valide"
    @property
    def card_rules(self):
        return {
            "name": "required",
            "surname": "required",
            "email": "required|mail",
            "url": UrlRule(),
            "phone_1": PhoneRule(),
            "phone_2": PhoneRule()
        }

    @property
    def url_rules(self):
        return {"url": UrlRule()}

    def closeapp(self):
        App.get_running_app().stop()
        Window.close()


class QRCodeApp(App):

    def build(self):
        # return a Button() as a root widget
        return QRCoder()


if __name__ == '__main__':
    QRCodeApp().run()
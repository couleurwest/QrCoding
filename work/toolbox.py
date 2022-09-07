import os
import re
from string import punctuation

RGX_ACCENTS = 'àâäãéèêëîïìôöòõùüûÿñç'
RGX_EMAIL = r'^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$'
RGX_PUNCT = '#!?$%&_@*+-'
RGX_PHONE = r'^0[1-9]\d{8}$'
RGX_URL = r'https?:\/\/(www\.)?[-a-z0-9@:%._\+~#=]{1,256}\.[a-z0-9()]{1,6}\b([-a-z0-9()@:%_\+.~#?&//=]*)'


def string_me(v):
    """ Convertion d'une valeur en chaine

    :param v: valeur à convertir
    :rtype: str, None en cas d'erreur

    """

    try:
        return str(v)
    except:
        return None


def clean_space(ch):
    """ Nettoyage des espaces "superflus"

    * Espaces à gouche et à droite supprimés
    * Répétition d'espace réduit

    :Exemple:
        >>> chaine = 'Se  réveiller au matin        de sa destiné    ! !           '
        >>> clean_space (chaine)
        'Se réveiller au matin  de sa destiné ! !'

    """
    ch = string_me(ch)
    if ch:
        s = string_me(ch)
        return re.sub(r'\s{2,}', ' ', s.strip())
    else:
        return ch


def clean_allspace(ch, very_all=True):
    """Nettoyage de tous les espace et carateres vides

    :param str ch: Chaine à nettoyer
    :param bool very_all: caractère vide aussi, True (False = Espaces uniquement)

    :Exemple:
        >>> chaine = 'Se  réveiller au matin        de sa destiné !'
        >>> clean_allspace (chaine)
        'Seréveilleraumatindesadestiné!'

    """
    c = r'\s' if very_all else '[ ]'
    s = string_me(ch)

    return re.sub(c, '', s.strip())


def clean_coma(ch, w_punk=False):
    """ Supprime les accents/caractères spéciaux du texte source en respectant la casse

    :param ch: Chaine de caractere à "nettoyer"
    :param w_punk: indique si la punctuation est à nettoyer ou pas (suppression)

    :Exemple:
        >>> s = 'Se  réveiller au matin    de sa destiné !!'
        >>> clean_coma (s)
        'Se seveiller au matin (ou pas) de sa destine !!''
        >>> clean_coma (s, True)
        'Se reveiller au matin ou pas de sa destine'

    """

    if w_punk:
        # Nettoyage caractere spéciaux (espace...)
        o_rules = str.maketrans(RGX_ACCENTS, 'aaaaeeeeiiioooouuuync', punctuation)
    else:
        o_rules = str.maketrans(RGX_ACCENTS, 'aaaaeeeeiiioooouuuync')

    return clean_space(ch).translate(o_rules).swapcase().translate(o_rules).swapcase()


def clean_master(ch):
    """ Supprime les accents, caractères spéciaux et espace du texte source

    :param str ch: Chaine de caractere à "nettoyer"
    :return str: chaine sans accents:car. spéciaux ni espace en minuscule

    :Exemple:
        >>> s = 'Se  réveiller au matin  (ou pas) de sa destiné !'
        >>> clean_master (s)
        'sereveilleraumatinoupasdesadestine

    """
    return clean_allspace(clean_coma(ch, True)).lower()


def dircurrent(source=None):
    """Répertoire pour le fichier en cours """
    return os.path.dirname(os.path.realpath((source or __file__)))

def makedirs(path):
    """ Création du répertoire données

    :param path: chemin du répertoire à créer
    :rtype bool:

    """

    if not os.path.exists(path):
        os.makedirs(path)

def path_build(directory ,ps_complement):
    return os.path.abspath(os.path.join(directory, ps_complement))

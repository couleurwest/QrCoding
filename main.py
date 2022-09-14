import os

from app.mewidget import toolbox
from app import MeConfig, QRCoding

if __name__ == '__main__':
    MeConfig.projet_path = os.path.dirname(__file__) + r"\app"
    MeConfig.generation_path = toolbox.path_build(MeConfig.projet_path, 'generation')
    toolbox.makedirs(MeConfig.generation_path )
    QRCoding()

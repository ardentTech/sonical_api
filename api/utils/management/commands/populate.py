from django.core.management.base import BaseCommand

from manufacturing.factories import ManufacturerFactory


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.manufacturers = {}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        self._create_manufacturers()
        print("ALL DONE!")

    def _create_manufacturers(self):
        manufacturers = [
            ('Accuton', 'http://accuton.com/'),
            ('Audax', 'http://www.audax.com/'),
            ('AuraSound', ''),
            ('Aurum Cantus', 'http://www.aurumcantus.com/'),
            ('Celestion', 'http://celestion.com/'),
            ('Dayton Audio', 'http://daytonaudio.com/'),
            ('Eclipse', 'http://www.eclipse-td.com/us/'),
            ('Eminence', 'http://www.eminence.com/'),
            ('Eton', 'http://www.eton-gmbh.com/en/home'),
            ('FaitalPRO', 'http://www.faitalpro.com/'),
            ('Fountek', 'http://www.fountek.net/'),
            ('Fostex', 'http://www.fostextinternational.com/'),
            ('Galaxy Audio', 'http://www.galaxyaudio.com/'),
            ('Goldwood', 'http://www.goldwoodsound.com/'),
            ('GRS', ''),
            ('HiVi', 'http://www.hivi.us/'),
            ('HiWave', ''),
            ('Markaudio', 'http://www.markaudio.com/'),
            ('Morel', 'http://www.morelhifi.com/'),
            ('Mundorf', 'http://www.mundorf.com/'),
            ('Peerless', 'http://www.tymphany.com/peerless/'),
            ('Prescient Audio', 'http://prescientaudio.com/'),
            ('PRV Audio', 'http://prvaudio.com/'),
            ('Pyle', 'http://www.pyleaudio.com/'),
            ('Pyramid', ''),
            ('Quam', 'http://www.quamspeakers.com/'),
            ('Raal', 'http://www.raalribbon.com/'),
            ('SB Acoustics', 'http://www.sbacoustics.com/'),
            ('Scan-Speak', 'http://www.scan-speak.dk/'),
            ('SEAS', 'http://www.seas.no/'),
            ('Tang Band', 'http://www.tb-speaker.com/en/'),
            ('Tectonic Elements', 'http://www.tectonicelements.com/'),
            ('Tianle', 'http://www.tianle.com/en/'),
            ('Titan', ''),
            ('Tymphany', 'http://www.tymphany.com/'),
            ('Vifa', 'http://www.vifa.dk/'),
            ('Visaton', 'http://www.visaton.com/'),
        ]

        for m in manufacturers:
            self.manufacturers[m[0]] = ManufacturerFactory.create(
                name=m[0], website=m[1])

        print("created {0} manufacturers".format(len(manufacturers)))

#! /usr/bin/env python
# -*-  coding: utf-8 -*-
import sys
import os
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from applicationinstance import ApplicationInstance

from apiclient.discovery import build
from places.models import Place, Description
#from utils.cache import kes



import logging
log = logging.getLogger('genel')

from configuration.models import configuration

class TranslationMachine:
    """
    google translation machine
    """
    def __init__(self):
        self.auto_langs = configuration('auto_trans_langs').split(',')
        self.service = build('translate', 'v2', developerKey='AIzaSyAd8evO6SwmuE3RoBdaROzLoNGesc386Vg')
        self.run()

    def translate(self, input, target, source=None):
        try:
#            print target,input
            if source:
                tr = self.service.translations().list(source=source, target=target, q=input).execute()
            else:
                tr = self.service.translations().list(target=target, q=input).execute()
            return   tr['translations']
        except:
            log.exception('unexpected error')

    def run(self):
        print self.auto_langs
        for p in Place.objects.filter(translation_status__lt=30):
            already_translated_langs = p.get_translation_list()
            for l in self.auto_langs:
                if l not in already_translated_langs:
                    translation = self.translate([p.title,p.description],l)
                    if translation:
#                        print 'laaaaaaaaaaaaaaan',p.title,l
#                        print translation[0]
                        d, new = Description.objects.get_or_create(place=p, lang=l)
                        d.text = translation[1]['translatedText']
                        d.title = translation[0]['translatedText']
                        d.auto = True
                        d.save()
            translated_langs = p.get_translation_list()
            if translated_langs:
                p.translation_status = 20
                if all([ (l in translated_langs ) for l in self.auto_langs] ):
                    p.translation_status = 30
                p.save()
















if __name__ == '__main__':
    o = None
    inst = None
    try:
        inst = ApplicationInstance( '/tmp/gtranslate.pid' )

        o = TranslationMachine()
        if inst:
            inst.exitApplication()
    except SystemExit:
        if inst:
            inst.exitApplication()
        pass
    except:
        if inst:
            inst.exitApplication()
        log.exception('beklenmeyen hata')


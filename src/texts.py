#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

langs = {
    'en': {
        'welcome': u'Hi {first_name}! I\'m here to help you complete your Russia 2018 album.',
        'roger': u'Roger that! {first_name}',
        'menu': u'Choose one of the following options',
        '/trades': u'See my trades',
        '/stickers': u'See stickers I have',
        '/wishlist': u'See stickers I need'
    },
    'es': {
        'welcome': u'¡Hola {first_name}! Estoy para ayudarte a completar tu álbum de Rusia 2018.',
        'roger': u'Roger that! {first_name}',
        'menu': u'Elegí una de las siguientes opciones',
        '/trades': u'Ver mis cambios',
        '/stickers': u'Figuritas que tengo',
        '/wishlist': u'Figuritas que quiero'
    }
}

def get_texts(user):
    lang = 'en'
    if 'locale' in user:
        lang = user['locale'].lower()[:2]
    if not lang in langs:
        lang = 'en'

    def get_text(key, **params):
        params.update(user)
        print 'Getting text ' + key, params
        text = langs[lang][key]
        if type(text) == list:
            text = random.choice(text)
        return text.format(**params)

    return get_text
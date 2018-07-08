#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

langs = {
    'en': {
        'welcome': u'Hi {first_name}! I\'m here to help you complete your Russia 2018 album.',
        'roger': u'Roger that! {first_name}',
        'menu': u'Choose one of the following options',
        'hi': [u'Hello {first_name}', u'Hi there {first_name}', u'Hey {first_name}'],
        'wanted_changed': u'Great! We updated the stickers you want',
        'collection_changed': u'Awesome! We updated the stickers you have',
        'no_trades': u'You have no trades',
        'no_stickers': u'You have no stickers',
        'no_wishlist': u'You have no cards in your wishlist',
        'new_transaction': u'We\'ve found a new match!',
        'ask_sticker': u'Which one?',
        'ask_wishlist': u'Which one?',
        'trade': u'Trade {card_put} by {card_get}',
        '/remove_from_collection': u'I don\'t have it',
        '/remove_from_wanted': u'I don\'t want it',
        '/cancel_transaction': u'Cancel it',
        '/trades': u'See my trades',
        '/stickers': u'See stickers I have',
        '/add_sticker': u'Add a sticker',
        '/wishlist': u'See stickers I need',
        '/add_wishlist': u'Add a sticker I need'
    },
    'es': {
        'welcome': u'¡Hola {first_name}! Estoy para ayudarte a completar tu álbum de Rusia 2018.',
        'roger': u'Roger that! {first_name}',
        'menu': u'Elegí una de las siguientes opciones',
        'hi': [u'Hola {first_name}', u'Hola hola {first_name}', u'Buenas! {first_name}'],
        'wanted_changed': u'¡Buenísimo! Cambiamos las figuritas que querés',
        'collection_changed': u'¡Bárbaro! Cambiamos las figuritas que querés',
        'no_trades': u'No tienes ningún cambio',
        'no_stickers': u'No tienes ninguna figurita',
        'no_wishlist': u'No tienes figuritas que quieras',
        'new_transaction': u'Encontramos un nuevo intercambio!',
        'ask_sticker': u'¿Cuál? Dime el número, o una foto',
        'ask_wishlist': u'¿Cuál? Dime el número o una foto',
        'trade': u'Cambiar {card_put} por {card_get}',
        '/remove_from_collection': u'Ya no la tengo',
        '/remove_from_wanted': u'Ya no la quiero',
        '/cancel_transaction': u'Cancelarla',
        '/trades': u'Ver mis cambios',
        '/stickers': u'Figuritas que tengo',
        '/add_sticker': u'Agregar una figurita',
        '/wishlist': u'Figuritas que quiero',
        '/add_wishlist': u'Agregar una figurita'
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
        # print 'Getting text ' + key, params
        text = langs[lang][key]
        if type(text) == list:
            text = random.choice(text)
        return text.format(**params)

    return get_text

#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

langs = {
    'en': {
        'welcome': u'Hi {first_name}! I\'m here to help you find people you can swap stickers with.',
        'roger': u'Roger that! {first_name}',
        'menu': u'Choose one of the following options',
        'default': [u'I\'m not sure I understand', u'I\'m still learning', u'Sorry, I don\'t think I know what you mean'],
        'hi': [u'Hello {first_name}', u'Hi there {first_name}', u'Hey {first_name}'],
        'wanted_changed': u'Great! We updated the stickers you want',
        'collection_changed': u'Awesome! We updated the stickers you have',
        'no_trades': [u'You have no trades', u'Nothing to show in your trades'],
        'no_stickers': [
            u'You have no stickers',
            u'Nothing to show in your collection',
            u'No stickers in your collection'
        ],
        'no_wishlist': [
            u'You have no cards in your wishlist',
            u'Nothing to show in your wishlist',
            u'No stickers in your wishlist'
        ],
        'new_transaction': [
            u'We\'ve found a new match!',
            u'New trading opportunity!'
        ],
        'transaction_line_from_you': [
            u'You can give {card} to {name_to}',
            u'You have {card}, which will go to {name_to}',
            u'{card} will go from you to {name_to}'
        ],
        'transaction_line_to_you': [
            u'{name_from} will give you {card}',
            u'{name_from} has {card}, which will go to you',
            u'{card} will go from {name_from} to you'
        ],
        'transaction_line': [
            u'{name_from} will give {card} to {name_to}',
            u'{name_from} has {card}, which will go to {name_to}',
            u'{card} will go from {name_from} to {name_to}'
        ],
        'transaction_cta': u'Talk to them to arrange when to meet',
        'transaction_finished': u'The transaction has been finished',
        'transaction_canceled': u'The transaction has been canceled',
        'ask_sticker': [
            u'Which one? You can tell me the number or send a pic',
            u'Send me a number or a pick and I\'ll add it to your collection'
        ],
        'ask_wishlist': [
            u'Which one? You can tell me the number or send a pic',
            u'Send me a number or a pick and I\'ll add it to your wishlist'
        ],
        'ask_message': [
            u'What do you wanna say to this group?',
            u'What is your message for the group',
            u'Give me your message and I\'ll forward it to the group'
        ],
        'cta': [
            u'What\'s next?',
            u'What else can I help you with?'
            u'What can I do for you now?'
        ],
        'message_sent': [
            u'Awesome, we forwarded your message',
            u'Your message has been delivered',
            u'We\'ve passed along your message'
        ],
        'message_received': u'{first_name} says:',
        # This are "menu" items, it makes sense to have only one option
        'trade': u'Trade {card_put} by {card_get}',
        'remove_sticker': u'I don\'t have it',
        'remove_wishlist': u'I don\'t want it',
        'cancel_transaction': u'Cancel it',
        'finish_transaction': u'Swap done!',
        'talk': u'Talk to the group',
        'reply': u'Reply to all',
        'trades': u'See my trades',
        'stickers': u'See stickers I have',
        'add_sticker': u'Add a sticker I have',
        'wishlist': u'See stickers I need',
        'add_wishlist': u'Add a sticker I need'
    },
    'es': {
        'welcome': u'¡Hola {first_name}! Estoy para ayudarte a encontrar gente para cambiar figus y completar tu álbum.',
        'roger': u'Entendido! {first_name}',
        'menu': u'Elegí una de las siguientes opciones',
        'default': [u'No estoy seguro de entender', u'Todavía estoy aprendiendo', u'Perdón pero creo que no entendí'],
        'hi': [u'Hola {first_name}', u'Hola hola {first_name}', u'Buenas! {first_name}'],
        'wanted_changed': u'¡Buenísimo! Cambiamos las figuritas que querés',
        'collection_changed': u'¡Bárbaro! Cambiamos las figuritas que querés',
        'no_trades': [
            u'No tienes ningún cambio', u'Nada que mostrar en tus cambios'
        ],
        'no_stickers': [
            u'No tienes ninguna figurita',
            u'No hay figuritas que mostrar en tu colección',
            u'Tu colección está vacia'
        ],
        'no_wishlist': [
            u'No tienes figuritas que quieras',
            u'No hay figuritas en tu lista de deseos',
            u'Tu lista de deseos está vacia'
        ],
        'new_transaction': [
            u'Encontramos un nuevo intercambio!',
            u'Tienes una nueva oportunidad de intercambio!'
            u'Prepárate, un nuevo intercambio está en camino'
        ],
        'transaction_line_from_you': [
            u'Tú le darías {card} a {name_to}',
            u'Tú tienes {card}, que iría para {name_to}',
            u'{card} iría de ti a {name_to}'
        ],
        'transaction_line_to_you': [
            u'{name_from} te va a dar {card} a ti',
            u'{name_from} tiene {card}, que va a ir para ti',
            u'{card} va a ir de {name_from} a ti'
        ],
        'transaction_line': [
            u'{name_from} le va a dar {card} a {name_to}',
            u'{name_from} tiene {card}, que va a ir para {name_to}',
            u'{card} va a ir de {name_from} a {name_to}'
        ],
        'transaction_cta': u'Habla con ellos para arreglar cuando juntarse',
        'transaction_finished': u'La transacción ha sido finalizada',
        'transaction_canceled': u'La transacción ha sido canceleda',
        'ask_sticker': [
            u'¿Cuál? Dime el número, o una foto',
            u'Mándame un número o una foto y la agrego a tu colección'
        ],
        'ask_wishlist': [
            u'¿Cuál? Dime el número o una foto',
            u'Mándame un número o una foto y la agrego a tu lista de deseos'
        ],
        'ask_message': [
            u'¿Qué quieres decirle a este grupo?',
            u'Dame tu mensaje y lo reenviaré al grupo',
            u'¿Cuál es tu mensaje para el grupo?'
        ],
        'cta': [
            u'¿Cómo seguimos?',
            u'¿Con qué más te ayudo?',
            u'¿Qué otra cosa puedo hacer por ti?'],
        'message_sent': [
            u'Genial, ya enviamos tu mensaje',
            u'Listo, tu mensaje ya fue reenviado',
            u'Ya transmitimos tu mensaje'
        ],
        'message_received': u'{first_name} dice:',
        # This are "menu" items, it makes sense to have only one option
        'trade': u'Cambiar {card_put} por {card_get}',
        'remove_sticker': u'Ya no la tengo',
        'remove_wishlist': u'Ya no la quiero',
        'cancel_transaction': u'Cancelarla',
        'finish_transaction': u'Intercambio hecho!',
        'talk': u'Hablar con el grupo',
        'reply': u'Reponder a todos',
        'trades': u'Ver mis cambios',
        'stickers': u'Figuritas que tengo',
        'add_sticker': u'Poner figu que tengo',
        'wishlist': u'Figuritas que quiero',
        'add_wishlist': u'Poner figu que busco'
    }
}


def get_texts(user):
    lang = 'en'
    if 'locale' in user:
        lang = user['locale'].lower()[:2]
    if lang not in langs:
        lang = 'en'

    def get_text(key, **params):
        params.update(user)
        # print 'Getting text ' + key, params
        text = langs[lang][key]
        if type(text) == list:
            text = random.choice(text)
        return text.format(**params)

    return get_text

curl -X POST -H "Content-Type: application/json" -d '{
  "greeting": [
    {
      "locale": "default",
      "text": "This is the right spot to get together with other collectors and find your missing sticker to complete the album"
    },
    {
      "locale": "es_LA",
      "text": "Este es el lugar para juntarse con otros coleccionistas y completar el album del mundial"
    },
    {
      "locale": "es_ES",
      "text": "Este es el lugar para juntarse con otros coleccionistas y completar el album del mundial"
    }
  ],
  "get_started": {
    "payload": "/start"
  },
  "persistent_menu": [
    {
      "locale": "default",
      "call_to_actions": [
        {
          "title": "My trades",
          "type": "postback",
          "payload": "/trades"
        },
        {
          "title": "Stickers I have",
          "type": "postback",
          "payload": "/stickers"
        },
        {
          "title": "Stickers I need",
          "type": "postback",
          "payload": "/wishlist"
        }
      ]
    },
    {
      "locale": "es_LA",
      "call_to_actions": [
        {
          "title": "Mis cambios",
          "type": "postback",
          "payload": "/trades"
        },
        {
          "title": "Figuritas que tengo",
          "type": "postback",
          "payload": "/stickers"
        },
        {
          "title": "Figuritas que quiero",
          "type": "postback",
          "payload": "/wishlist"
        }
      ]
    },
    {
      "locale": "es_ES",
      "call_to_actions": [
        {
          "title": "Mis cambios",
          "type": "postback",
          "payload": "/trades"
        },
        {
          "title": "Figuritas que tengo",
          "type": "postback",
          "payload": "/stickers"
        },
        {
          "title": "Figuritas que quiero",
          "type": "postback",
          "payload": "/wishlist"
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v3.0/me/messenger_profile?access_token=$PAGE_ACCESS_TOKEN"
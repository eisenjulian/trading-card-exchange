curl -X POST -H "Content-Type: application/json" -d '{
  "greeting": [
    {
      "locale": "default",
      "text": "This is the right spot to get together with other collectors and find your missing sticker to complete the album"
    },
    {
      "locale": "es_LA",
      "text": "Este es el lugar para juntarse con otros coleccionistas y completar el álbum"
    },
    {
      "locale": "es_ES",
      "text": "Este es el lugar para juntarse con otros coleccionistas y completar el álbum"
    }
  ],
  "get_started": {
    "payload": "{\"intent\": \"start\"}"
  },
  "persistent_menu": [
    {
      "locale": "default",
      "call_to_actions": [
        {
          "title": "My trades",
          "type": "postback",
          "payload": "{\"intent\": \"trades\"}"
        },
        {
          "title": "Stickers I have",
          "type": "postback",
          "payload": "{\"intent\": \"stickers\"}"
        },
        {
          "title": "Stickers I need",
          "type": "postback",
          "payload": "{\"intent\": \"wishlist\"}"
        }
      ]
    },
    {
      "locale": "es_LA",
      "call_to_actions": [
        {
          "title": "Mis cambios",
          "type": "postback",
          "payload": "{\"intent\": \"trades\"}"
        },
        {
          "title": "Figuritas que tengo",
          "type": "postback",
          "payload": "{\"intent\": \"stickers\"}"
        },
        {
          "title": "Figuritas que quiero",
          "type": "postback",
          "payload": "{\"intent\": \"wishlist\"}"
        }
      ]
    },
    {
      "locale": "es_ES",
      "call_to_actions": [
        {
          "title": "Mis cambios",
          "type": "postback",
          "payload": "{\"intent\": \"trades\"}"
        },
        {
          "title": "Figuritas que tengo",
          "type": "postback",
          "payload": "{\"intent\": \"stickers\"}"
        },
        {
          "title": "Figuritas que quiero",
          "type": "postback",
          "payload": "{\"intent\": \"wishlist\"}"
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v3.0/me/messenger_profile?access_token=$PAGE_ACCESS_TOKEN"
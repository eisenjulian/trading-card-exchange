# Swapr

This is a messenger bot for aiding trading communities. The first version specializes in trading world cup collectible cards.

## What can I do?

There are two set of cards associated to each user: the wanted cards and the collection.
Cards can be added or removed to both sets by users, either by their names or by a picture.
We use image recognition to identify cards from images.

Once enough users have input their cards we run a matching algorithm to identify groups of people that can trade together.
We do more than the clasic 1 to 1 trade. For example we could have the following situation:

| User          | Wants   | Has   |
|:-------------:|:-------:|:-----:|
| A             | 1       | 2     |
| B             | 2       | 3     |
| C             | 3       | 1     |

Any 1 to 1 trade here would not be convinient for one of the users but if the three of them get together they all can be
happy.

An user can be part of many trading circles. That's why we have the concept of transaction. The bot will show each user
their active transactions. The user only sees which card has to give in and which card has to leave when running the trade.
Users can confirm or cancel a transaction. If any user cancels the transaction, it becomes obsolete and then we would cancel it
for all users. If all users confirm the transaction, then we mark it as done and we move on to find more transactions.

The bot is available in English and Spanish.

## How does it work?

We store all the information in redis. For each user, card and transaction we have a key 'object:id' with a json containing
all the information related to that object.
Given the information about the users and the cards we can create a bipartite directed graph with vertex set.
There is an edge from an user to a card when the user posseses the card and there is an edge from a card to an user
when the user wants the card. Cycles in this graph represent trading opportunities.
We use networkx to represent graphs and also to compute the cycles.

## Testing
Please reach out to @eisenjulian or @quimey

## Contributing
Please reach out to @eisenjulian or @quimey

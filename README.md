# streamlabs_auction

### this scripts adds the auction system to your streamlabs chatbot.
The available default commands are:
* !startBid {(opt)MinimumBiddingPrice} {(opt)ForXSeconds} (Caster only)
* !stopBid (Caster only)
* !bid {number}

Open an auction with !startBid. Witout parameter, the auction will be opend until default time (config).

The users can now bid until the end of the auction game. The one with the highest bid wins.

To prevent that every user takes a bid in the last 5 seconds, the game will be setted in the last 10 seconds (can be changes in config) to 10 seconds.

The plugin does have a full UI Setting support and is full customable.

Have fun :)


### Changelog

* v1.0.0 Major Release
<<<<<<< Updated upstream
=======
* v1.1.0 Add minimum bidding price at start and minimum bid increase
>>>>>>> Stashed changes

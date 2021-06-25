## A variant on the Blotto game

This project explores the following variant on the traditional Blotto game:

> 10 castles numbered 1 to 10 are worth 1, 2, 3 ... 10 points respectively. We are given 100 soldiers to allocate between the castles. Our opponent independently does the same. Castles are fought in order from 1 to 10. The number of soldiers on each castle is then compared, and for each castle, whoever has the most soldiers on that castle wins its points (no points in case of a tie). If a player wins 3 consecutive castles, they automatically win all the remaining Castles too.

I approach this from the standpoint of maximising point-profits against a theoretical large set of players. Strategies against a small number of players (where one can afford riskier play), or to maximise wins rather than points, are discussed briefly too. There is no dominant 'good answer' to this game, so my conclusions and indeed modelling choices are subjective. I tried to stick with what I felt would be sensible strategies from intelligent players. 

A collection of data was modelled in Python using beta-binomial distributions with varying parameters, selected by hand; the results are tweaked/skewed, also by hand, to better model what I would perceive to be more 'human' strategies. Indeed with only 10 castles, most probability distributions will produce arrangements that are too conservative or unwise; as a result, I chose to emphasise certain castles after generating samples by uniformly reallocating numbers too large or small to more sensible ranges.

This data is then played played against itself (as well as a 'noise' data set), and winners are produced at the end.

--------
A discussion behind the motivations and strategies I employed, as well as results, can be found in the [PDF game report](game-report.pdf).

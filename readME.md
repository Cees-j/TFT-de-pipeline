API key is set as environment variable
Run order is get_chall, get_puuid, get_match

api rate limit is 20 per sec, 100 per 2 min, per region, (e.g na1, euw1, americas)

Get_chall -> Get_puuid -> Get_match, thats pretty much extracting it done, then need to acutally make some tables within, with is the transform part..
Need to design a scheme i want, once i have that should be pretty simple to transform it and that.

For each player, get their match history, and then for each match in their match history take all that data

need to remove "items" from match df, gives id of items, remove name aswell, dead field
# Here are some example queries that could be run against the schema.

## Find the total damage dealt to players in a particular match:
SELECT sum(total_damage_to_players)
FROM game_results
WHERE match_id = <match_id>;


## Find the most commonly used trait for each player:
SELECT participant_id, trait_name
FROM traits_data
WHERE match_id = <match_id>
GROUP BY participant_id
ORDER BY count(*) DESC
LIMIT 1;


## Find the most popular 5-Cost unit in each match:
SELECT match_id, unit_id
FROM units_per_player_and_match
WHERE rarity = '5-Cost'
GROUP BY match_id, unit_id
ORDER BY count(*) DESC
LIMIT 1;


## Find the average gold left for players who placed in the top 3 in each match:
SELECT match_id, avg(gold_left)
FROM game_results
WHERE placement <= 3
GROUP BY match_id;


## Find the most common combination of traits for players who placed in the top 4 in each match:
SELECT match_id, style, count(*) as num_players
FROM traits_data
WHERE participant_id IN (
    SELECT participant_id
    FROM game_results
    WHERE placement <= 4
)
GROUP BY match_id, style
ORDER BY num_players DESC
LIMIT 1;


## Find the players who used the same unit as a particular player in a particular match:
SELECT DISTINCT p.participant_id
FROM units_per_player_and_match p
WHERE p.match_id = <match_id>
AND p.unit_id IN (
    SELECT unit_id
    FROM units_per_player_and_match
    WHERE match_id = <match_id> AND participant_id = <participant_id>
    GROUP BY unit_id
    HAVING COUNT(*) > 1
)
AND p.participant_id != <participant_id>;


## Find the top 3 players in terms of total damage dealt to players, along with their placement in each match:
SELECT match_id, placement, participant_id, total_damage_to_players,
  RANK() OVER (PARTITION BY match_id ORDER BY total_damage_to_players DESC) AS rank
FROM game_results
WHERE placement <= 3
ORDER BY match_id, rank;




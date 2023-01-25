CREATE TABLE global (id int, name varchar(255), picks int, wins int, winrate float);
CREATE TABLE my (id int, picks int, wins int, winrate float);
INSERT INTO global VALUES (%s, %s, %s, %s, %s);
INSERT INTO my VALUES (%s, %s, %s, %s);
CREATE TABLE dotanomaly AS (
SELECT my.id, global.name AS hero_name, my.picks AS games, my.winrate AS my_winrate, global.winrate AS global_winrate
FROM my
INNER JOIN global
ON my.id = global.id
WHERE my.picks > 2
ORDER BY my.winrate-global.winrate DESC);
CREATE TABLE dotanomaly%s SELECT * FROM dotanomaly;
CREATE TABLE global%s SELECT * FROM global;
CREATE TABLE my%s SELECT * FROM my;
DROP TABLE my;
DROP TABLE global;
DROP TABLE dotanomaly;

--SELECT table_name FROM information_schema.tables where table_schema='dota';
--SELECT table_name FROM information_schema.tables where table_schema='dota' order by update_time desc limit 3;
SELECT table_name FROM information_schema.tables where table_schema='dota' and table_name REGEXP '^d' order by update_time desc limit 3; 
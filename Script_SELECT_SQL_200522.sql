SELECT album_name, release_year FROM album_list
	WHERE release_year = 2018;

SELECT track_name, track_time FROM track_list
	WHERE track_time = (SELECT MAX(track_time) FROM track_list);
	
SELECT track_name, track_time FROM track_list
	WHERE track_time >= 210;
	
SELECT collection_name, collection_year FROM collection
	WHERE collection_year BETWEEN 2018 AND 2020;

SELECT singer_name FROM singer_list
	WHERE singer_name NOT LIKE '%% %%';

SELECT track_name FROM track_list
	WHERE track_name LIKE '%%My%%' 
	OR track_name LIKE '%%my%%'
	OR track_name LIKE '%%Мой%%'
	OR track_name LIKE '%%мой%%'; 
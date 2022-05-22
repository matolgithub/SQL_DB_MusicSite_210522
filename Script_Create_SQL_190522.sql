CREATE TABLE IF NOT EXISTS style_list (
	id SERIAL PRIMARY KEY,
	style_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS singer_list (
	id SERIAL PRIMARY KEY,
	singer_name VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS style_singer (
	id SERIAL PRIMARY KEY,
	style_id INTEGER NOT NULL REFERENCES style_list(id),
	singer_id INTEGER NOT NULL REFERENCES singer_list(id)
);

CREATE TABLE IF NOT EXISTS album_list (
	id SERIAL PRIMARY KEY,
	album_name VARCHAR(40) NOT NULL,
	release_year INTEGER CHECK(release_year>=1900 AND release_year<=2022)
);

CREATE TABLE IF NOT EXISTS singer_album (
	id SERIAL PRIMARY KEY,
	album_id INTEGER NOT NULL REFERENCES album_list(id),
	singer_id INTEGER NOT NULL REFERENCES singer_list(id)
);

CREATE TABLE IF NOT EXISTS track_list (
	id SERIAL PRIMARY KEY,
	track_name VARCHAR(40) NOT NULL,
	track_time INTEGER CHECK(track_time>0 AND track_time<=3600),
	album_id INTEGER REFERENCES album_list(id)
);

CREATE TABLE IF NOT EXISTS collection (
	id SERIAL PRIMARY KEY,
	collection_name VARCHAR(40) NOT NULL,
	collection_year INTEGER CHECK(collection_year>=1900 AND collection_year<=2022)
);

CREATE TABLE IF NOT EXISTS collection_track (
	id SERIAL PRIMARY KEY,
	collection_id INTEGER NOT NULL REFERENCES collection(id),
	track_id INTEGER NOT NULL REFERENCES track_list(id)
);
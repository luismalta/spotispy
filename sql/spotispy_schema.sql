CREATE schema spotispy;

CREATE TABLE IF NOT EXISTS spotispy.playback_history  (
    datetime timestamp NOT NULL,
    track_id varchar NOT NULL,
    device_id varchar NOT NULL,
    PRIMARY KEY (datetime, track_id)
);

CREATE TABLE IF NOT EXISTS spotispy.track_artists (
    track_id varchar NOT NULL,
    artist_id varchar NOT NULL,
    PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE IF NOT EXISTS spotispy.album_artists (
    album_id varchar NOT NULL,
    artist_id varchar NOT NULL,
    PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS spotispy.tracks (
    track_id varchar PRIMARY KEY,
    artist_id varchar NOT NULL,
    album_id varchar NOT NULL,
    name varchar NOT NULL,
    track_number int NOT NULL,
    uri varchar NOT NULL,
    duration int NOT NULL,
    explicit boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS spotispy.artists (
    artist_id varchar PRIMARY KEY,
    name varchar NOT NULL,
    type varchar NOT NULL,
    uri varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS spotispy.albums (
    album_id varchar PRIMARY KEY,
    name varchar NOT NULL,
    uri varchar NOT NULL,
    album_type varchar NOT NULL,
    release_date date NOT NULL,
    total_tracks int NOT NULL
);

CREATE TABLE IF NOT EXISTS spotispy.devices (
    device_id varchar PRIMARY KEY,
    is_private_session boolean NOT NULL,
    name varchar NOT NULL,
    type varchar NOT NULL,
    volume_percent int NOT NULL
);

create table albums(
    id varchar primary key,
    name varchar,
    release_date timestamp,
    total_tracks integer
);

create table tracks(
    id varchar primary key,
    name varchar,
    is_explicit boolean,
    duration_ms integer,
    album_id varchar references albums(id)
);

create table artists(
    id varchar primary key,
    name varchar
);

create table devices(
    id varchar primary key,
    name varchar,
    device_type varchar
);

create table tracks_artists(
    track_id varchar references tracks(id),
    artist_id varchar references artists(id),
    PRIMARY KEY (track_id, artist_id)
);

create table tracks_albums(
    track_id varchar references tracks(id),
    album_id varchar references albums(id),
    PRIMARY KEY (track_id, album_id)
);

create table playback_history(
    track_id varchar references tracks(id),
    device_id varchar,
    playback_datetime timestamp,
    PRIMARY KEY (track_id, playback_datetime)
);
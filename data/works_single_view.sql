DROP DATABASE IF EXISTS works_single_view;

CREATE DATABASE works_single_view;

\c works_single_view 

DROP TABLE IF EXISTS song_metadata;

CREATE TABLE song_metadata(
    id serial  PRIMARY KEY,
    title VARCHAR(200),
    contributors TEXT[],
    iswc VARCHAR(11) UNIQUE,
    sources TEXT[],
    source_ids INT[]
);


-- migrate:up
create table if not exists deck (
    deck_id integer primary key autoincrement,
    deck_name text not null,
    left_name text,
    right_name text
);

-- migrate:down
drop table deck;


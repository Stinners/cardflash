-- migrate:up
create table if not exists tag(
    tag_id integer primary key autoincrement,
    tag_name text not null,
    deck_id integer,
    foreign key(deck_id) references deck(deck_id)
);


-- migrate:down
drop table tag;


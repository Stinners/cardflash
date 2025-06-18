-- migrate:up
create table if not exists card_tag(
    card_tag_id integer primary key autoincrement,
    card_id integer,
    tag_id integer,
    foreign key(card_id) references card(card_id),
    foreign key(tag_id) references card(tag_id)
);


-- migrate:down
drop table card_tag;


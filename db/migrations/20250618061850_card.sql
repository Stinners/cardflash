-- migrate:up
create table if not exists card (
    card_id integer primary key autoincrement,
    left text not null,
    right text not null,
    direction integer not null 
        check(direction>=0 and direction<=2),
    deck_id integer not null,
    foreign key(deck_id) references deck(deck_id)
);


-- migrate:down
drop table card;


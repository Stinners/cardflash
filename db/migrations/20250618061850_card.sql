-- migrate:up
create table if not exists card (
    deck_id integer primary key autoincrement,
    left text not null,
    right text not null,
    direction integer not null 
        check(direction>=0 and direction<=2) 
);


-- migrate:down
drop table card;


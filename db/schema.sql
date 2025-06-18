CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE deck (
    deck_id integer primary key autoincrement,
    deck_name text not null,
    left_name text,
    right_name text
);
CREATE TABLE card (
    deck_id integer primary key autoincrement,
    left text not null,
    right text not null,
    direction integer not null
        check(direction>=0 and direction<=2)
);
CREATE TABLE tag(
    tag_id integer primary key autoincrement,
    tag_name text not null,
    deck_id integer,
    foreign key(deck_id) references deck(deck_id)
);
CREATE TABLE card_tag(
    card_tag_id integer primary key autoincrement,
    card_id integer,
    tag_id integer,
    foreign key(card_id) references card(card_id),
    foreign key(tag_id) references card(tag_id)
);
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20250618061427'),
  ('20250618061850'),
  ('20250618062230'),
  ('20250618062455');

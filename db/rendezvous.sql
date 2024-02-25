create table rendezvous (
  id integer primary key,
  user_id integer,
  nom varchar(25),
  num_tattoo integer,
  mois integer,
  jour integer,
  description varchar(500),
  depot numeric,
  prix_total numeric,
  taxes_dues numeric,
  tip numeric
);

create table users (
  user_id integer primary key,
  username varchar(25),
  password varchar(25)
);

insert into users values (1, 'elo', 'caddierory');
insert into rendezvous values (1, 1, 'Eloïse', 2, 1, 25, 'Gentille, talentueuse, belle', 70, 300, 33, 20);



create table rendezvous (
  id integer primary key,
  user_id integer,
  nom varchar(25),
  num_tattoo integer,
  jour integer,
  mois integer,
  annee integer,
  depot numeric,
  prix_total numeric,
  type_paiement varchar(10),
  tip numeric,
  pistache integer
);

create table users (
  user_id integer primary key,
  username varchar(25),
  password varchar(25)
);

insert into users values (1, 'elo', 'caddierory');
insert into rendezvous values (1, 1, 'Eloïse', 2, 11, 1, 2024, 70, 150000, "interac", 20, 0);



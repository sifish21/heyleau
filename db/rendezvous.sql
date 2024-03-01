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
insert into rendezvous values (1, 1, 'Eloïse', 2, 11, 1, 2024, 70, 300, "interac", 20, 0);
insert into rendezvous values (2, 1, 'Maya', 2, 12, 1, 2024, 70, 300, "visa", 20, 0);
insert into rendezvous values (3, 1, 'Caddie', 2, 13, 2, 2024, 70, 300, "cash", 20, 1);



create table rendezvous (
  id integer primary key,
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

insert into rendezvous values (1, 'Eloïse', 2, 1, 25, 'Gentille, talentueuse, belle', 70, 300, 33, 20);



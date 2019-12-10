delete from Role;
delete from Person;
delete from Movie;
delete from TVSeries;



/* Movie */

insert into Movie (title,year,rating) values ('American Beauty', 1999, 'r');
insert into Movie (title,year,rating) values ('American Pie', 1999, 'r');


/* Person */

insert into Person (videoClassId,videoObjId,name,birthDate) values (1,1, 'Paul Weitz', '1/1/1966');
insert into Person (videoClassId,videoObjId,name,birthDate) values (1,2, 'Sam Mendes', '9/1/1965');
insert into Person (videoClassId,videoObjId,name,birthDate) values (1,null, 'Kevin Spacey', '7/26/1959');
insert into Person (videoClassId,videoObjId,name,birthDate) values (1,null, 'Mena Suvari', '2/9/1979');
insert into Person (videoClassId,videoObjId,name,birthDate) values (1,null, 'Jason Biggs', '5/12/1978');
insert into Person (videoClassId,videoObjId,name,birthDate) values (1,null, 'Shannon Elizabeth', '9/7/1976');


/* Role */

insert into Role (videoClassId,videoObjId,karacter,personClassId,personObjId) values (1,1, 'Lester Burnham', 4,3);
insert into Role (videoClassId,videoObjId,karacter,personClassId,personObjId) values (1,1, 'Angela Hayes', 4,4);
insert into Role (videoClassId,videoObjId,karacter,personClassId,personObjId) values (1,2, 'Jim', 4,5);
insert into Role (videoClassId,videoObjId,karacter,personClassId,personObjId) values (1,2, 'Heather', 4,4);
insert into Role (videoClassId,videoObjId,karacter,personClassId,personObjId) values (1,2, 'Nadia', 4,5);

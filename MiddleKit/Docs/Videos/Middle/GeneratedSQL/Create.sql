/*
Start of generated SQL.

# Date         = Thu Dec  5 06:30:42 2019
# Python ver   = 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)]
# Op Sys       = nt
# Platform     = win32
# Cur dir      = C:\Python38\Lib\site-packages\MiddleKit\Docs\Videos\Middle
# Num classes  = 5

Classes:
    Video
    Movie
    TVSeries
    Person
    Role
*/

drop table if exists _MKClassIds;
drop table if exists Role;
drop table if exists Person;
drop table if exists TVSeries;
drop table if exists Movie;
drop table if exists Video;

create table _MKClassIds (
id int not null primary key,
name varchar(100)
);
insert into _MKClassIds (id, name) values     (1, 'Video');
insert into _MKClassIds (id, name) values     (2, 'Movie');
insert into _MKClassIds (id, name) values     (3, 'TVSeries');
insert into _MKClassIds (id, name) values     (4, 'Person');
insert into _MKClassIds (id, name) values     (5, 'Role');

create table Movie (
    serialNum                      integer primary key autoincrement,
    title                          text not null,
    year                           int not null,
    rating                         varchar(5) not null    /* directors list of Person - not a SQL column */
    /* cast list of Role - not a SQL column */
);


create table TVSeries (
    serialNum                      integer primary key autoincrement,
    title                          text not null,
    years                          int    /* directors list of Person - not a SQL column */
    /* cast list of Role - not a SQL column */
);


create table Person (
    serialNum                      integer primary key autoincrement,
    videoClassId                   integer /* Video */ default 1 references _MKClassIds , /* Video */ 
    videoObjId                     integer /* Video */,
    name                           text not null,
    birthDate                      date);


create table Role (
    serialNum                      integer primary key autoincrement,
    videoClassId                   integer /* Video */ default 1 not null references _MKClassIds , /* Video */ 
    videoObjId                     integer /* Video */ not null,
    karacter                       text not null,
    personClassId                  integer /* Person */ default 4 not null references _MKClassIds , /* Person */ 
    personObjId                    integer /* Person */ not null);


/* end of generated SQL */

/*
Start of generated SQL.

# Date         = Wed Nov 20 16:47:31 2019
# Python ver   = 3.6.9 (default, Oct 29 2019, 10:39:36) [GCC]
# Op Sys       = posix
# Platform     = linux
# Cur dir      = /home/nico/Downloads/w4py3-master/webware/MiddleKit/Docs/Videos
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

create table TVSeries (
    serialNum                      integer primary key autoincrement,
    title                          text not null,
    years                          int    /* directors list of Person - not a SQL column */
    /* cast list of Role - not a SQL column */
);


create table Movie (
    serialNum                      integer primary key autoincrement,
    title                          text not null,
    year                           int not null,
    rating                         varchar(5) not null    /* directors list of Person - not a SQL column */
    /* cast list of Role - not a SQL column */
);


create table Person (
    serialNum                      integer primary key autoincrement,
    videoClassId                   integer /* Video */ default 1 references _MKClassIds, /* Video */ 
    videoObjId                     integer /* Video */,
    name                           text not null,
    birthDate                      date);


create table Role (
    serialNum                      integer primary key autoincrement,
    videoClassId                   integer /* Video */ not null default 1 references _MKClassIds, /* Video */ 
    videoObjId                     integer /* Video */ not null,
    karacter                       text not null,
    personClassId                  integer /* Person */ not null default 4 references _MKClassIds, /* Person */ 
    personObjId                    integer /* Person */ not null);


/* end of generated SQL */

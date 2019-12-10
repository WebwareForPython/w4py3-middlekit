/*
Start of generated SQL.

# Date         = Tue Dec 10 08:22:10 2019
# Python ver   = 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Op Sys       = nt
# Platform     = win32
# Cur dir      = C:\Python38\Lib\site-packages\MiddleKit\Tests
# Num classes  = 2

Classes:
    Thing
    Person
    Dummy
    Foo
*/

use Master
go
if exists(select * from master.dbo.sysdatabases where name = N'MKModelInh3') drop database MKModelInh3;
go 
Use Master
go

if not exists(select * from master.dbo.sysdatabases where name = N'MKModelInh3') create database MKModelInh3;
go 
USE MKModelInh3;


if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[_MKClassIds]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[_MKClassIds]
go

create table _MKClassIds (
id int not null primary key,
name varchar(100)
)
go
delete from _MKClassIds

insert into _MKClassIds (id, name) values (1, 'Thing');
insert into _MKClassIds (id, name) values (4, 'Foo');

go

create table [Person] (
        serialNum                      int constraint [PK__Person__serialNum] primary key not null identity(1, 1),
    [id]                           varchar(32) null,
    [firstName]                    varchar(50) null,
    [middleName]                   varchar(50) null,
    [lastName]                     varchar(50) null);



create table [Dummy] (
        serialNum                      int constraint [PK__Dummy__serialNum] primary key not null identity(1, 1),
    [x]                            int null);



create table [Thing] (
        serialNum                      int constraint [PK__Thing__serialNum] primary key not null identity(1, 1),
    [a]                            varchar(100) /* WARNING: NO LENGTH SPECIFIED */ null,
    [b]                            varchar(100) /* WARNING: NO LENGTH SPECIFIED */ null);



create table [Foo] (
        serialNum                      int constraint [PK__Foo__serialNum] primary key not null identity(1, 1),
    [a]                            varchar(100) /* WARNING: NO LENGTH SPECIFIED */ null,
    [b]                            varchar(100) /* WARNING: NO LENGTH SPECIFIED */ null,
    [x]                            int null);



/* end of generated SQL */

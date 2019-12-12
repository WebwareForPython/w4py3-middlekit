/*
Start of generated SQL.

# Date         = Tue Dec 10 09:33:14 2019
# Python ver   = 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Op Sys       = nt
# Platform     = win32
# Cur dir      = C:\Users\nico\Documents\GitHub\w4py3-middlekit\MiddleKit\Tests
# Num classes  = 2

Classes:
    Foo
    Bar
*/

use Master
go
if exists(select * from master.dbo.sysdatabases where name = N'MKTypeValueChecking') drop database MKTypeValueChecking;
go 
Use Master
go

if not exists(select * from master.dbo.sysdatabases where name = N'MKTypeValueChecking') create database MKTypeValueChecking;
go 
USE MKTypeValueChecking;


if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[_MKClassIds]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[_MKClassIds]
go

create table _MKClassIds (
id int not null primary key,
name varchar(100)
)
go
delete from _MKClassIds

insert into _MKClassIds (id, name) values (1, 'Foo');
insert into _MKClassIds (id, name) values (2, 'Bar');

go

create table [Bar] (
        serialNum                      int constraint [PK__Bar__serialNum] primary key not null identity(1, 1),
    [x]                            int null,
    [y]                            int null);



create table [Foo] (
        serialNum                      int constraint [PK__Foo__serialNum] primary key not null identity(1, 1),
    [b]                            bit null,
    [i]                            int null,
    [l]                            bigint null,
    [f]                            float null,
    [s]                            varchar(100) null,
    [d]                            DateTime null,
    [t]                            DateTime null,
    [dt]                           DateTime null,
    [e]                            varchar(1) null,
    barClassId                     int default 2 null constraint [FK__Foo__barClassId___MKClassIds__id] references _MKClassIds, /* Bar */ 
    barObjId                       int null);



/* end of generated SQL */

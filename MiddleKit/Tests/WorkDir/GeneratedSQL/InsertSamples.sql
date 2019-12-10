use MKModelInh3;

delete from [Foo];
delete from [Thing];
delete from [Dummy];
delete from [Person];

go
go


/* Thing */

insert into [Thing] ([a],[b]) values ('adsf', 'qwer');
insert into [Thing] ([a],[b]) values ('zxcv', 'adsf');
go


/* Foo */

insert into [Foo] ([a],[b],[x]) values ('a', 'b', 0);
insert into [Foo] ([a],[b],[x]) values ('a', 'b', 1);
insert into [Foo] ([a],[b],[x]) values ('asdf', 'qwer', 45);
go

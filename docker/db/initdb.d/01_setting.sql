CREATE TABLE ranks(
    id int,
    rank_name varchar(30),
    point int,
    init_point int,
    pre_rank_id int,
    next_rank_id int,
    primary key (id)
);


insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (10,'初心',200,0, -1,20);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (20,'雀士',600,300,10,21);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (21,'雀士2',800,400,20,22);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (22,'雀士3',1000,500,21,30);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (30,'雀傑',2000,1000,22,40);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (40,'雀鬼',3000,1500,30,50);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (50,'雀聖',4000,2000,40,60);
insert into ranks (id,rank_name,point,init_point, pre_rank_id,next_rank_id) values (60,'雀神',20000000,10000000,50,-1);


delete from rareapi_comment
where id = 4
delete from rareapi_postreaction
where id >1

update rareapi_post
set user_id = 2
where id in (5,6,7);

INSERT INTO rareapi_comment (created_on, content, author_id, post_id)
VALUES ('2020-01-05', 'SQL comment', 2, 1)

insert into rareapi_post_tags (post_id, tag_id)
values (1,1);
insert into rareapi_post_tags (post_id, tag_id)
values (2,3);
insert into rareapi_post_tags (post_id, tag_id)
values (3,5);
insert into rareapi_post_tags (post_id, tag_id)
values (4,4);
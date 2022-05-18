delete from auth_user
where id = 3
delete from rareapi_postreaction
where id > 1

UPDATE rareapi_rareuser
SET active = 0
WHERE id = 1

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
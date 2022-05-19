delete from auth_user
where id = 3
delete from rareapi_comment
where id = 10

UPDATE rareapi_rareuser
SET active = 0
WHERE id = 1

INSERT INTO rareapi_rareuser (bio, profile_image_url, active, user_id, created_on)
VALUES ('Grilling, with propane of course.', 'http://www.placeholder.com', 1, 4, '2022-05-17')

insert into rareapi_post_tags (post_id, tag_id)
values (1,1);
insert into rareapi_post_tags (post_id, tag_id)
values (2,3);
insert into rareapi_post_tags (post_id, tag_id)
values (3,5);
insert into rareapi_post_tags (post_id, tag_id)
values (4,4);
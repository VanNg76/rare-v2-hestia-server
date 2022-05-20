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

insert into rareapi_subscription (created_on, ended_on, author_id, follower_id)
values ("2022-05-05", "2022-06-06", 1,2);
insert into rareapi_subscription (created_on, ended_on, author_id, follower_id)
values ("2022-08-08", "2022-09-09", 2,1);
insert into rareapi_subscription (created_on, ended_on, author_id, follower_id)
values ("2022-07-07", "2022-06-09", 1,3);
insert into rareapi_subscription (created_on, ended_on, author_id, follower_id)
values ("2022-09-09", "2022-10-10", 2,4);
insert into rareapi_subscription (created_on, ended_on, author_id, follower_id)
values ("2022-05-10", "2022-06-11", 4,1);

delete from rareapi_subscription
where id = 9
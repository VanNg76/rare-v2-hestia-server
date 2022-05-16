delete from rareapi_postreaction
where id >1

update auth_user
set is_staff = 1
where id =1
INSERT INTO rareapi_comment (created_on, content, author_id, post_id)
VALUES ('2020-01-05', 'SQL comment', 2, 1)

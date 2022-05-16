delete from rareapi_postreaction
where id >1

update auth_user
set is_staff = 1
where id =1
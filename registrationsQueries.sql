SELECT id, first_name FROM users WHERE NOT (id = 1);

SELECT * FROM registrationsdb.users;

SELECT * FROM registrationsdb.messages;

SELECT * FROM registrationsdb.messages WHERE user_id = 1 ORDER BY id DESC LIMIT 5;

SELECT COUNT(user_id) FROM registrationsdb.messages WHERE user_id = 1;

SELECT COUNT(receiver_id) FROM registrationsdb.messages WHERE receiver_id = 2;

SELECT * FROM registrationsdb.messages WHERE receiver_id = 2 ORDER BY id DESC LIMIT 3;

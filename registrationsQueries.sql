-- Add user_level column for admin determination
USE registrationsdb;
SELECT * FROM users;
ALTER TABLE users ADD user_level SET('1','9');
UPDATE registrationsdb.users SET user_level = '1'
	WHERE id > 1;
UPDATE registrationsdb.users SET user_level = '9'
	WHERE id = 1;
SELECT * FROM registrationsdb.users;

---------------------------------------------------

SELECT id, first_name FROM users WHERE NOT (id = 1);

SELECT * FROM registrationsdb.users;

SELECT * FROM registrationsdb.messages;

SELECT * FROM registrationsdb.messages WHERE user_id = 1 ORDER BY id DESC LIMIT 5;

SELECT COUNT(user_id), COUNT FROM registrationsdb.messages WHERE user_id = 1;

SELECT COUNT(receiver_id) FROM registrationsdb.messages WHERE receiver_id = 2;

SELECT * FROM registrationsdb.messages WHERE receiver_id = 2 ORDER BY id DESC LIMIT 3;

SELECT user_id, content, created_at FROM messages WHERE receiver_id = 3;

-- getting received messages (not dynamic example)
SELECT user_id, first_name, content, messages.created_at, messages.id FROM messages, users WHERE receiver_id = 3 and user_id = users.id ORDER BY messages.id DESC LIMIT 5;

-- delete message
-- DELETE FROM messages WHERE id = request.form['messagesId'];
DELETE FROM messages WHERE id = 1; -- hard coding --

-- getting time difference example
SELECT TIMEDIFF(NOW(), messages.updated_at) FROM registrationsdb.messages WHERE id = 1;

SELECT MAX(id) FROM registrationsdb.users;


UPDATE registrationsdb.users SET last_name = 'firstUser'
	WHERE id = 1;




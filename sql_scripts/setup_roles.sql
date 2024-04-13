CREATE USER IF NOT EXISTS 'unprivileged'@'localhost' IDENTIFIED BY 'unprivileged_password';
CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'user_password';
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin_password';

CREATE ROLE IF NOT EXISTS 'app_read', 'app_write', 'app_admin';

GRANT SELECT ON quizmaker.* TO 'app_read'@'%';
GRANT INSERT, SELECT, UPDATE, DELETE ON quizmaker.* TO 'app_write'@'%';
GRANT ALL ON quizmaker.* TO 'app_admin'@'%';

GRANT 'app_read' to 'unprivileged'@'localhost';
GRANT 'app_write' to 'user'@'localhost';
GRANT 'app_admin' to 'admin'@'localhost';

SET DEFAULT ROLE 'app_read' TO 'unprivileged'@'localhost';
SET DEFAULT ROLE 'app_write' TO 'user'@'localhost';
SET DEFAULT ROLE 'app_admin' TO 'admin'@'localhost';
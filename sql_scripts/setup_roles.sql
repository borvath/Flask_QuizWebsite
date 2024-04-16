CREATE USER IF NOT EXISTS 'unprivileged'@'%' IDENTIFIED BY 'unprivileged_password';
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'user_password';
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin_password';

CREATE ROLE IF NOT EXISTS 'app_read', 'app_write', 'app_admin';

GRANT SELECT ON quizmaker.* TO 'app_read'@'%';
GRANT INSERT ON quizmaker.user TO 'app_read'@'%';
GRANT INSERT, SELECT, UPDATE, DELETE ON quizmaker.* TO 'app_write'@'%';
GRANT ALL ON quizmaker.* TO 'app_admin'@'%';

GRANT 'app_read' to 'unprivileged'@'%';
GRANT 'app_write' to 'user'@'%';
GRANT 'app_admin' to 'admin'@'%';

SET DEFAULT ROLE 'app_read' TO 'unprivileged'@'%';
SET DEFAULT ROLE 'app_write' TO 'user'@'%';
SET DEFAULT ROLE 'app_admin' TO 'admin'@'%';

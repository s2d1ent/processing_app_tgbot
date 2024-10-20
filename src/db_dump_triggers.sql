CREATE TRIGGER insert_mailling_group_after_company
AFTER INSERT ON Companys
FOR EACH ROW
BEGIN
    INSERT INTO MaillingGroups(name) VALUES(NEW.name);
    INSERT INTO MaillingGroups(name) VALUES(NEW.name || '_IT');
END;

CREATE TRIGGER delete_mailling_group_after_company
AFTER DELETE ON Companys
FOR EACH ROW
BEGIN
    DELETE FROM MaillingGroups
    WHERE name = OLD.name;

    DELETE FROM MaillingGroups
    WHERE name = OLD.name || '_IT';
END;

CREATE TRIGGER insert_mailling_group_after_deptocompanys
AFTER INSERT ON DepToCompanys
FOR EACH ROW
BEGIN
    INSERT INTO MaillingGroups (name)
    VALUES (
        (SELECT name FROM Companys WHERE id=NEW.company LIMIT 1) 
        || '_' || 
        (SELECT name FROM Departaments WHERE id=NEW.departament LIMIT 1));
END;

CREATE TRIGGER insert_mailling_users_after_users
AFTER INSERT ON Users
FOR EACH ROW
BEGIN
    INSERT INTO MaillingUsers(uid, group_id) 
    VALUES(NEW.id, 
        (SELECT id FROM MaillingGroups 
         WHERE name = (SELECT name FROM Companys WHERE id=NEW.company) LIMIT 1)
    );

    INSERT INTO MaillingUsers(uid, group_id) 
    VALUES(NEW.id, 
        (SELECT id FROM MaillingGroups 
         WHERE name = (SELECT name FROM Companys WHERE id=NEW.company) || '_' || 
                       (SELECT name FROM Departaments WHERE id=NEW.departament) LIMIT 1)
    );
END;
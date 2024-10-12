PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Status (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    text CHAR(100)
);
INSERT INTO Status VALUES(1,'Создано');
INSERT INTO Status VALUES(2,'Отменено');
INSERT INTO Status VALUES(3,'Выполняется');
INSERT INTO Status VALUES(4,'Завершено');
CREATE TABLE IF NOT EXISTS "Users"(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100),
    tg_id CHAR(100) NULL UNIQUE,
    is_admin INTEGER DEFAULT 0);

CREATE TABLE Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date DATE NULL,                
    finishDate DATE NULL,            
    creater CHAR(100) NULL,            
    receiver CHAR(100) NULL,              
    status INTEGER NULL,                
    createrComment CHAR(500),
    receiverComment CHAR(500), 
    thema CHAR(100) NULL,
    FOREIGN KEY (creater) REFERENCES Users(tg_id),
    FOREIGN KEY (receiver) REFERENCES Users(tg_id),
    FOREIGN KEY (status) REFERENCES Status(id)
);

COMMIT;

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Status (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    text CHAR(20),
    emoji CHAR(20)
);
INSERT INTO Status VALUES(1,'Создано', 'U+1F525');
INSERT INTO Status VALUES(2,'Отменено', 'U+274C');
INSERT INTO Status VALUES(3,'Выполняется', 'U+1F501');
INSERT INTO Status VALUES(4,'Завершено', 'U+2705');
INSERT INTO Status VALUES(5,'Переадресованно', 'U+1F503');

CREATE TABLE MaillingGroups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100) NOT NULL
);
INSERT INTO MaillingList VALUES(0, 'ALL');
INSERT INTO MaillingList VALUES(1, 'ALL_ADMINS');

CREATE TABLE MaillingUsers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    uid INTEGER NOT NULL,
    group INTEGER NOT NULL,
    FOREIGN KEY (group) REFERENCES MaillingGroups(id)
);

CREATE TABLE Companys (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100) NOT NULL
);
INSERT INTO Companys VALUES(0, 'None');

CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100),
    tg_id CHAR(100) NULL UNIQUE,
    is_admin INTEGER DEFAULT 0,
    db_managment_access INTEGER DEFAULT 0,
    company INTEGER DEFAULT 0,
    email CHAR(100) NULL,
    FOREIGN KEY (company) REFERENCES Companys(id)
);

CREATE TABLE Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date DATE NULL,                           
    creater CHAR(100) NULL,            
    receiver CHAR(100) NULL,
    receiver1 CHAR(100) NULL,               
    status INTEGER DEFAULT 0,                
    createrComment CHAR(500),
    receiverComment CHAR(500), 
    thema CHAR(100) NULL,
    rating INTEGER DEFAULT 5,
    FOREIGN KEY (creater) REFERENCES Users(tg_id),
    FOREIGN KEY (receiver) REFERENCES Users(tg_id),
    FOREIGN KEY (status) REFERENCES Status(id)
);

CREATE TABLE ContentMetadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(20) NOT NULL
);
INSERT INTO ContentMetadata VALUES(0, 'question');
INSERT INTO ContentMetadata VALUES(1, 'mailling');

CREATE TABLE Images (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    url CHAR(200) NULL,
    contentId INTEGER NOT NULL,
    metadata INTEGER NOT NULL,
    FOREIGN KEY (metadata) REFERENCES ContentMetadata(id)
);

CREATE TABLE Voices (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    url CHAR(200) NULL,
    contentId INTEGER NOT NULL,
    metadata INTEGER NOT NULL,
    FOREIGN KEY (metadata) REFERENCES ContentMetadata(id)
);

COMMIT;
PRAGMA foreign_keys=ON;
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
INSERT INTO Status VALUES(6,'Создается', 'U+1F525');

CREATE TABLE MaillingGroups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100) NOT NULL
);
INSERT INTO MaillingGroups VALUES(0, 'ALL');
INSERT INTO MaillingGroups VALUES(1, 'ALL_ADMINS');

CREATE TABLE MaillingUsers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    uid INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES MaillingGroups(id),
    FOREIGN KEY (uid) REFERENCES Users(id)
);

CREATE TABLE Companys (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100) NOT NULL
);
INSERT INTO Companys VALUES(0, 'None');

CREATE TABLE Departaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100) NOT NULL
);
INSERT INTO Departaments VALUES(0, 'None');

CREATE TABLE DepToCompanys (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    company INTEGER NOT NULL,
    departament INTEGER NOT NULL,
    FOREIGN KEY (company) REFERENCES Companys(id),
    FOREIGN KEY (departament) REFERENCES Departaments(id)
);

CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(100),
    tg_id CHAR(100) NULL UNIQUE,
    is_admin INTEGER DEFAULT 0,
    company INTEGER DEFAULT 0,
    departament INTEGER DEFAULT 0,
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

CREATE TABLE ContentTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name CHAR(20) NOT NULL
);
INSERT INTO ContentTypes VALUES(1, 'photo');
INSERT INTO ContentTypes VALUES(2, 'voice');
INSERT INTO ContentTypes VALUES(3, 'document');

CREATE TABLE Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    file_id CHAR(500) NULL,
    contentType INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (contentType) REFERENCES ContentTypes(id),
    FOREIGN KEY (owner_id) REFERENCES Users(id)
);

CREATE TABLE QuestionFiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    question_id INTEGER NOT NULL,
    fileId INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Questions(id),
    FOREIGN KEY (fileId) REFERENCES File(id)
);

CREATE TABLE UsersState (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    state CHAR(100) NOT NULL,
    value CHAR(100) NULL
);

CREATE TABLE AppBuffer (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    u_id CHAR(100) NOT NULL,
    u_status CHAR(100) NULL,
    keyboard CHAR(100) NULL,
    FOREIGN KEY (u_id) REFERENCES Users(id)
);

CREATE TABLE AppBufferVariables (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    u_id CHAR(100) NOT NULL,
    name CHAR(100) NULL,
    value CHAR(100) NULL,
    FOREIGN KEY (u_id) REFERENCES Users(id)
);

COMMIT;
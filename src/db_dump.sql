PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE Status (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    text TEXT,
    emoji TEXT
);

CREATE TABLE MaillingGroups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE Companys (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    fullname TEXT NOT NULL
);

CREATE TABLE Departaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    fullname TEXT NOT NULL
);

CREATE TABLE DepToCompanys (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    company INTEGER NOT NULL,
    departament INTEGER NOT NULL,
    FOREIGN KEY (company) REFERENCES Companys(id),
    FOREIGN KEY (departament) REFERENCES Departaments(id)
);

CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT,
    tg_id TEXT NULL UNIQUE,
    is_admin INTEGER DEFAULT 0,
    company INTEGER DEFAULT 0,
    departament INTEGER DEFAULT 0,
    email TEXT NULL,
    FOREIGN KEY (company) REFERENCES Companys(id)
);

CREATE TABLE MaillingUsers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    uid INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES MaillingGroups(id),
    FOREIGN KEY (uid) REFERENCES Users(id)
);


CREATE TABLE QuestionThems (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL 
);

CREATE TABLE Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date DATE NULL,                           
    creater TEXT NULL,            
    receiver TEXT NULL,
    receiver1 TEXT NULL,               
    status INTEGER DEFAULT 0,                
    createrComment CHAR(500),
    receiverComment CHAR(500), 
    thema INT NOT NULL,
    rating INTEGER DEFAULT 5,
    FOREIGN KEY (creater) REFERENCES Users(tg_id),
    FOREIGN KEY (receiver) REFERENCES Users(tg_id),
    FOREIGN KEY (status) REFERENCES Status(id),
    FOREIGN KEY (thema) REFERENCES QuestionThems(id)
);

CREATE TABLE ContentTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    file_id TEXT NULL,
    contentType INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (contentType) REFERENCES ContentTypes(id),
    FOREIGN KEY (owner_id) REFERENCES Users(id)
);

CREATE TABLE QuestionFiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    question_id INTEGER NULL,
    fileId INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Questions(id),
    FOREIGN KEY (fileId) REFERENCES Files(id)
);
COMMIT;
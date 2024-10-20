-- НЕ ТРОГАТЬ, В ПРОГРАММЕ ИДЕТ ЖЕСТКАЯ ПРИВЯЗКА ПРОПИСЫВАЕМЫМ СТАТУСАМ
-- ГРУППАМ РАССЫЛОК
-- КОМПАНИЯМ
-- ДЕПАРТАМЕНТАМ
-- ТИПУ КОНТЕНТА
-- ЕДИНСТВЕННОЕ ЧТО МОЖНО ПОМЕНЯТЬ ЭТО ТЕМЫ ЗАЯВОК И ЮНИКОДЫ СМАЙЛОВ В СТАТУСАХ

-- Status
INSERT INTO Status VALUES(1,'Создано', 'U+1F525');
INSERT INTO Status VALUES(2,'Отменено', 'U+274C');
INSERT INTO Status VALUES(3,'Выполняется', 'U+1F501');
INSERT INTO Status VALUES(4,'Завершено', 'U+2705');
INSERT INTO Status VALUES(5,'Переадресованно', 'U+1F503');
INSERT INTO Status VALUES(6,'Создается', 'U+1F525');
-- Status

-- MaillingGroups
INSERT INTO MaillingGroups VALUES(0, 'ALL');
INSERT INTO MaillingGroups VALUES(1, 'ALL_ADMINS');
-- MaillingGroups

-- Companys
INSERT INTO Companys VALUES(0, 'None', 'None');
-- Companys

-- Departaments
INSERT INTO Departaments VALUES(0, 'None', 'None');
-- Departaments

-- QuestionThems
INSERT INTO QuestionThems VALUES(1, '1С');
INSERT INTO QuestionThems VALUES(2, 'СЭД');
INSERT INTO QuestionThems VALUES(3, 'Проблема с компьютером');
INSERT INTO QuestionThems VALUES(4, 'Проблема с программой');
-- QuestionThems

-- ContentTypes
INSERT INTO ContentTypes VALUES(1, 'photo');
INSERT INTO ContentTypes VALUES(2, 'voice');
INSERT INTO ContentTypes VALUES(3, 'document');
INSERT INTO ContentTypes VALUES(4, 'audio');
INSERT INTO ContentTypes VALUES(5, 'video');
INSERT INTO ContentTypes VALUES(6, 'video_note');
-- ContentTypes
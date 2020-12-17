DROP DATABASE IF EXISTS project;

CREATE DATABASE project;
USE project;

CREATE TABLE Newspaper
(
  Name VARCHAR(255) NOT NULL,
  Publication_Frequency ENUM('DAILY','WEEKLY','MONTHLY') NOT NULL,
  Owner VARCHAR(255) NOT NULL,
  PRIMARY KEY (Name)
);

CREATE TABLE Worker
(
  Name VARCHAR(255) NOT NULL,
  Last_Name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  Date_of_Recruitment DATE NOT NULL,
  Salary FLOAT NOT NULL,
  Newspaper_Name VARCHAR(255) NOT NULL,
  Password VARCHAR(255) NOT NULL,
  initial_salary INT NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (Newspaper_Name) REFERENCES Newspaper(Name)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Issue
(
  Issue_No INT NOT NULL,
  Date_of_Publication DATE NOT NULL,
  No_of_pages INT DEFAULT '30' ,
  Printed_Copies INT DEFAULT '10000' ,
  Returned_copies INT DEFAULT '0',
  Newspaper_Name VARCHAR(255) NOT NULL,
  PRIMARY KEY (Issue_No, Newspaper_Name),
  FOREIGN KEY (Newspaper_Name) REFERENCES Newspaper(Name)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Administrative
(
  Duties ENUM('Secretary','Logistics') NOT NULL,
  Street VARCHAR(255) NOT NULL,
  Street_No INT NOT NULL,
  City VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (email) REFERENCES Worker(email)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Administrative_Phone
(
  Phone VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (Phone, email),
  FOREIGN KEY (email) REFERENCES Administrative(email)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Journalist
(
  pre_occupation_at_assignment INT NOT NULL,
  Short_bio VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (email) REFERENCES Worker(email)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Editor_in_chief
(
  Newspaper_Name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (Newspaper_Name) REFERENCES Newspaper(Name)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (email) REFERENCES Worker(email)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Category
(
  code INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Description VARCHAR(255) NOT NULL,
  is_child_of INT,
  PRIMARY KEY (code),
  FOREIGN KEY (is_child_of) REFERENCES Category(code)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Article
(
  article_path VARCHAR(255) NOT NULL,
  Title VARCHAR(255) NOT NULL,
  Summary VARCHAR(255) NOT NULL,
  article_order INT,
  revision_comments VARCHAR(255),
  checked_or_not ENUM('NOT CHECKED', 'APPROVED', 'TO BE REVISED','DENIED') DEFAULT 'TO BE REVISED',
  editor_in_chief VARCHAR(255),
  No_of_pages INT NOT NULL,
  Photos VARCHAR(255),
  Issue_No INT,
  Newspaper_Name VARCHAR(255) NOT NULL,
  Category INT NOT NULL,
  Approval_Date DATE default null,
  PRIMARY KEY (article_path),
  FOREIGN KEY (Category) REFERENCES Category(code)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (editor_in_chief) REFERENCES Editor_in_chief(email)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (Issue_No, Newspaper_Name) REFERENCES Issue(Issue_No, Newspaper_Name)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Submits
(
  submission_date DATE NOT NULL,
  article_path VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  PRIMARY KEY (article_path,author),
  FOREIGN KEY (article_path) REFERENCES Article(article_path)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (author) REFERENCES Journalist(email)
  ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Article_key_word
(
  article_path VARCHAR(255) NOT NULL,
  key_word VARCHAR(255) NOT NULL,
  PRIMARY KEY (article_path,key_word),
  FOREIGN KEY (article_path) REFERENCES Article(article_path)
  ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO Newspaper VALUES
('TO BHMA', 'WEEKLY', 'Maria Rigou'),
('KATHIMERINH', 'DAILY', 'Eleni Voyatzaki'),
('CEID Times', 'MONTHLY', 'Efstratios Gallopoulos');

INSERT INTO Worker VALUES
('Leonidas', 'Karagiannis', 'st1064036@ceid.upatras.gr', '2017-08-25', '1200.00', 'CEID Times','password1','1200.00'),
('Aristeidis', 'Elias', 'aristeid@ceid.upatras.gr', '1998-01-01', '2500.00', 'CEID Times','password2','2500.00'),
('Haridimos', 'Vergos', 'vergos@ceid.upatras.gr', '1985-06-10', '3000.00', 'CEID Times','password3','3000.00'),
('Ioannis', 'Hatziligeroudis', 'ihatz@ceid.upatras.gr', '1982-05-05', '2310.00', 'CEID Times','password4','2310.00'),
('George', 'Al Baboul','st1059631@ceid.upatras.gr','2016-05-20','1500.00','KATHIMERINH','password5','1500.00'),
('Spyros', 'Sioutas','sioutas@ceid.upatras.gr','2005-04-13','2100.00','KATHIMERINH','password6','2100.00'),
('George', 'Alexiou', 'alexiou@ceid.upatras.gr', '1980-01-01', '4000.00', 'KATHIMERINH','password7','4000.00'),
('Christos', 'Christidis', 'christides@ceid.upatras.gr', '2001-10-03', '900.00', 'KATHIMERINH','password8','900.00'),
('Paulinho', 'Akino Elloul', 'st1059630@ceid.upatras.gr', '2017-08-22', '1200.00', 'TO BHMA','password9','1200.00'),
('Dimitris', 'Nikolos', 'nikolosd@ceid.upatras.gr', '1985-02-25', '3000.00', 'TO BHMA','password10','3000.00'),
('Vasileios', 'Megalooikonomou', 'vasilis@ceid.upatras.gr', '1999-08-17', '1300.00', 'TO BHMA','password11','1300.00'),
('Emmanouil', 'Psarakis', 'psarakis@ceid.upatras.gr', '1995-04-03', '5000.00', 'TO BHMA','password12','5000.00');

INSERT INTO Issue VALUES
(1,'2019-01-01',DEFAULT,DEFAULT,DEFAULT,'KATHIMERINH'),
(1,'2019-03-15',50,10000,320,'TO BHMA'),
(1,'2019-02-10',24,10300,1789,'CEID Times');

INSERT INTO Administrative VALUES
('Secretary','Sofokleoys',11,'Patras','st1064036@ceid.upatras.gr'),
('Secretary','Athinon',31,'Patras','st1059631@ceid.upatras.gr'),
('Logistics','Agiou Vasileiou',4,'Patras','st1059630@ceid.upatras.gr');

INSERT INTO Journalist VALUES
(150,'bio1','vasilis@ceid.upatras.gr'),
(32,'bio2','vergos@ceid.upatras.gr'),
(231,'bio3','alexiou@ceid.upatras.gr'),
(20,'bio4','aristeid@ceid.upatras.gr'),
(30,'bio5','christides@ceid.upatras.gr'),
(40,'bio6','nikolosd@ceid.upatras.gr');

INSERT INTO Editor_in_chief VALUES
('CEID Times','aristeid@ceid.upatras.gr'),
('KATHIMERINH','christides@ceid.upatras.gr'),
('TO BHMA','nikolosd@ceid.upatras.gr');

INSERT INTO Administrative_Phone VALUES
(6986829965,'st1064036@ceid.upatras.gr'),
(6987489294,'st1059630@ceid.upatras.gr'),
(1234567890,'st1059631@ceid.upatras.gr');

INSERT INTO Category VALUES
(NULL,'Sports','Athlitika lol',DEFAULT),
(NULL,'Politics','All things politics',DEFAULT),
(NULL,'Esoteriki Politiki','All things politics',2),
(NULL,'Economics','All about the new CEID building budget',DEFAULT);

INSERT INTO Article VALUES
('path1','Title1','Summary1',DEFAULT,DEFAULT,DEFAULT,'aristeid@ceid.upatras.gr',15,DEFAULT,DEFAULT,'CEID Times',1,DEFAULT),
('path2','Title2','Summary2',DEFAULT,DEFAULT,DEFAULT,'christides@ceid.upatras.gr',24,DEFAULT,DEFAULT,'KATHIMERINH',1,DEFAULT),
('path3','Title3','Summary3',DEFAULT,DEFAULT,DEFAULT,'nikolosd@ceid.upatras.gr',24,DEFAULT,DEFAULT,'TO BHMA',1,DEFAULT);

INSERT INTO Submits VALUES
('2019-01-01','path1','vergos@ceid.upatras.gr'),
('2019-01-01','path2','alexiou@ceid.upatras.gr'),
('2019-01-01','path3','vasilis@ceid.upatras.gr');
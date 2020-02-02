DROP PROCEDURE IF EXISTS validatePassword;
DELIMITER $
CREATE PROCEDURE validatePassword(email VARCHAR(255))
BEGIN
	SELECT password,attribute FROM Passwords 
	WHERE username = email;
END $
DELIMITER ;

DROP PROCEDURE IF EXISTS insertCoAuthor;
DELIMITER $ 
CREATE PROCEDURE insertCoAuthor(articlepath VARCHAR(255), coauthor VARCHAR(255))
BEGIN
	INSERT INTO Submits VALUES
	(current_timestamp,articlepath,coauthor);
END $
DELIMITER ;
DROP PROCEDURE IF EXISTS getCategoryCode;
DELIMITER $
CREATE PROCEDURE getCategoryCode(category VARCHAR(255))
BEGIN
	SELECT code FROM Category WHERE Category.Name = category;
END $
DELIMITER ;


DROP PROCEDURE IF EXISTS showRestJournalists;
DELIMITER $
CREATE PROCEDURE showRestJournalists(email VARCHAR(255))
BEGIN 
	DECLARE newspaper VARCHAR(255);
	DECLARE editors VARCHAR(255);	
	SELECT Newspaper_Name INTO newspaper FROM Worker WHERE Worker.email=email;
	
	SELECT Journalist.email FROM Journalist
	INNER JOIN Worker ON Journalist.email = Worker.email
	LEFT JOIN Editor_in_chief ON Journalist.email = Editor_in_chief.email
	WHERE Journalist.email != email AND Worker.Newspaper_Name=newspaper ;
END $
DELIMITER ;


DROP PROCEDURE IF EXISTS insertArticleAsJournalist;
DELIMITER $
CREATE PROCEDURE insertArticleAsJournalist(article_path VARCHAR(255), 
											Title VARCHAR(255),
											Summary VARCHAR(255),
											Photos VARCHAR(255),
											Category 	             INT,											
											No_of_pages INT,
											email VARCHAR(255))
BEGIN

	DECLARE newspaper VARCHAR(255);
	DECLARE editor VARCHAR(255);
	SELECT Newspaper_Name INTO newspaper FROM Worker WHERE Worker.email=email;
	
	SELECT Editor_in_chief.email INTO editor FROM Editor_in_chief WHERE Newspaper_Name = newspaper;
	INSERT INTO Article VALUES
	(article_path,Title,Summary,NULL,NULL,'NOT CHECKED',editor,No_of_pages,Photos,1,newspaper,Category);

	INSERT INTO Submits VALUES
	(current_timestamp,article_path,email);
END $
DELIMITER ;

CALL insertArticleAsJournalist('path4','TEST','Summary4',5,'PHTOS',1,'vergos@ceid.upatras.gr');


DROP PROCEDURE IF EXISTS insertArticleAsEditor;
DELIMITER $
CREATE PROCEDURE insertArticleAsEditor(article_path VARCHAR(255),
                                        Title VARCHAR(255),
                                        Summary VARCHAR(255),
                                        No_of_pages INT,
                                        Photos VARCHAR(255),
                                        Category INT,
                                        email VARCHAR(255)
                                        )
BEGIN

    DECLARE newspaper VARCHAR(255);
    SELECT Newspaper_Name INTO newspaper FROM Worker WHERE Worker.email=email;
    
    INSERT INTO Article VALUES
    (article_path,Title,Summary,NULL,NULL,'APPROVED',email,No_of_pages,Photos,1,newspaper,Category);

END$
DELIMITER ;



DROP PROCEDURE IF EXISTS updateCheckStatus;
DELIMITER $
CREATE PROCEDURE updateCheckStatus(my_article_path VARCHAR(255), checkStatus VARCHAR(255))
BEGIN
		UPDATE Article
		SET checked_or_not = checkStatus 
		WHERE article_path = my_article_path;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS updateArticle;
DELIMITER $
CREATE PROCEDURE updateArticle(articlepath VARCHAR(255),
								new_title VARCHAR(255),
								new_summary VARCHAR(255),
								new_no_of_pages INT,
								new_photos VARCHAR(255),
								new_category INT,
								email VARCHAR(255))
BEGIN

	DECLARE newspaper VARCHAR(255);
	SELECT Newspaper_Name INTO newspaper FROM Worker WHERE Worker.email=email;

	UPDATE Article
	SET 
	Title = new_title,
	Summary = new_summary,
	No_of_pages = new_no_of_pages,
	Photos = new_photos,
	Category = new_category
	WHERE Article.Newspaper_Name = newspaper AND Article.article_path = articlepath;

END$
DELIMITER ;



DROP PROCEDURE IF EXISTS showAllIssues;
DELIMITER $
CREATE PROCEDURE showAllIssues(email VARCHAR(255))
BEGIN
	DECLARE newspaper VARCHAR(255);
	SELECT Newspaper_Name INTO newspaper FROM Worker WHERE Worker.email=email;

	SELECT Issue_No FROM Issue
	WHERE Newspaper_Name = newspaper;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS showArticle;
DELIMITER $
CREATE PROCEDURE showArticle(articlepath VARCHAR(255))
BEGIN
	SELECT * FROM Article 
	WHERE article_path = articlepath;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS showAllJournalistArticles;
DELIMITER $
CREATE PROCEDURE showAllJournalistArticles(journalist_email VARCHAR(255))
BEGIN
	SELECT Article.article_path FROM Article
	INNER JOIN Submits 
	ON Submits.article_path = Article.article_path
	WHERE journalist_email = Submits.email;
END $
DELIMITER ; 


DROP PROCEDURE IF EXISTS showAllOwnedNewspapers;
DELIMITER $
CREATE PROCEDURE showAllOwnedNewspapers(IN username VARCHAR(255))
BEGIN
	SELECT Name FROM Newspaper WHERE Owner = username;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS showAllNewspaperJournalists;
DELIMITER $
CREATE PROCEDURE showAllNewspaperJournalists(newspaper VARCHAR(255))
BEGIN 
	SELECT Worker.Name,Worker.Last_name FROM Journalist
	INNER JOIN Worker 
	ON Worker.email = Journalist.email
	WHERE Worker.Newspaper_Name = newspaper;
END $
DELIMITER ; 




DROP PROCEDURE IF EXISTS showAllArticlesNotInIssue;
DELIMITER $ 
CREATE PROCEDURE showAllArticlesNotInIssue(editor varchar(255),issue INT)
BEGIN
	SELECT article_path,No_of_pages FROM Article 
	WHERE editor_in_chief = editor AND (Article.Issue_No != issue OR Article.Issue_No IS NULL );
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS updateComments;
DELIMITER $ 
CREATE PROCEDURE updateComments(articlepath VARCHAR(255),new_comments VARCHAR(255))
BEGIN
	UPDATE Article
	SET   revision_comments = new_comments
	WHERE article_path = articlepath;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS showAllCategories;
DELIMITER $
CREATE PROCEDURE showAllCategories()
BEGIN
	SELECT Name FROM Category;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS insertNewCategory;
DELIMITER $
CREATE PROCEDURE insertNewCategory(name VARCHAR(255),description VARCHAR(255),is_child_of INT)
BEGIN 
	IF is_child_of != 0 THEN
		INSERT INTO Category VALUES (NULL,name,description,is_child_of);
	
	ELSE
		INSERT INTO Category VALUES (NULL,name,description,NULL);
	END IF;	
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS insertReturnedCopies;
DELIMITER $ 
CREATE PROCEDURE insertReturnedCopies(issueno INT ,returned_copies INT,email VARCHAR(255))
BEGIN
	DECLARE newspaper VARCHAR(255);
	SELECT Newspaper_Name INTO newspaper FROM Worker WHERE Worker.email=email;


	UPDATE Issue
	SET  Returned_copies = returned_copies
	WHERE Issue_no = issueno AND Newspaper_Name = newspaper;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS showTotalExpenses;
DELIMITER $
CREATE PROCEDURE showTotalExpenses(first_month int , second_month int)
BEGIN
	DECLARE month INT;
	DECLARE Total_expenses INT;
	SET month = second_month - first_month + 1;
	SET Total_expenses = month * ( SELECT SUM(salary) FROM Worker);

	SELECT Total_expenses;
END $
DELIMITER ; 	
	 


DROP PROCEDURE IF EXISTS updateNewspaper;
DELIMITER $
CREATE PROCEDURE updateNewspaper(Name VARCHAR(255),Publication_Frequency VARCHAR(20) , Owner VARCHAR(255))
BEGIN
	UPDATE Newspaper SET Name = Name,Publication_Frequency = Publication_Frequency WHERE Owner = Owner;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS insertNumberOfCopies;
DELIMITER $ 
CREATE PROCEDURE insertNumberOfCopies(issue INT,copies INT, Newspaper VARCHAR(255))
BEGIN
	
	UPDATE Issue
	SET Printed_Copies = copies
	WHERE Issue_No = issue AND Newspaper_Name = Newspaper;
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS insertPriorityNumber;
DELIMITER & 
CREATE PROCEDURE insertPriorityNumber(articlepath varchar(255),priority int)
BEGIN
	UPDATE Article
	SET  article_order = priority
	WHERE Article_Path = articlepath;
END &
DELIMITER ;




DROP PROCEDURE IF EXISTS addKeyWords;
DELIMITER $ 
CREATE PROCEDURE addKeyWords(articlepath VARCHAR(255),keyword VARCHAR(255))
BEGIN
	INSERT INTO Article_key_word VALUES (articlepath,keyword);
END $
DELIMITER ;



DROP PROCEDURE IF EXISTS promotion;
DELIMITER & 
CREATE PROCEDURE promotion(email varchar(255))
BEGIN
	DECLARE paper varchar(255);
	
	SET paper = (SELECT Worker.Newspaper_Name FROM Worker WHERE Worker.email = email );
	
	UPDATE Editor_in_chief 
	SET Editor_in_chief.email = email WHERE Editor_in_chief.Newspaper_Name = paper;
END &
DELIMITER ;

DROP PROCEDURE IF EXISTS getCatName;
DELIMITER $
CREATE PROCEDURE getCatName(IN cod INT)
BEGIN
	SELECT Name FROM Category WHERE code = cod ;
END $
DELIMITER ;

DROP PROCEDURE IF EXISTS showAllIssuesPub;
DELIMITER $
CREATE PROCEDURE showAllIssuesPub(Newspaper VARCHAR(255))
BEGIN
	
	SELECT Issue_No FROM Issue
	WHERE Newspaper_Name = Newspaper;
END $
DELIMITER ;

DROP PROCEDURE IF EXISTS showOldEditor;
DELIMITER $
CREATE PROCEDURE showOldEditor(Newspaper VARCHAR(255))
BEGIN
	
	SELECT Name, Last_Name FROM Editor_in_chief
	INNER JOIN Worker ON Worker.email = Editor_in_chief.email
	WHERE Worker.Newspaper_Name = Newspaper;
END $
DELIMITER ;

DROP PROCEDURE IF EXISTS nameToEmail;
DELIMITER $
CREATE PROCEDURE nameToEmail(Name VARCHAR(255),lastname VARCHAR(255))
BEGIN
	
	SELECT email FROM Worker
	WHERE Name = Name and Last_Name = lastname;
END $
DELIMITER ;

DROP PROCEDURE IF EXISTS totalSold;
DELIMITER $
CREATE PROCEDURE totalSold(Newspaper VARCHAR(255),issueno INT)
BEGIN
	SELECT Printed_Copies - Returned_Copies AS SOLD FROM Issue 
	WHERE Newspaper_Name = Newspaper AND Issue_No = issueno;
	
END $
DELIMITER ;

DROP PROCEDURE if exists showAllNewspaperExpenses;
DELIMITER &
CREATE PROCEDURE showAllNewspaperExpenses(first_month DATE , second_month DATE, em VARCHAR(255))
BEGIN 
	DECLARE all_salary INT;
	DECLARE paper VARCHAR(255);
	DECLARE months INT;
	DECLARE datediff INT;
	
	SELECT DATEDIFF( second_month , first_month ) INTO datediff;
	SET months = (datediff / 30);
	
	SET paper = (SELECT Newspaper_Name FROM Worker WHERE email = em);
	
	SET all_salary = months * ( SELECT sum(salary) FROM Worker WHERE Newspaper_Name = paper);
	SELECT all_salary;
END&
DELIMITER ; 	

DROP PROCEDURE IF EXISTS showNewspaperExpensesPerEmployee;
DELIMITER &
CREATE PROCEDURE showNewspaperExpensesPerEmployee(first_month DATE , second_month DATE, em VARCHAR(255))
BEGIN 
	DECLARE months INT;
	DECLARE datediff INT;
	DECLARE all_salary INT ;
	DECLARE paper VARCHAR(255);
	
	SELECT DATEDIFF( second_month , first_month ) into datediff;
	SET months = (datediff / 30);
	
	
	SET paper = (SELECT Newspaper_Name FROM Worker WHERE email = em);
		
	SELECT Worker.name AS name , Worker.last_name AS last_name , salary * months AS cost FROM Worker WHERE Newspaper_Name = paper;

	
END&
DELIMITER ; 


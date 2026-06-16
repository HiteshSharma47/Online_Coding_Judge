CREATE DATABASE OCJ

USE OCJ

--For Problems
CREATE TABLE Problems
(
problem_id INT PRIMARY KEY IDENTITY(1,1),
title VARCHAR(MAX) NOT NULL,
description VARCHAR(MAX) NOT NULL,
input_format VARCHAR(MAX),
output_format VARCHAR(MAX),
sample_input VARCHAR(MAX),
sample_output VARCHAR(MAX)
)

--Testcases for each Problem
CREATE TABLE Testcases
(
testcase_id INT PRIMARY KEY IDENTITY(1,1),
problem_id INT,
input_data VARCHAR(MAX) NOT NULL,
expected_output VARCHAR(MAX) NOT NULL,

CONSTRAINT FK_TestCases_Problems
FOREIGN KEY (problem_id)
REFERENCES Problems(problem_id)
)

--Submissions Done By User Will go here
CREATE TABLE Submissions
(
submission_id INT PRIMARY KEY IDENTITY(1,1),
problem_id INT NOT NULL,
code VARCHAR(MAX) NOT NULL,
verdict VARCHAR(50),

CONSTRAINT FK_Submissions_Problems
FOREIGN KEY (problem_id)
REFERENCES Problems(problem_id)
)

--Problem 1
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
'Add Two Integers',
'Read two integers and print their sum',
'Two Integers Separated By a Space',
'Print The Sum of two Integers',
'2 3',
'5'
)

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(1, '2 3', '5'),
(1, '5 7', '12'),
(1, '10 20', '30'),
(1, '100 200', '300'),
(1, '1 1', '2'),
(1, '0 5', '5'),
(1, '0 0', '0'),
(1, '99 1', '100'),
(1, '123 456', '579'),
(1, '5000 5000', '10000');

--Problem 2
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
'Multiply Two Integers',
'Given two integers, print their product.',
'Two space-separated integers A and B',
'A single integer representing A * B',
'3 4',
'12'
);

INSERT INTO TestCases (problem_id,input_data,expected_output)
VALUES
(2,'3 4','12'),
(2,'5 5','25'),
(2,'10 20','200'),
(2,'0 5','0'),
(2,'1 999','999'),
(2,'7 8','56'),
(2,'12 12','144'),
(2,'100 2','200'),
(2,'50 50','2500'),
(2,'123 2','246');

--Problem 3
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
'Maximum of Two Numbers',
'Given two integers, print the larger number.',
'Two space-separated integers A and B',
'The maximum value',
'10 20',
'20'
);

INSERT INTO Testcases (problem_id,input_data,expected_output)
VALUES
(3,'10 20','20'),
(3,'50 30','50'),
(3,'100 100','100'),
(3,'1 2','2'),
(3,'99 1','99'),
(3,'7 7','7'),
(3,'500 1000','1000'),
(3,'45 12','45'),
(3,'999 998','999'),
(3,'250 250','250');

--Problem 4
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
'Sum of Three Integers',
'Given three integers, print their sum.',
'Three space-separated integers A B C',
'A single integer representing A+B+C',
'1 2 3',
'6'
);

INSERT INTO Testcases (problem_id,input_data,expected_output)
VALUES
(4,'1 2 3','6'),
(4,'10 20 30','60'),
(4,'5 5 5','15'),
(4,'100 200 300','600'),
(4,'0 0 0','0'),
(4,'1 1 1','3'),
(4,'50 25 25','100'),
(4,'7 8 9','24'),
(4,'500 500 500','1500'),
(4,'123 456 789','1368');


--Problem 5
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
'Even or Odd',
'Given an integer, print Even if divisible by 2 otherwise print Odd.',
'Single integer N',
'Even or Odd',
'4',
'Even'
);

INSERT INTO Testcases (problem_id,input_data,expected_output)
VALUES
(5,'4','Even'),
(5,'7','Odd'),
(5,'10','Even'),
(5,'1','Odd'),
(5,'100','Even'),
(5,'99','Odd'),
(5,'50','Even'),
(5,'13','Odd'),
(5,'2','Even'),
(5,'15','Odd');

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


-- Problem 6
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Palindrome Number',
  'Given an integer, return True if the integer is a palindrome, and False otherwise.',
  'A single integer',
  'True or False',
  '121',
  'True'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(6, '121', 'True'),
(6, '-121', 'False'),
(6, '10', 'False'),
(6, '12321', 'True'),
(6, '1', 'True'),
(6, '0', 'True'),
(6, '11', 'True'),
(6, '123', 'False'),
(6, '1221', 'True'),
(6, '9999', 'True');

-- Problem 7
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Factorial',
  'Calculate the factorial of a given non-negative integer N.',
  'A single integer N',
  'The factorial of N',
  '5',
  '120'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(7, '0', '1'),
(7, '1', '1'),
(7, '2', '2'),
(7, '3', '6'),
(7, '4', '24'),
(7, '5', '120'),
(7, '6', '720'),
(7, '7', '5040'),
(7, '8', '40320'),
(7, '9', '362880');

-- Problem 8
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Reverse String',
  'Given a string, print its reverse.',
  'A single string',
  'The reversed string',
  'hello',
  'olleh'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(8, 'hello', 'olleh'),
(8, 'world', 'dlrow'),
(8, 'python', 'nohtyp'),
(8, 'a', 'a'),
(8, 'ab', 'ba'),
(8, 'coding', 'gnidoc'),
(8, 'judge', 'egduj'),
(8, 'racecar', 'racecar'),
(8, 'test', 'tset'),
(8, 'antigravity', 'ytivargitna');

-- Problem 9
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Fibonacci Number',
  'Given N, calculate the N-th Fibonacci number. F(0) = 0, F(1) = 1, F(N) = F(N-1) + F(N-2).',
  'A single integer N',
  'The N-th Fibonacci number',
  '6',
  '8'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(9, '0', '0'),
(9, '1', '1'),
(9, '2', '1'),
(9, '3', '2'),
(9, '4', '3'),
(9, '5', '5'),
(9, '6', '8'),
(9, '7', '13'),
(9, '8', '21'),
(9, '9', '34');

-- Problem 10
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Leap Year Check',
  'Determine if a given year is a leap year. Print Yes or No.',
  'A single integer representing the year',
  'Yes or No',
  '2020',
  'Yes'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(10, '2020', 'Yes'),
(10, '2021', 'No'),
(10, '1900', 'No'),
(10, '2000', 'Yes'),
(10, '2024', 'Yes'),
(10, '2100', 'No'),
(10, '2016', 'Yes'),
(10, '2018', 'No'),
(10, '2400', 'Yes'),
(10, '2004', 'Yes');

-- Problem 11
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Square of a Number',
  'Calculate the square of a given integer.',
  'A single integer N',
  'The square of N',
  '5',
  '25'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(11, '0', '0'),
(11, '1', '1'),
(11, '-2', '4'),
(11, '5', '25'),
(11, '10', '100'),
(11, '-10', '100'),
(11, '12', '144'),
(11, '15', '225'),
(11, '20', '400'),
(11, '100', '10000');

-- Problem 12
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Fahrenheit to Celsius',
  'Convert a temperature from Fahrenheit to Celsius using formula C = (F - 32) * 5/9. Round to the nearest integer.',
  'A single integer Fahrenheit',
  'The rounded integer Celsius value',
  '32',
  '0'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(12, '32', '0'),
(12, '50', '10'),
(12, '68', '20'),
(12, '86', '30'),
(12, '104', '40'),
(12, '-40', '-40'),
(12, '212', '100'),
(12, '98', '37'),
(12, '0', '-18'),
(12, '10', '-12');

-- Problem 13
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Sum of Digits',
  'Calculate the sum of digits of a non-negative integer N.',
  'A single non-negative integer N',
  'The sum of the digits',
  '123',
  '6'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(13, '0', '0'),
(13, '5', '5'),
(13, '12', '3'),
(13, '123', '6'),
(13, '999', '27'),
(13, '1001', '2'),
(13, '4567', '22'),
(13, '9090', '18'),
(13, '11111', '5'),
(13, '987654', '39');

-- Problem 14
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Prime Number Check',
  'Check if a given positive integer N is prime. Print Yes or No.',
  'A single positive integer N',
  'Yes or No',
  '7',
  'Yes'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(14, '1', 'No'),
(14, '2', 'Yes'),
(14, '3', 'Yes'),
(14, '4', 'No'),
(14, '5', 'Yes'),
(14, '6', 'No'),
(14, '7', 'Yes'),
(14, '8', 'No'),
(14, '9', 'No'),
(14, '11', 'Yes');

-- Problem 15
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Power of Two Check',
  'Check if a given integer is a power of two. Print True or False.',
  'A single integer N',
  'True or False',
  '16',
  'True'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(15, '16', 'True'),
(15, '3', 'False'),
(15, '1', 'True'),
(15, '0', 'False'),
(15, '-2', 'False'),
(15, '8', 'True'),
(15, '64', 'True'),
(15, '100', 'False'),
(15, '1024', 'True'),
(15, '512', 'True');

-- Problem 16
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Count Vowels',
  'Count the number of vowels (a, e, i, o, u, case-insensitive) in a string.',
  'A single string',
  'An integer representing the number of vowels',
  'hello',
  '2'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(16, 'hello', '2'),
(16, 'world', '1'),
(16, 'python', '1'),
(16, 'AEIOU', '5'),
(16, 'xyz', '0'),
(16, 'a', '1'),
(16, 'b', '0'),
(16, 'coding', '2'),
(16, 'online judge', '5'),
(16, 'testcase', '3');

-- Problem 17
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Largest of Three',
  'Given three integers, print the largest one.',
  'Three space-separated integers A B C',
  'The largest integer',
  '10 20 15',
  '20'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(17, '10 20 15', '20'),
(17, '5 5 5', '5'),
(17, '-1 -5 0', '0'),
(17, '100 20 5', '100'),
(17, '10 20 30', '30'),
(17, '30 20 10', '30'),
(17, '10 30 20', '30'),
(17, '-10 -20 -30', '-10'),
(17, '9 9 10', '10'),
(17, '1 10 10', '10');

-- Problem 18
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Greatest Common Divisor',
  'Calculate the Greatest Common Divisor (GCD) of two positive integers A and B.',
  'Two space-separated integers A and B',
  'The GCD of A and B',
  '12 18',
  '6'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(18, '12 18', '6'),
(18, '5 7', '1'),
(18, '10 20', '10'),
(18, '24 60', '12'),
(18, '17 17', '17'),
(18, '1 5', '1'),
(18, '100 10', '10'),
(18, '48 180', '12'),
(18, '81 27', '27'),
(18, '9 6', '3');

-- Problem 19
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Least Common Multiple',
  'Calculate the Least Common Multiple (LCM) of two positive integers A and B.',
  'Two space-separated integers A and B',
  'The LCM of A and B',
  '12 18',
  '36'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(19, '12 18', '36'),
(19, '5 7', '35'),
(19, '10 20', '20'),
(19, '24 60', '120'),
(19, '17 17', '17'),
(19, '1 5', '5'),
(19, '100 10', '100'),
(19, '48 180', '720'),
(19, '8 12', '24'),
(19, '9 6', '18');

-- Problem 20
INSERT INTO Problems
(title, description, input_format, output_format, sample_input, sample_output)
VALUES
(
  'Capitalize Words',
  'Capitalize the first letter of each word in a string.',
  'A single line of text',
  'The capitalized text',
  'hello world',
  'Hello World'
);

INSERT INTO Testcases (problem_id, input_data, expected_output)
VALUES
(20, 'hello world', 'Hello World'),
(20, 'python programming', 'Python Programming'),
(20, 'a b c', 'A B C'),
(20, 'coding judge', 'Coding Judge'),
(20, 'computer science', 'Computer Science'),
(20, 'test case', 'Test Case'),
(20, 'high quality', 'High Quality'),
(20, 'hello', 'Hello'),
(20, 'multiple words here', 'Multiple Words Here'),
(20, 'welcome to leetcode', 'Welcome To LeetCode');

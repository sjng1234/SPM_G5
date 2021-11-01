insert into course 
values ("IS110", "Information Systems and Innovation", "Overview of Business Cases", "HR Adrian", "2021-08-16"),
("IS111", "Introduction to Programming", "Basic to Python", "HR Adrian", "2021-08-16"),
("IS112", "Introduction to Coding", "Basic to Python", "HR101", "2021-08-20");

insert into classes
values ("IS110", 1, "Patrick Thng", "2021-08-31", "2021-11-29", 40, 1),
("IS110", 2, "Lee Yeow Leong", "2021-08-31", "2021-11-29", 40, 1),
("IS111", 1, "Lee Yeow Leong", "2021-08-31", "2021-11-29", 40, 1),
("IS112", 1, "Lee Yeow Leong", "2021-08-31", "2021-11-29", 40, 1),
("IS112", 2, "Lee Yeow Leong", "2021-08-31", "2021-11-29", 40, 1);

insert into chapter
values ("IS110", 1, 1, "String Methods"),
("IS111", 1, 2, "Conditional Statements"),
("IS111", 2, 1, "String Methods"),
("IS112", 2, 2, "Conditional Statements");

insert into quiz
values ("IS110", 1, 1, 100),
("IS111", 1, 2, 100),
("IS112", 1, 3, 100);

insert into quiz_questions
values ("IS110", 1, 1, 1,"Are you smart?"),
("IS111", 1, 2, 1,"Are you dumb?"),
("IS111", 1, 2, 2, "Are you cool?"),
("IS112", 1, 3, 1, "Are you funky?");

insert into quiz_questions_options
values ("IS110", 1, 1, 1,"No", false),
("IS111", 1, 2, 1,"yes",false),
("IS111", 1, 2, 2, "treu",true),
("IS112", 1, 3, 1, "no",false);
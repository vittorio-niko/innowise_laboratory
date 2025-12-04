-- ------------------------------
-- Task 1: Creating tables
-- ------------------------------

-- Table "students" (parent for "grades")
CREATE TABLE IF NOT EXISTS students (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	full_name TEXT NOT NULL CHECK(TRIM(full_name) != ''), -- name cannot be empty
	birth_year INTEGER NOT NULL,
	CONSTRAINT birth_year_chk CHECK(birth_year > 1900) -- birth year check
);

-- Table "grades" (child for "students")
CREATE TABLE IF NOT EXISTS grades (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	student_id INTEGER NOT NULL,
	subject TEXT NOT NULL CHECK(TRIM(subject) != ''), -- subject name cannot be empty
	grade INTEGER NOT NULL,
	CONSTRAINT grade_chk CHECK(grade BETWEEN 0 AND 100), -- valid grade range check
	FOREIGN KEY (student_id) 
		REFERENCES students(id)
		ON DELETE CASCADE -- grades get deleted automatically with a student
);

-- ------------------------------
-- Task 2: Insert data
-- ------------------------------

-- Students data
INSERT INTO students(full_name, birth_year) VALUES
	('Alice Johnson', 2005),
	('Brian Smith', 2004), 
	('Carla Reyes', 2006), 
	('Daniel Kim', 2005),
	('Eva Thompson', 2003),
	('Felix Nguyen', 2007), 
	('Grace Patel', 2005),
	('Henry Lopez', 2004),
	('Isabella Martinez', 2006);
	
-- Grades data
INSERT INTO grades(student_id, subject, grade) VALUES
	(1, 'Math', 88),
	(1, 'English', 92),
	(1, 'Science', 85),
	(2, 'Math', 75),
	(2, 'History', 83),
	(2, 'English', 79),
	(3, 'Science', 95),
	(3, 'Math', 91),
	(3, 'Art', 89),
	(4, 'Math', 84),
	(4, 'Science', 88),
	(4, 'Physical Education', 93),
	(5, 'English', 90),
	(5, 'History', 85),
	(5, 'Math', 88),
	(6, 'Science', 72),
	(6, 'Math', 78),
	(6, 'English', 81),
	(7, 'Art', 94),
	(7, 'Science', 87),
	(7, 'Math', 90),
	(8, 'History', 77),
	(8, 'Math', 83),
	(8, 'Science', 80),
	(9, 'English', 96),
	(9, 'Math', 89),
	(9, 'Art', 92);

-- ------------------------------
-- Create indices for optimization
-- ------------------------------

-- idx_grades_student_id (most frequently used for access to grades)
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);

-- idx_grades_student_grade (composite index for queries which touch 
-- both student_id and grade (e.g. Task 8))
CREATE INDEX IF NOT EXISTS idx_grades_student_grade ON grades(student_id, grade);

-- idx_students_full_name (full_name search optimization (e.g. Task 3))
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students(full_name);

-- idx_students_birth_year (optimization for range queries by birth_year (e.g. Task 5))
CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students(birth_year);

-- ------------------------------
-- Task 3: All grades for the specific student (Alice Johnson)
-- ------------------------------
SELECT 
    subject, 
    grade 
FROM grades 
WHERE student_id = (
    SELECT id 
    FROM students 
    WHERE full_name = 'Alice Johnson'
)
ORDER BY grade DESC; -- from the best grade to the worst

-- ------------------------------
-- Task 4: Average grade per student
-- ------------------------------
SELECT 
	full_name, 
	birth_year,
	ROUND(
		AVG(grade), -- rounded to 2 digits 
		2
	) AS avg_grade
FROM students 
LEFT JOIN grades ON students.id = grades.student_id
GROUP BY full_name
ORDER BY full_name ASC; -- alphabetic order for students

-- ------------------------------
-- Task 5: Students born after 2004
-- ------------------------------
SELECT 
	full_name,
	birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year DESC, full_name ASC; -- from the youngest to the oldest

-- ------------------------------
-- Task 6: All subjects and their average grades
-- ------------------------------
SELECT 
	subject,
	ROUND(
		AVG(grade), -- rounded to 2 digits 
		2
	) AS avg_subject_grade
FROM grades
GROUP BY subject
ORDER BY subject ASC; -- alphabetic order for subjects

-- ------------------------------
-- Task 7: Top 3 students with the highest average grades
-- ------------------------------
SELECT 
	full_name, 
	birth_year,
	ROUND(
		AVG(grade), -- rounded to 2 digits 
		2
	) AS avg_grade
FROM students 
LEFT JOIN grades ON students.id = grades.student_id
GROUP BY full_name
ORDER BY avg_grade DESC, full_name ASC
LIMIT 3; -- only the first 3 students

-- ------------------------------
-- Task 8: Students who scored below 80 in any subject
-- ------------------------------
SELECT 
	full_name,
	birth_year
FROM students
WHERE EXISTS ( -- check if a grade below 80 exists
	SELECT 1 
	FROM grades 
	WHERE students.id = grades.student_id 
	  AND grade < 80
)
ORDER BY full_name ASC; -- alphabetic order for students


-- ============================================
-- SCHOOL DATABASE SETUP
-- Database for storing student information and grades
-- ============================================

-- Drop existing tables for clean setup
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

-- ============================================
-- 1. CREATE TABLES
-- ============================================

-- Students table: stores basic student information
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Grades table: stores student grades with foreign key constraint
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL,
    -- Ensure grade is between 1 and 100
    CHECK (grade >= 1 AND grade <= 100),
    -- Foreign key to maintain referential integrity
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ============================================
-- 2. INSERT SAMPLE DATA
-- ============================================

-- Insert student records
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Insert grade records (first dataset)
INSERT INTO grades (student_id, subject, grade) VALUES
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
(7, 'Art', 94);

-- Insert additional grade records (second dataset)
INSERT INTO grades (student_id, subject, grade) VALUES
(7, 'Science', 87),
(7, 'Math', 90),
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);

-- ============================================
-- 3. CREATE INDEXES FOR QUERY OPTIMIZATION
-- ============================================

-- Index for fast student lookups in grades table
CREATE INDEX idx_student_id ON grades(student_id);

-- Index for subject-based queries
CREATE INDEX idx_subject ON grades(subject);

-- Index for grade range queries (e.g., grades below 80)
CREATE INDEX idx_grade ON grades(grade);

-- Index for birth year queries in students table
CREATE INDEX idx_birth_year ON students(birth_year);

-- Composite index for common student-subject queries
CREATE INDEX idx_student_subject ON grades(student_id, subject);

-- ============================================
-- 4. EXECUTE REQUIRED QUERIES
-- ============================================

-- Query 3: Find all grades for Alice Johnson
SELECT
    s.full_name,
    g.subject,
    g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson'
ORDER BY g.subject;

-- Query 4: Calculate average grade per student
SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- Query 5: List all students born after 2004
SELECT
    full_name,
    birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year DESC;

-- Query 6: List all subjects and their average grades
SELECT
    subject,
    ROUND(AVG(grade), 2) as average_grade,
    COUNT(*) as number_of_grades
FROM grades
GROUP BY subject
ORDER BY average_grade DESC;

-- Query 7: Find top 3 students with highest average grades
SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Query 8: Show all students who scored below 80 in any subject
SELECT DISTINCT
    s.full_name,
    g.subject,
    g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name, g.grade;

-- ============================================
-- ADDITIONAL ANALYSIS QUERIES
-- ============================================

-- Complete student grade report with letter grades
SELECT
    s.full_name,
    s.birth_year,
    g.subject,
    g.grade,
    CASE
        WHEN g.grade >= 90 THEN 'A'
        WHEN g.grade >= 80 THEN 'B'
        WHEN g.grade >= 70 THEN 'C'
        WHEN g.grade >= 60 THEN 'D'
        ELSE 'F'
    END as letter_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
ORDER BY s.full_name, g.subject;

-- Count of subjects taken by each student
SELECT
    s.full_name,
    COUNT(g.subject) as subjects_taken
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY subjects_taken DESC;
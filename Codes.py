def check_number(num):
    # Check perfect number
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    isperfect = (divisorssum == num)
    
    # Check palindrome
    is_palindrome = str(num) == str(num)[::-1]
    
    return (isperfect, ispalindrome)

Example
print(check_number(121))  # (False, True)


def is_fibonacci(n):
    from math import sqrt
    # Check if 5n² ± 4 is a perfect square
    return int(sqrt(5nn + 4))2 == 5nn + 4 or int(sqrt(5nn - 4))2 == 5nn - 4

def is_harshad(n):
    digit_sum = sum(int(d) for d in str(n))
    return n % digit_sum == 0

def checkfibharshad(num):
    return (isfibonacci(num), isharshad(num))

Example
print(checkfibharshad(21))  # (True, False)



filename = "lines.txt"

Read multi-line input
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

Save to file
with open(filename, "w") as f:
    for line in lines:
        f.write(line + "\n")

Read and print with length
linecount = wordcount = char_count = 0
with open(filename, "r") as f:
    for line in f:
        line = line.rstrip("\n")
        print(f"{line} ({len(line)} chars)")
        line_count += 1
        word_count += len(line.split())
        char_count += len(line)

print(f"Lines: {linecount}, Words: {wordcount}, Chars: {char_count}")


-- 1. List employee details along with their salary
SELECT e.emp_id, e.name, e.department, s.salary
FROM EMPLOYEES e
JOIN SALARIES s ON e.emp_id = s.emp_id;

-- 2. Find the average salary by department
SELECT e.department, AVG(s.salary) AS avg_salary
FROM EMPLOYEES e
JOIN SALARIES s ON e.emp_id = s.emp_id
GROUP BY e.department;

-- 3. List employees without salary records
SELECT e.emp_id, e.name, e.department
FROM EMPLOYEES e
LEFT JOIN SALARIES s ON e.emp_id = s.emp_id
WHERE s.emp_id IS NULL;
-- 1. Show all enrollments with the student's name
SELECT s.student_id, s.name, e.course_id
FROM STUDENTS s
JOIN ENROLLMENTS e ON s.student_id = e.student_id;

-- 2. Get the total number of courses each student is enrolled in
SELECT s.student_id, s.name, COUNT(e.course_id) AS total_courses
FROM STUDENTS s
LEFT JOIN ENROLLMENTS e ON s.student_id = e.student_id
GROUP BY s.student_id, s.name;

-- 3. List students not enrolled in any course
SELECT s.student_id, s.name
FROM STUDENTS s
LEFT JOIN ENROLLMENTS e ON s.student_id = e.student_id
WHERE e.student_id IS NULL;

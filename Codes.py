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


filename = "paragraphs.txt"

Accept paragraphs
paras = []
while True:
    line = input()
    if line == "":
        break
    paras.append(line)

Save to file
with open(filename, "w") as f:
    for p in paras:
        f.write(p + "\n")

Read and process
longest_line = ""
totalwords = totalchars = 0
with open(filename, "r") as f:
    for idx, line in enumerate(f, start=1):
        line = line.rstrip("\n")
        print(f"{idx}: {line}")
        if len(line) > len(longest_line):
            longest_line = line
        total_words += len(line.split())
        total_chars += len(line)

print(f"Longest line: {longest_line}")
print(f"Total words: {totalwords}, Total chars: {totalchars}")


-- List employee details along with salary
SELECT e.*, s.salary
FROM EMPLOYEES e
JOIN SALARIES s ON e.empid = s.empid;

-- Average salary by department
SELECT department, AVG(salary) AS avg_salary
FROM EMPLOYEES e
JOIN SALARIES s ON e.empid = s.empid
GROUP BY department;

-- Employees without salary records
SELECT e.*
FROM EMPLOYEES e
LEFT JOIN SALARIES s ON e.empid = s.empid
WHERE s.emp_id IS NULL;
-- Show all enrollments with student's name
SELECT s.studentname, e.courseid
FROM STUDENTS s
JOIN ENROLLMENTS e ON s.studentid = e.studentid;

-- Total number of courses each student is enrolled in
SELECT s.studentname, COUNT(e.courseid) AS total_courses
FROM STUDENTS s
LEFT JOIN ENROLLMENTS e ON s.studentid = e.studentid
GROUP BY s.student_name;

-- Students not enrolled in any course
SELECT s.*
FROM STUDENTS s
LEFT JOIN ENROLLMENTS e ON s.studentid = e.studentid
WHERE e.student_id IS NULL;

Read a text file line by line and print each word separated by #
f=open("data.txt")
for line in f:
    print("#".join(line.split()))

Count vowels, consonants, uppercase and lowercase characters
t=open("data.txt").read()
v=sum(c.lower() in "aeiou" for c in t)
co=sum(c.isalpha() and c.lower() not in "aeiou" for c in t)
print(v, co, sum(c.isupper() for c in t), sum(c.islower() for c in t))

Copy all lines that do NOT contain 'a' into another file
fin=open("data.txt"); fout=open("out.txt","w")
[fout.write(l) for l in fin if 'a' not in l]

Binary file: store name & roll, search roll and display name
import pickle
data=[["Ram",1],["Mina",2]]
pickle.dump(data,open("stud.dat","wb"))
print(next((n for n,r in pickle.load(open("stud.dat","rb")) if r==2),"Not Found"))

Binary file: update marks for a given roll
import pickle
s=pickle.load(open("marks.dat","rb"))
for x in s:
    if x[0]==2: x[2]=95
pickle.dump(s,open("marks.dat","wb"))

Random number generator (simulate dice)
import random
print(random.randint(1,6))

Stack implementation using list
stack=[]
stack.append(10); stack.append(20)
print(stack.pop())

CSV file: store userid & password, search password
import csv
csv.writer(open("user.csv","w",newline="")).writerow(["101","abc"])
print(next((r[1] for r in csv.reader(open("user.csv")) if r[0]=="101"),"Not Found"))

Create student table
CREATE TABLE student(roll INT, name VARCHAR(20), marks INT);
INSERT INTO student VALUES (1,'Ram',90),(2,'Mina',85),(3,'Raju',70);

ALTER TABLE
ALTER TABLE student ADD age INT;
ALTER TABLE student MODIFY marks FLOAT;
ALTER TABLE student DROP age;

UPDATE
UPDATE student SET marks=95 WHERE roll=1;

ORDER BY
SELECT * FROM student ORDER BY marks ASC;
SELECT * FROM student ORDER BY marks DESC;

DELETE
DELETE FROM student WHERE marks<80;

GROUP BY (min, max, sum, count, avg)
SELECT name, MIN(marks), MAX(marks), SUM(marks),
COUNT(*), AVG(marks) FROM student GROUP BY name;

Python + SQL Integration
import sqlite3 as s
c=s.connect("stud.db").cursor()
c.execute("SELECT * FROM student"); print(c.fetchall())

===============================================================
20 MORE SUGGESTED QUESTIONS WITH ANSWERS
===============================================================

1. Count number of words in a file
f=open("data.txt")
print(len(f.read().split()))

2. Copy lines that start with a vowel
fin=open("data.txt"); fout=open("vowel.txt","w")
for l in fin:
    if l[0].lower() in "aeiou": fout.write(l)

3. Count spaces, digits, special characters
t=open("data.txt").read()
spaces=t.count(" ")
digits=sum(c.isdigit() for c in t)
special=sum(not c.isalnum() and not c.isspace() for c in t)
print(spaces, digits, special)

4. Append text to file
with open("data.txt","a") as f:
    f.write("New line added\n")

5. Store dictionary in a binary file
import pickle
d={"roll":1,"name":"Ram"}
pickle.dump(d,open("dict.dat","wb"))

6. Read binary & print names only
import pickle
data=pickle.load(open("stud.dat","rb"))
for n,r in data: print(n)

7. Count records in binary file
import pickle
print(len(pickle.load(open("stud.dat","rb"))))

8. Write list to binary file
import pickle
pickle.dump([10,20,30],open("num.dat","wb"))

9. Read binary file & print each item
for x in pickle.load(open("num.dat","rb")):
    print(x)

10. Create CSV with header
import csv
w=csv.writer(open("emp.csv","w",newline=""))
w.writerow(["id","name"])
w.writerow([1,"Amit"])

11. Read CSV and print rows
import csv
for r in csv.reader(open("emp.csv")):
    print(r)

12. Search in CSV
print(next((r for r in csv.reader(open("emp.csv")) if r[0]=="1"),"Not Found"))

13. Append row in CSV
import csv
csv.writer(open("emp.csv","a",newline="")).writerow([2,"Neha"])

14. Random OTP (4 digits)
import random
print(random.randint(1000,9999))

15. Implement queue
q=[]
q.append(1); q.append(2)
print(q.pop(0))

16. SQL – Create table product
CREATE TABLE product(id INT, name VARCHAR(20), price INT);

17. SQL – Insert values
INSERT INTO product VALUES (1,'Pen',10),(2,'Book',50);

18. SQL – Select price > 20
SELECT * FROM product WHERE price>20;

19. SQL – Increase all prices by 10
UPDATE product SET price=price+10;

20. SQL – Delete price < 15
DELETE FROM product WHERE price<15;

===============================================================
50 MORE NEW QUESTIONS WITH ANSWERS
===============================================================

TEXT FILE HANDLING (1–10)

1. Count lines in file
f=open("data.txt")
print(sum(1 for _ in f))

2. Print first 5 lines
f=open("data.txt")
for i in range(5):
    print(f.readline(),end="")

3. Replace spaces with underscores
open("out.txt","w").write(open("data.txt").read().replace(" ","_"))

4. Extract numeric words
t=open("data.txt").read().split()
nums=[w for w in t if w.isdigit()]
print(nums)

5. Word frequency
from collections import Counter
print(Counter(open("data.txt").read().split()))

6. Longest word
words=open("data.txt").read().split()
print(max(words,key=len))

7. Copy lines > 20 chars
fin=open("data.txt"); fout=open("long.txt","w")
for l in fin:
    if len(l)>20: fout.write(l)

8. Count specific word
print(open("data.txt").read().split().count("India"))

9. Print lines containing “Python”
for line in open("data.txt"):
    if "Python" in line: print(line,end="")

10. Reverse content of file
t=open("data.txt").read()
open("rev.txt","w").write(t[::-1])

===============================================================
BINARY FILE HANDLING (11–20)
===============================================================

11. Store numbers in binary
import pickle
pickle.dump([1,2,3,4],open("num.dat","wb"))

12. Sum numbers from binary
import pickle
print(sum(pickle.load(open("num.dat","rb"))))

13. Search name in binary
import pickle
names=pickle.load(open("names.dat","rb"))
print("Found" if "Raju" in names else "Not Found")

14. Store employee records
import pickle
e=[["Amit",101,50000],["Neha",102,60000]]
pickle.dump(e,open("emp.dat","wb"))

15. Display salary > 55000
import pickle
for n,i,s in pickle.load(open("emp.dat","rb")):
    if s>55000: print(n)

16. Add record to binary
import pickle
d=pickle.load(open("emp.dat","rb"))
d.append(["Rohit",103,45000])
pickle.dump(d,open("emp.dat","wb"))

17. Delete student by roll
import pickle
s=pickle.load(open("stud.dat","rb"))
roll=2
s=[x for x in s if x[1]!=roll]
pickle.dump(s,open("stud.dat","wb"))

18. Update salary
import pickle
data=pickle.load(open("emp.dat","rb"))
for e in data:
    if e[0]=="Neha": e[2]=70000
pickle.dump(data,open("emp.dat","wb"))

19. Count records
import pickle
print(len(pickle.load(open("emp.dat","rb"))))

20. Print roll numbers
import pickle
for n,r in pickle.load(open("stud.dat","rb")):
    print(r)

===============================================================
CSV FILE HANDLING (21–30)
===============================================================

21. Create student CSV
import csv
w=csv.writer(open("stud.csv","w",newline=""))
w.writerow([1,"Ram"]); w.writerow([2,"Mina"]); w.writerow([3,"Raju"])

22. Print names
import csv
for r in csv.reader(open("stud.csv")):
    print(r[1])

23. Count rows
import csv
print(sum(1 for _ in csv.reader(open("stud.csv"))))

24. Search name by roll
import csv
print(next((r[1] for r in csv.reader(open("stud.csv")) if r[0]=="2"),"Not Found"))

25. Append row
import csv
csv.writer(open("stud.csv","a",newline="")).writerow([4,"Rita"])

26. Copy rows where roll > 2
import csv
fin=csv.reader(open("stud.csv"))
fout=csv.writer(open("out.csv","w",newline=""))
for r in fin:
    if int(r[0])>2: fout.writerow(r)

27. Count names starting with R
import csv
print(sum(1 for r in csv.reader(open("stud.csv")) if r[1].startswith("R")))

28. CSV to list of dicts
import csv
data=[{"roll":r[0],"name":r[1]} for r in csv.reader(open("stud.csv"))]
print(data)

29. CSV to text file
import csv
f=open("out.txt","w")
for r in csv.reader(open("stud.csv")):
    f.write(" ".join(r)+"\n")

30. Sort CSV by name
import csv
rows=list(csv.reader(open("stud.csv")))
rows.sort(key=lambda x:x[1])
csv.writer(open("sorted.csv","w",newline="")).writerows(rows)

===============================================================
STACK, QUEUE, RANDOM (31–40)
===============================================================

31. Queue using list
q=[]; q.append(10); q.append(20)
print(q.pop(0))

32. 5 random numbers 100–200
import random
print([random.randint(100,200) for _ in range(5)])

33. Random name selection
import random
names=["Ram","Mina","Raju"]
print(random.choice(names))

34. Shuffle list
import random
l=[1,2,3,4,5]; random.shuffle(l); print(l)

35. Menu-driven stack
stack=[]
while True:
    ch=int(input("1 Push 2 Pop 3 Exit: "))
    if ch==1: stack.append(input("Enter: "))
    elif ch==2: print(stack.pop())
    else: break

36. Check if stack empty
stack=[]; print("Empty" if not stack else "Not Empty")

37. Random password (8 chars)
import random,string
pwd="".join(random.choice(string.ascii_letters+string.digits) for _ in range(8))
print(pwd)

38. Priority queue
pq=[1,4,2]; pq.append(3); pq.sort()
print(pq.pop(0))

39. 20 coin tosses
import random
res=[random.choice(["H","T"]) for _ in range(20)]
print(res.count("H"))

40. Max element in stack
stack=[3,1,9,5]; print(max(stack))

===============================================================
SQL QUESTIONS (41–50)
===============================================================

41. Create teacher table
CREATE TABLE teacher(id INT, name VARCHAR(20), subject VARCHAR(20));

42. Insert records
INSERT INTO teacher VALUES(1,'Asha','Math'),(2,'Ravi','Physics');

43. Display Physics teachers
SELECT * FROM teacher WHERE subject='Physics';

44. Change subject
UPDATE teacher SET subject='English' WHERE id=1;

45. Count teachers per subject
SELECT subject, COUNT(*) FROM teacher GROUP BY subject;

46. Create marks table
CREATE TABLE marks(roll INT, subject VARCHAR(20), marks INT);

47. Marks > 80
SELECT * FROM marks WHERE marks>80;

48. Max marks per subject
SELECT subject, MAX(marks) FROM marks GROUP BY subject;

49. Delete marks < 35
DELETE FROM marks WHERE marks<35;

50. Order by marks
SELECT * FROM marks ORDER BY marks DESC;

===============================================================
END OF COMPLETE TXT FILE
===============================================================

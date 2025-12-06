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

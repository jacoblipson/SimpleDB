## Jake's Take: Thumbtack's Simple Database challenge

This challenge (detailled fully by Thumbtack 
[here](https://www.thumbtack.com/challenges/simple-database)) required me to 
implement a database capable of supporting a number of simple commands (get, 
set, unset, etc) in addition to nesting and rolling back transaction blocks. A 
number of these commands were expected to boast an average runtime of O(log n). 
I chose to use Python 3 to solve this problem.

### How to run
This program can be run in two ways: passing a file to standard input, or 
interactively. The only dependency is Python 3, available 
[here](https://www.python.org/downloads/).
* Method 1: ```python3 simple_db.py < test_file.txt```  
* Method 2: ```python3 simple_db.py```

### Some Implementation Thoughts
The Database: I thought that the choice to use a dict was pretty clear: fast,
lightweight, and we immediately have an average run time of O(1) for our GET,
SET, and UNSET actions.

Value Counts: The NUMEQUALTO operation requires us to know how many instances of
each value exist in our database. Rather than iterate across the entire database
when we receive this command (a solution that takes O(n) time - more than we are 
allotted), we use a separate dict to store this info. This dict takes the 
values in the database as its keys, and these keys map to the count of each 
value. This increases our memory costs, but allows us to perform this command in
O(1) time.

Transaction Commands: My initial approach to remembering database states outside
of nested transaction blocks was to store a copy of the database and a copy of 
the values count dictionary in our history arrays when we entered a new block.
However, the copy method has O(n) runtime, which does not accomplish our goal 
for the BEGIN method. Instead, after a bit of experimentation, I decided to 
insert empty dicts into our history arrays when we enter a new transaction block.
Then, as we overwrite our database within the block, we log what the values and 
counts were before this command. This allows us to execute BEGIN in O(1) time. 
Then, if we go to ROLLBACK, we simply iterate across the original values and 
counts and apply them. ROLLBACK therefore takes O(m) time, where m is the number
of commands executed in the nested block. COMMIT takes O(1) time, as the only
thing left to do is forget our history!

# Part 1: Routing
Besides baseball, McDonald’s, and reality TV, few things are as canonically American as hopping in the car for an old-fashioned road trip. We’ve prepared a dataset of major highway segments of the United States (and parts of southern Canada and northern Mexico), including highway names, distances, and speed limits; you can visualize this as a graph with nodes as towns and highway segments as edges. We’ve also prepared a dataset of cities and towns with corresponding latitude-longitude positions. These files should be in the GitHub repo you cloned in step 0. Your job is to implement algorithms that find good driving directions between pairs of cities given by the user.

Supervised by **David Crandall** Code by **Dhaval Niphade**

# Part 2: Team Assignments using Preferences
You can assume every student fills out the survey exactly once. Ideally, student preferences would be compatible with each other so that the group assignments would make everyone happy, but inevitably this is not possible because of conflicting preferences. So instead, being selfish, the course staff would like to choose the group assignments that minimize the total amount of work they’ll have to do. They estimate that:
•	They need k minutes to grade each assignment, so total grading time is k times number of teams.
•	Each student who requested a specific group size and was assigned to a different group size will complain to the instructor after class, taking 1 minute of the instructor’s time.
•	Each student who is not assigned to someone they requested will send a complaint email, which will take n minutes for the instructor to read and respond. If a student requested to work with multiple people, then they will send a separate email for each person they were not assigned to.
•	Each student who is assigned to someone they requested not to work with (in question 4 above) will request a meeting with the instructor to complain, and each meeting will last m minutes. If a student requested not to work with two specific students and is assigned to a group with both of them, then they will request 2 meetings.
The total time spent by the course staff is equal to the sum of these components. Your goal is to write a program to find an assignment of students to teams that minimizes the total amount of work the course staff needs to do, subject to the constraint that no team may have more than 3 students.

Supervised by **David Crandall** Code by **Zoher Kachwala**

# Part 3: 15 Puzzle
Consider a variant of the 15-puzzle, but with the following important change. Instead of sliding a single tile from one cell into an empty cell, in this variant, either one, two, or three tiles may be slid left, right, up or down in a single move.
The goal is to find a short sequence of moves that restores the canonical configuration (on the left above) given an initial board configuration. Write a program called solver16.py that finds a solution to this problem efficiently using A* search. 

Supervised by **David Crandall** Code by **Melita Dsouza**

# Repository Setup Instructions
The course's *source* repository (located at `https://github.com/Make-School-Courses/CS-2-Tweet-Generator`) contains course materials including the schedule, class topics, tutorial milestones, challenges, starter code, unit tests, slides, and links to resources.
It will be continuously updated throughout the course, so you will need to regularly *pull* from it to get new materials.
(Note that you cannot *push* to the course's source repository.)
However, you can *fork* it to create a copy and push code to your own fork.

**Important:**
Please follow these instructions *exactly* to correctly set up your fork of this repository. If you skip a step or do them out of order, it may not work.

1. Fork the course's source repo on GitHub to create your own copy of it on your GitHub account, which should also be named `CS-2-Tweet-Generator`

1. Visit your fork on GitHub and clone *that* repo onto your local computer:
`git clone https://github.com/<your-username>/CS-2-Tweet-Generator.git`

1. Push once to link your local repo to your *remote* forked GitHub repo with:
`git push -u origin master`

1. Each time you've completed a challenge, you should *commit* your work. When you want to share code for review, *push* it to your remote GitHub repo with:
`git push` (the `-u` in the previous command lets you omit `origin master`)

1. Add this course's source repo as another *remote* to your local repo with:
`git remote add course https://github.com/Make-School-Courses/CS-2-Tweet-Generator.git`

1. When you want to access new course materials, first be sure you've committed and pushed your recent work (run `git status` to check) and then *pull* from the course's source repo with:
`git pull course master`

1. To earn credit towards your streak for commits to this repo, you'll need to create another repo on GitHub named `Tweet-Generator` (no `CS-2-` prefix) and **do not** initialize it with a ReadMe.

1. Add that new GitHub repo as another URL to the `origin` remote on your local repo with:
`git remote set-url --add origin https://github.com/<your-username>/Tweet-Generator.git`

1. Verify that the `origin` remote has two distinct URLs with `(push)` after them with:
`git remote -v`

1. Now, after each time you complete a challenge and *commit* your work, you can *push* it to both remote GitHub repos with one simple command:
`git push`

# ARCHIVE - CS 2: Tweet Generator: Text Processing & Probability

## NOTE: This repo is no longer maintained

## Course Schedule

**Course Dates:** Monday, October 23 – Friday, December 8, 2017 (6 weeks)

**Class Times:** Tuesday & Thursday 2-4pm or 4–6pm (12 class sessions)


| Class |         Date          |                  Topics                  |
|:-----:|:---------------------:|:----------------------------------------:|
|   1   |  Tuesday, October 24  | [Strings & Random Numbers](Class1.md)    |
|   2   | Thursday, October 26  | [Histogram Data Structures](Class2.md)   |
|   3   |  Tuesday, October 31  | [Probability & Sampling](Class3.md)      |
|   4   | Thursday, November 2  | [Flask Web App Development](Class4.md)   |
|   5   |  Tuesday, November 7  | [Application Architecture](Class5.md)    |
|   6   | Thursday, November 9  | [Generating Sentences](Class6.md)        |
|   7   |  Tuesday, November 14 | [Arrays & Linked Lists](Class7.md)       |
|   8   | Thursday, November 16 | [Hash Tables](Class8.md)                 |
|   9   |  Tuesday, November 28 | [Algorithm Analysis](Class9.md)          |
|  10   | Thursday, November 30 | [Higher Order Markov Chains](Class10.md) |
|  11   |  Tuesday, December 5  | [Regular Expressions](Class11.md)        |
|  12   | Thursday, December 7  | Parsing & Tokenization     |


## Repository Setup Instructions

Please follow [these instructions](Setup.md) exactly to set up your fork of this repository.

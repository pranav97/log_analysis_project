log_analysis_project
-
I wrote all the code in the same file. The point of the project is to make psql do all the heavy lifting and let python 
just do the printing. The code itself is pretty short, execute the query and print the result. 

#### Details about the project
The database is a PostgreSQL database for a fictional news website. 

The tables in this project are:
- articles - The articles table has all the articles texts and the title and an
author number which is looked up in the authors database.
- authors - The authors table describes the names of the authors and has a 
foreign key of authors.id with the articles table.
- logs - Some of the "hits" were status 200 - Ok and the others were errors 
404\. The goal of the last question was the find the percent of successful 
"hits".


Running instructions:
-

### Requirements


- If you already have psql installed.


1. Python2.*
2. PostgreSQL
3. psycopg2

This link over [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdta/newsdata.zip)
will take you to a zipped version of the file. Unzip this.

From the command line, navigate to the directory containing newsdata.sql.
Import the schema and data in newsdata.sql to the news database by typing: psql -d news -f newsdata.sql
 
- If you don't have psql and would like to give vagrant a try or have that you 
can also use the vagrant file (to automatically acquire the database
and the dependencies for this which is just psycopg2 which is the database api
that I have used here and python2.*)
1. Vagrant
2. VirtualBox

###Running Instructions
```
python popular_articles.py
```

The output from the program is stored in ```output.txt```

The sql file that was added to psql to get this program going is stored in 
```newsdata.sql``` which can be unzipped from the download from the link 
above. Or from the vagrant file that I have provided in this repo.

This data is not owned by me but by Udacity. I only used it to learn about joins, subqueries and other psql intricacies. 

This is how I solved the questions in this question set.


#### Q1. What are the most popular three articles of all time? 

Steps to get the best articles:
1) Look at the logs and determine the pages that get the most hits.
2) Join with the articles table to get the titles using || operator

#### Q2. Find out the authors that 

Steps to get the best authors:
1) Look at the logs, and aggregate over the author using another join on the authors table from the previous query
2) Join to the authors table on the authors tables id to get the author's name

#### Q3. On which days did more than 1% of requests lead to errors? 

Steps to get the days
1) Use date(time) to find out the date that they are talking about
2) group by date and then by status code
3) make sure that the number of errors are greater than 1%

There are 3 subqueries in the last one, might not be the best way to solve it but it definitely works.


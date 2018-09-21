### log_analysis_project

I wrote all the code in the same file. The point of the project is to make psql do all the heavy lifting and let python 
just do the printing. The code itself is pretty short, execute the query and print the result. 
```
# Running instructions:
python popular_articles.py
```

The output from the program is stored in ```output.txt```

The sql file that was added to psql to get this program going is stored in ```newsdata.sql```

*can not store in git because its too large sorry

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


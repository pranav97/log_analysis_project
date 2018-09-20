### log_analysis_project

I wrote all the code in the same file. The point of the project is to make psql do all the heavy lifting and let python 
just do the printing. The code itself is pretty short, execute the query and print the result. 
```
# Running instructions:
python popular_articles.py
```



#### Q1. What are the most popular three articles of all time? 

Steps to get the best articles:
1) Look at the logs and determine the pages that get the most hits.
2) Join with the articles table to get the titles using || operator

#### Q2. Find out the authors that 

Steps to get the best authors:
1) Look at the logs, and aggregate over the author using another join on the authors table from the previous query
2) Join to the authors table on the authors tables id to get the author's name

#### Q3.
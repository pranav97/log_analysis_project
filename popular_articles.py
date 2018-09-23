#!/usr/bin/env python

import psycopg2

# change this to the database being imported
conn_string = "dbname=news"


def execute_query(query):
    """
    execute the query and returns the results as a list of tuples.

    https://en.wikipedia.org/wiki/Don%27t_repeat_yourself Never repeat yourself.

    args:
      query - (string) an SQL query statement to be executed.

    returns:
      A list of tuples containing the results of the query.
    """
    try:
        db = psycopg2.connect(conn_string)
        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        db.close()
        return rows
    except psycopg2.Error as e:
        print e.pgerror
        print e.diag.message_detail
        sys.exit(1)


def get_popular_articles():
    """
    Sum up the individual hits on each unique article.

    Using a string concatenation in sql using the || operator to join
    articles.slug and log.path we are able to figure out the names of the
    articles's names

    :return: print the most popular articles
    """
    # I found a website that makes sql commands that I type look professional
    #     like this one http://www.dpriver.com/pp/sqlformat.htm
    q = """
    SELECT articles.title,
               Count(path)
        FROM   log
               JOIN articles
                 ON '/article/'
                    || articles.slug = log.path
        GROUP  BY articles.title
        ORDER  BY Count(path) DESC
        LIMIT  3;
    """
    rows = execute_query(q)

    for title, times in rows:
        print "'{}' - {} visits.".format(title, times)


def get_popular_authors():
    """
    Sum up the hits on all the articles and group by author and find the best.

    We take the join from earlier and join it to another table, this one is
    called authors, this join is pretty straight forward and can be done with
    the authors.id = articles.author
    :return:
    """
    q = """
    SELECT authors.name,
    Count(*)
    FROM   ((articles
             join authors
               ON articles.author = authors.id)
            inner join log
                    ON log.path = '/article/'
                                  || articles.slug)
    GROUP  BY authors.name
    ORDER  BY Count(path) DESC;
    """
    rows = execute_query(q)
    for author, visits in rows:
        print "'{}' - {} total visits.".format(author, visits)


def get_error_days():
    """
    Find out days in which error rate was greater than 1%.

    inner most query gets the total
    2nd inner most query gets the error rate every single day
    last select is just filtering the error rate by the 1.00% threshold

    :return:
    """
    q = """
    SELECT To_char(day, 'FMMonth DD, YYYY'),
        Cast (failrate AS DECIMAL(10,2))
    FROM   (SELECT totaltable.total,
                   Count(status)
                   AS
                          failed,
                   Date(time)
                   AS day,
                   ( ( Cast (Count(status)
                    AS DECIMAL) / totaltable.total ) * 100 )
                   AS
                          failrate
            FROM   log
                   JOIN (SELECT Count(Date(time)) AS total,
                                Date(time)        AS day
                         FROM   log
                         GROUP  BY Date(time)) AS totaltable
                     ON totaltable.day = Date(time)
            WHERE  status = '404 NOT FOUND'
            GROUP  BY Date(time),
                      status,
                      totaltable.total) AS failtable
    WHERE  failrate > 1.0;
    """
    rows = execute_query(q)
    for date, err_p in rows:
        print "{} - {}% error ".format(date, err_p)


if __name__ == '__main__':
    get_popular_articles()
    print "____"
    print "____"
    get_popular_authors()
    print "____"
    print "____"
    get_error_days()
    print "____"
    print "____"

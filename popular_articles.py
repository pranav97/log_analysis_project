
import psycopg2


def get_popular_articles():
    """
    The logs table stores the visits themselves from the users. We need to count each distinct path and compile a list
    of the most visited articles
    :return: print the most popular articles
    """
    db = psycopg2.connect("dbname=news")
    """ 
    Using a string concatenation in sql using the || operator to join articles.slug and log.path we are able to figure
    out the names of the articles's names
    """
    cur = db.cursor()
    # I found a website that makes sql commands that I type look professional like this one
    # http://www.dpriver.com/pp/sqlformat.htm
    cur.execute(
        """
            SELECT articles.title,
                   Count(path)
            FROM   log
                   JOIN articles
                     ON '/article/'
                        || articles.slug = log.path
            WHERE  log.path LIKE '/article/%'
            GROUP  BY articles.title
            ORDER  BY Count(path) DESC
            LIMIT  3;  
        """
    )
    rows = cur.fetchall()
    for title, times in rows:
        print("'{}' - {} visits.".format(title, times))
    cur.close()
    db.close()


def get_popular_authors():
    """
    We take the join from earlier and join it to another table, this one is called authors, this join is pretty straight
    forward and can be done with the authors.id = articles.author
    :return:
    """
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    cur.execute(
        """
            SELECT authors.name,
            Count(*)
            FROM   ((articles
                     join authors
                       ON articles.author = authors.id)
                    inner join log
                            ON log.path = '/article/'
                                          || articles.slug)
            WHERE  log.path LIKE '/article/%'
            GROUP  BY authors.name
            ORDER  BY Count(path) DESC;  
        """
    )
    rows = cur.fetchall()
    for r in rows:
        print("'{}' - {} total visits.".format(r[0], r[1]))
    cur.close()
    db.close()


def get_error_days():
    """
    This function will
    :return:
    """
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()

    # inner most query gets the total
    # 2nd inner most query gets the error rate every single day
    # last select is just filetering the error rate by the 1.00% threshold
    cur.execute(
        """
            SELECT To_char(day, 'Month DD, YYYY'),
                Cast (failrate AS DECIMAL(10,2))
            FROM   (SELECT totaltable.total,
                           Count(status)
                           AS
                                  failed,
                           Date(time)
                           AS day,
                           ( ( Cast (Count(status) AS DECIMAL) / totaltable.total ) * 100 )
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
    )
    rows = cur.fetchall()
    for r in rows:
        print("{} - {}% error ".format(r[0], r[1]))
    cur.close()
    db.close()


if __name__ == '__main__':
    get_popular_articles()
    print("____")
    print("____")
    get_popular_authors()
    print("____")
    print("____")
    get_error_days()
    print("____")
    print("____")

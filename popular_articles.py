
import psycopg2, re
# the logs table stores the visits themselves from the users. We need to count each distinct path and compile a most
# visited list first.


def counts_paths(print_visits=False):
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    cur.execute(
        """
        select path, count(path)
        from log 
        where path like '/article/%'
        group by path 
        order by count(path) desc 
        limit 3;
        """
    )

    rows = cur.fetchall()
    cur.close()
    if print_visits:
        print "\nRows: \n"
        for row in rows:
            print "{} was visited {} times".format(row[0], row[1])
    db.close()
    return rows


def get_popular_articles():
    db = psycopg2.connect("dbname=news")
    most_visited = counts_paths()
    for article in most_visited:
        # this line takes the article string from the path and extracts the critical part to search inside of the
        # articles database
        # re.search(r'/article/(.*)', "/article/candidate-is-jerk").groups()[0]
        cur = db.cursor()
        slug_to_search = re.search(r'/article/(.*)', article[0]).group(1)
        cur.execute(
            """
                select articles.title, authors.name
                from articles JOIN authors on (articles.author = authors.id)
                where articles.slug = '{}';
            """.format(slug_to_search)
        )
        title, author = cur.fetchall()[0]
        print("'{}' by '{}' was visited {} times".format(title, author, article[1]))


if __name__ == '__main__':
    get_popular_articles()















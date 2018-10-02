#!/usr/bin/env python3

from analyticsdb import *


def main():

    db = load_logs("news")
    c = db.cursor()
    t = "1. What are the most popular three articles of all time? \n"
    t += "\n".join("%s - %s Views " % (title, visits)for title, visits
                   in get_popular_articles(c))
    t += "\n\n2. Who are the most popular article authors of all time?\n"
    t += "\n".join("%s - %s Views " % (author, views)for author, views
                   in get_popular_authors(c))
    t += "\n\n3. On which days did more than 1% of requests lead to errors?\n"
    t += "\n".join("%s%% - %s " % (rate, date.strftime('%d, %b %Y'))for rate,
                   date in get_requests_errors(c))
    close_db(db)
    file = open('output.txt', 'w')
    file.write(t)
    file.close()


if __name__ == '__main__':
    main()

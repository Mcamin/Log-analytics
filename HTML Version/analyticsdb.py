#!/usr/bin/env python3
# "Database code" for the DB Forum.

import psycopg2


def get_popular_articles(c):
    # Get the 3 most popular articles:
    c.execute("select slugs.title,visited.visits from slugs,visited"
              "where visited.slug=slugs.slug limit 3;")
    return c.fetchall()


def get_popular_authors(c):
    # Get the 3 most popular Authors:
    c.execute("select slugs.author,sum(visited.visits) as views"
              "from slugs,visited where"
              "slugs.slug=visited.slug group by slugs.author order by"
              "views desc;")
    return c.fetchall()


def get_requests_errors(c):
    # Get the date and  error rates which are  higher than 1%:
    c.execute("select rate,date"
              "from("
              "select cast((badrequests.badreq*100)/reqperday.numreq"
              "as decimal(10,2))"
              " as rate,reqperday.date"
              "from badrequests,reqperday"
              "where reqperday.date=badrequests.date)as ratetable"
              "where ratetable.rate>1;")
    return c.fetchall()


def load_logs(dbname):
    db = psycopg2.connect(database=dbname)
    return db


def close_db(db):
    db.close()

# Udacity Log Analytics Project

#### Requirements:

##### 1. install  <a target="_blank" href="https://www.python.org/">Python</a>
##### 2. install  <a target="_blank" href="https://www.postgresql.org/">PostgreSQL</a>
##### 3. unzip and load the data from  "newsdata.sql" provided in the project directory using the command:
    psql -d news -f newsdata.sql

##### 4. connect to the database:
    psql -d news;

##### 5. execute the following queries to create the required views :
    create view visited as select (Replace(path,'/article/','')) as slug,(count(*))
    as visits from log where path like '%article%' and Status='200 OK' Group by
    path order by visits desc;

    create view slugs as select name as author,articles.title ,articles.slug
    from authors,articles where authors.id=articles.author;

    create view badrequests as select cast(count(*) as decimal(10,2))as badreq,
    date(time) as date from log where status<>'200 OK' group by date order by date desc;

    create view reqperday as select count(*) as numreq, date(time) as date
    from log group by date order by date desc;

##### 5. Run analytics.py and open <a target="_blank" href="http://localhost:8000/">localhost</a>
    You can download the results by clicking on download

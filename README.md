# Udacity Log Analytics Project

#### Instructions:

##### 1. install  <a target="_blank" href="https://www.python.org/">Python</a>

##### 2. install  <a target="_blank" href="https://www.postgresql.org/">PostgreSQL</a>

##### 3. unzip and load the data from <a target="_blank" href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">newsdata.sql</a> in the database using the  following command:

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

* ###### The Plain Text Version folder contains the scripts that output a text file containing the results. To get the output, just run the analytics.py. the output will be created in the same directory.  

* ###### The Html  Version folder contains the scripts that output an HTML Page containing the results and a download button that generate the output as a text file when clicked. just run the analytics.py and open <a target="_blank" href="http://localhost:8000/">localhost</a>. Once clicked on the download button, the output will be created in the same directory.

######The command to run the programm is the following:  
     python analytics.py

##### Table Representation

<br/>
    **** Articles Table *****

| Column | Type                     |
|--------|--------------------------|
| author | integer                  |
| title  | text                     |
| slug   | text                     |
| lead   | text                     |
| body   | text                     |
| time   | timestamp with time zone |
| id     | integer                  |
<br/>
**** Authors Table *****

| Column | Type    |
|--------|---------|
| name   | text    |
| bio    | text    |
| id     | integer |

<br/>
**** Log Table *****

| Column | Type    |
|--------|---------|
| path   | text    |
| ip    | inet    |
| method | text |
| status | text |
| time     | timestamp with time zone |
| id     | integer |

##### Views Representation
<br/>
**** Visited View *****

| Column | Type    |
|--------|---------|
| slug   | text    |
| visits    | bigint|

<br/>
**** Slugs View *****

| Column | Type    |
|--------|---------|
| author   | text    |
| title    | text|
| slug    | text|
<br/>
**** badrequests View *****

| Column | Type    |
|--------|---------|
| badreq   | numeric(10,2)|
| date    | date|

<br/>
**** reqperday View *****

| Column | Type    |
|--------|---------|
| numreq   | bigint |
| date    | date|

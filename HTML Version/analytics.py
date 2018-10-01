#!/usr/bin/env python3


from flask import Flask, Response, stream_with_context

from analyticsdb import *


app = Flask(__name__)

errorRate = '''\
<div class="m-t-20">
  <div class="d-flex no-block align-items-center">
    <h3>%s&#37;</h3>
    <div class="ml-auto">
      <span>%s</span>
    </div>
  </div>
  <div class="progress">
    <div class="progress-bar progress-bar-striped" role="progressbar"
         style="width: %s%%" aria-valuenow="10" aria-valuemin="0"
         aria-valuemax="100">
    </div>
  </div>
</div>
'''
popularAuthors = '''\
<div class="comment-widgets scrollable">
  <div class="d-flex flex-row comment-row m-t-0">
    <div class="p-2"><img src="static/assets/images/users/1.jpg"
      alt="user" width="50" class="rounded-circle"></div>
    <div class="comment-text w-100">
      <h3 class="font-medium">%s</h3>
      <div class="comment-footer">
        <button type="button" class="btn btn-cyan btn-sm">%s Views</button>
      </div>
    </div>
  </div>
</div>
'''
popularArticles = '''\
<li class="d-flex no-block card-body">
  <div>
    <h3><a href="#" class="m-b-0 font-medium p-0">%s</a></h3>
  </div>
  <div class="ml-auto">
    <div class="text-right">
      <h5 class="text-muted m-b-0">%s</h5>
      <span class="text-muted font-16">Views</span>
    </div>
  </div>
</li>
'''
HTML_WRAP = '''\
<!DOCTYPE html>
<html dir="ltr" lang="en">

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Log Analytics Project - Udacity">
  <meta name="author" content="Ahmed Amine Mchayaa">
  <link rel="icon" type="image/png" sizes="16x16"
  href="static/assets/images/favicon.png">
  <title>Log Analytics Project - Udacity</title>
  <link href="static/dist/css/style.min.css" rel="stylesheet">
</head>

<body>
  <!-- ============================================================== -->
  <!-- Preloader - style you can find in spinners.css -->
  <!-- ============================================================== -->
  <div class="preloader">
    <div class="lds-ripple">
      <div class="lds-pos"></div>
      <div class="lds-pos"></div>
    </div>
  </div>
  <!-- ============================================================== -->
  <!-- Main wrapper - style you can find in pages.scss -->
  <!-- ============================================================== -->
  <div id="main-wrapper">
    <!-- ============================================================== -->
    <!-- Topbar header - style you can find in pages.scss -->
    <!-- ============================================================== -->
    <header class="topbar" data-navbarbg="skin5">
      <nav class="navbar top-navbar navbar-expand-md navbar-dark">
        <div class="navbar-header" data-logobg="skin5">
    <!-- ============================================================= -->
    <!-- Logo -->
    <!-- ============================================================= -->
          <a class="navbar-brand" href=".">
            <!-- Logo icon -->
            <b class="logo-icon p-l-10">
                          <img src="static/assets/images/logo-icon.png"
                          alt="homepage" class="light-logo" />
                      </b>
            <!--End Logo icon -->

            <!-- Logo text -->
            <span class="logo-text">
                           <!-- dark Logo text -->
                           <img src="static/assets/images/logo-text.png"
                           alt="homepage" class="light-logo" />

                      </span>
          </a>
    <!-- ============================================================= -->
    <!-- End Logo -->
    <!-- ============================================================= -->
        </div>

        <div class="navbar-collapse collapse" id="navbarSupportedContent"
             data-navbarbg="skin5">
    <!-- ============================================================= -->
    <!-- toggle and nav items -->
    <!-- ============================================================= -->
          <ul class="navbar-nav float-left mr-auto">
            <li class="nav-item d-none d-md-block">
              <a class="nav-link sidebartoggler waves-effect waves-light"
              href="javascript:void(0)" data-sidebartype="mini-sidebar">
              <i class="mdi mdi-menu font-24"></i></a></li>
          </ul>
        </div>
      </nav>
    </header>

    <aside class="left-sidebar" data-sidebarbg="skin5">
      <!-- Sidebar scroll-->
      <div class="scroll-sidebar">
        <!-- Sidebar navigation-->
        <nav class="sidebar-nav">
          <ul id="sidebarnav" class="p-t-30">
            <li class="sidebar-item">
              <a class="sidebar-link waves-effect waves-dark sidebar-link"
              href="." aria-expanded="false">
                        <i class="mdi mdi-view-dashboard"></i>
                        <span class="hide-menu">Dashboard</span></a></li>
          </ul>
        </nav>
        <!-- End Sidebar navigation -->
      </div>
      <!-- End Sidebar scroll-->
    </aside>

    <!-- ====================================================== -->
    <!-- Page wrapper  -->
    <!-- ====================================================== -->
    <div class="page-wrapper">
      <!-- ==================================================== -->
      <!-- Bread crumb and right sidebar toggle -->
      <!-- ==================================================== -->
      <div class="page-breadcrumb">
        <div class="row">
          <div class="col-12 d-flex no-block align-items-center">
            <h4 class="page-title">Dashboard</h4>
            <div class="ml-auto text-right">
              <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                  <li class="breadcrumb-item">
                    <a href=".">Home</a></li>
                  <li class="breadcrumb-item active"
                      aria-current="page">Dashboard</li>
                </ol>
              </nav>
            </div>
          </div>
        </div>
      </div>
      <div class="container-fluid">
        <!-- ===================================================== -->
        <!-- Start Page Content -->
        <!-- ===================================================== -->
        <div class="row">
          <!-- Column -->
          <div class="col-lg-12">
            <div class="card card-hover">
              <button type="button" class="col-lg-12 box bg-cyan text-center"
              onclick="window.location.href='/getTextFile'">
              <h3 class="text-white">Download</h3>
              </button>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="card">
              <div class="card-body">
                <h4 class="card-title">Popular Authors</h4>
              </div>
              <div class="comment-widgets scrollable">
                <!-- Authors go here -->
                %s
              </div>
            </div>
            <!-- Card -->
          </div>
          <div class="col-md-6">
            <!-- card new -->
            <div class="card">
              <div class="card-body">
                <h4 class="card-title m-b-0">Popular Articles</h4>
              </div>
              <ul class="list-style-none">
                <!-- Articles go here -->
                %s
              </ul>
            </div>
            <!-- card -->
            <div class="card">
              <div class="card-body">
                <h4 class="card-title m-b-0">Error Rate</h4>
                <!-- Error Rate goes here -->
                %s
              </div>
            </div>
          </div>
        </div>
      </div>
      <footer class="footer text-center">
        All Rights Reserved by Matrix-admin. Designed and Developed by
        <a href="https://wrappixel.com">WrapPixel</a>.
      </footer>
    </div>

  </div>
  <script src="static/assets/libs/jquery/dist/jquery.min.js"></script>
  <script src="static/dist/js/jquery.ui.touch-punch-improved.js"></script>
  <script src="static/dist/js/jquery-ui.min.js"></script>
  <!-- Bootstrap tether Core JavaScript -->
  <script src="static/assets/libs/popper.js/dist/umd/popper.min.js"></script>
  <script src="static/assets/libs/bootstrap/dist/js/bootstrap.min.js"></script>
  <!-- slimscrollbar scrollbar JavaScript -->
  <script src="static/assets/libs/perfect-scrollbar/dist/perfect-scrollbar
  .jquery.min.js">
  </script>
  <!--Wave Effects -->
  <script src="static/dist/js/waves.js"></script>
  <!--Menu sidebar -->
  <script src="static/dist/js/sidebarmenu.js"></script>
  <!--Custom JavaScript -->
  <script src="static/dist/js/custom.min.js"></script>
  <!-- this page js -->
  <script src="static/assets/libs/moment/min/moment.min.js"></script>
  <script src="static/dist/js/pages/calendar/cal-init.js"></script>

</body>

</html>
'''

Authors = ""
Articles = ""
Rates = ""


@app.route('/')
def main():
    """Main page of the forum."""

    db = load_logs("news")
    c = db.cursor()
    Rates = "".join(errorRate % (rate, date.strftime('%d, %b %Y'), rate)
                    for rate, date in get_requests_errors(c))
    Authors = "".join(popularAuthors % (author, views)for author, views
                      in get_popular_authors(c))
    Articles = "".join(popularArticles % (title, visits)for title, visits
                       in get_popular_articles(c))
    html = HTML_WRAP % (Authors, Articles, Rates)
    close_db(db)
    return html


@app.route('/getTextFile')
def getTextFile():
    db = load_logs("news")
    c = db.cursor()
    t = "1. What are the most popular three articles of all time? \n"
    t += "\n".join("%s - %s Views " % (author, views)
                   for author, views in get_popular_authors(c))
    t += "\n\n2. Who are the most popular article authors of all time?\n"
    t += "\n".join("%s - %s Views " % (title, visits)
                   for title, visits in get_popular_articles(c))
    t += "\n\n3. On which days did more than 1% of requests lead to errors?\n"
    t += "\n".join("%s%% - %s " % (rate, date.strftime('%d, %b %Y'))
                   for rate, date in get_requests_errors(c))
    close_db(db)
    print(t)
    return Response(
        stream_with_context(t.encode(encoding='UTF-8', errors='strict')),
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=Results.txt"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

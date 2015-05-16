<% from time import gmtime, strftime %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <title>Pick Stuff 4 Me!</title>

    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
    <script type="text/javascript" src="/static/jquery.cookie.js"></script>
    <script type="text/javascript" src="/static/ps4m.js"></script>
    <link rel="stylesheet" href="/static/ps4m.css?version=3" type="text/css" />

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> 
  </head>

  <body onLoad="init()">

    <div id="header">
      <a href="/"><h1>Pick Stuff 4 Me!</h1></a>
    </div>


    ${self.body()}


    <div id="footer">
       % if (not advice is None):
       We learns what you like!  If you like something, click "More".  If don't like something, click "Less".<br />
       <br />
       New links are added every eight hours.<br />
       <br />
       % endif
       Feedback and questions are welcome. Email: admin@ps4m.com
    </div>


    <!-- sign-up/login lighbox -->
    <div class="lightboxBackdrop"></div>
    <div class="lightbox">
      <div class="lightboxSpacer"><div class="lightboxClose">x</div></div>
      <div class="signUp" style="float:left; width: 50%; border-right: 2px solid #D3D3D3; padding: 0 0 0 20px;">
	<h3>CREATE A NEW ACCOUNT</h3>
	  <ul>
	    <li><label>username:</label>
	      <input name="newAccount-username" type="text"></li>
	    <li><label>password:</label>
	      <input name="newAccount-password" type="password"></li>
	    <li><label>verify password:</label>
	      <input name="newAccount-password2" type="password"></li>
	    <li><span id="createAccountErrorMsg"></span></li>
	    <li><button onClick="createAccount()">create account</button></li>
	  </ul>
      </div>
      <div class="login" style="float:left; padding: 0 0 0 30px">
	<h3>LOGIN</h3>
	  <ul>
	    <li><label>username:</label>
	      <input name="logIn-userName" type="text"></li>
	    <li><label>password:</label>
	      <input name="logIn-password" type="password"></li>
	    <li><span id="loginErrorMsg"></span></li>
	    <li><button onClick="logIn()">login</button></li>
	  </ul>
      </div>
    </div>

  <!-- Items picked at: ${strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())}  -->
  </body>
</html>

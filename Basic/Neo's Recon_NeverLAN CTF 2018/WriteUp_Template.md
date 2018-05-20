# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

http://yocchin.hatenablog.com/entry/2018/03/04/200300

# Title

[//]: <> (题目)

Neo's Recon

The best place to learn about Neo is on our website. But what is that in the corner

# Content

[//]: <> (WriteUp内容)


NeverLAN Neoで検索すると、https://neverlanctf.com/Neoというページがある。

ソースを見ると、右下の位置にsubmitのinputがあり、hidden属性もある。

```html
<form method="post" action="ZD.php">
	<input type="submit" name="submit" value="submit" class="alt" style="position:fixed;bottom:0;right:0;padding:0;z-index:99999;background:transparent;">
	<input type="hidden" name="riddle" maxlength="3" minlength="3" value="">
	<!-- 
		Finding this form is half the challenge. Now can you solve the riddle?
		Edit the input field above to solve the challenge.
			type:text; maxlength: 3; minlength: 3;  
			solve -> riddle: To grow your mental perception and increase your cognizance.  Never let him stop growing. Never let him die; 
	-->
</form>
```

mental perception cognizance で検索すると ken というあやしい人名がある。

```html
$ curl https://www.neverlanctf.com/ZD.php -d 'riddle=ken'
<!DOCTYPE html>
<html lang="en" itemscope itemtype="http://schema.org/WebPage">
    <head>
        <meta name="robots" content="noindex, nofollow">
        <meta name="Author" content="Neo">
    </head>
    <body>
        <style>body{text-align:center;}</style>
        <h1>Congratulations, You Solved It</h1>
        <p><!--Throughout this event you may have noticed (or didn't notice) that we occationally personified the word ken to symbolize the strive for education.<br/>--> He[Ken] is used as a representation of the constant growth of mental perception. His friendship is your search for knowledge and his death your final attempt to reach new boundries.<br/> To never let Ken die you must never stop trying to learn, never give up on knowledge.<br/> Finding Ken is to find the joy in education. Learn to love learning and your ken will never stop growing.<br/> This event was created to help those who have not yet found their ken realize how important knowledge is.<br/>Even if computer programming or scripting is not your thing, I would hope you continue your search to find something you love to learn about.</p>
        <br/>
        <br/>
        <br/>
        <p>Ken, as described by dictionary.com, is "knowledge, understanding, or cognizance; mental perception"</p>
        <h5>ok, here's you flag{dat_ken_though}</h5>
        <!--<h5>For more fun, try the challenges on my cohorts' pages, you might even learn some more about them</h5>-->
    </body>
</html>
```

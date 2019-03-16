# MISC-waf

**Honeypot**
*Principals*

The goal of this configuration is to block multiple attacks performed from the same source, then transparently redirect the attacks to a VirtualHost that will:
- Always respond with a status code 200 (OK) to any request
- Deliver a page content with multiple signatures recognized by vulnerability scanners
The result of this operation is that any vulnerability scanner attacking your website will be flooded with false positives information in the report.

The setup of this configuration requires the following steps:

**Nikto (vulnerability scanner) signatures extraction**
```
$ git clone https://github.com/sullo/nikto.git
$ cd nikto/program/databases
$ cat * | awk -F"," '{print $6}' | sort | uniq | sed -e 's/"//g' -e 's/\\s/ /g' -e 's/\\//g' > /var/www/html/index.html
```

**Honeypot Apache VirtualHost preparation**

The VirtualHost will be configured to bind a specific port on the local server (WAF), this could also be configured on a third party server.
The file to use is honeypot_vhost.conf ut should be included to 

/etc/httpd/conf.d/honeypot_vhost.conf*:
```
Listen 127.0.0.1:5001
<VirtualHost 127.0.0.1:5001>
  # This will allow only GET/POST to be able to deliver content
  RewriteEngine on
  RewriteCond %{THE_REQUEST} !^(POST|GET)\ /.*\ HTTP/1\..$
  RewriteRule .* - [F]

  # Any request coming here is "transparently" proxified to index.html and keep the original URL called
  RewriteCond %{REQUEST_URI} !^/index.html
  RewriteRule .* http://127.0.0.1:5001/index.html?$1 [P,QSA] [R=200]
  SecRuleEngine Off
  
  # The index.hrml file is hosted in this directory
  DocumentRoot /var/www/html/

  # Logging is activated
  ErrorLog "/var/log/httpd/honey_error_log"
  CustomLog "/var/log/httpd/honey_access_log" combined
  
  # This can only be accessed by itself (a local WAF request in this setup)
  <Directory /var/www/html/>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
  </Directory>
</VirtualHost>
```

**ModSecurity configuration**

The ModSecurity configuration for transparent redirection in case of multiple attacks is located in *waf-honeypot.conf*, in our configuration it must be included in 
 "/etc/httpd/waf/vhosts/waf-bigcorp.ch.conf"

Using:
```
...
Include waf-honeypot.conf
...
```

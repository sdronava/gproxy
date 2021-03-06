FROM ubuntu 
RUN apt-get update \
    && apt-get install -y \
        apache2 \
        apache2-dev \  
        python2.7 \
        python-pip \
    && pip install django \
    && pip install requests \
    && pip install --upgrade google-api-python-client \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /installdata/src
   
CMD "ufw" "allow" "'Apache'"

######  WSGI ######################

#Build wsgi Module /usr/lib/apache2/modules/mod_wsgi.so
#TODO: Optimize the image size to see if just copying the .so is enough. Can avoid python2.7 and all these steps.
#Steps, courstesy: http://modwsgi.readthedocs.io/en/latest/user-guides/quick-installation-guide.html
WORKDIR /installdata/src 
ADD https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.4.tar.gz /installdata/src
RUN    tar xvfz 4.6.4.tar.gz  
WORKDIR /installdata/src/mod_wsgi-4.6.4
RUN  ./configure && make && make install 

#Enable/activate wsgi
WORKDIR /etc/apache2/mods-available
COPY apache/conf/mods-available/wsgi.load /etc/apache2/mods-available
RUN  rm /etc/apache2/sites-available/*.conf  
RUN  a2enmod wsgi 


######  Configure Apache to Serve The Django App ######################
COPY apache/conf/apache2.conf /etc/apache2/apache2.conf
COPY apache/conf/ports.conf /etc/apache2/ports.conf
COPY gproxy/mysite /var/www/mysite 

#Enable SSL
RUN a2enmod ssl
COPY apache/certs/server.crt /etc/ssl/certs/server.crt
COPY apache/certs/server.key /etc/ssl/private/server.key
CMD  "chmod" "640" "/etc/ssl/private/server.key"
CMD  "chmod" "644" "/etc/ssl/certs/server.crt"
COPY apache/conf/conf-available/servername.conf /etc/apache2/conf-available
COPY apache/conf/sites-available/localhost.conf /etc/apache2/sites-available
RUN  a2enconf servername
RUN  a2ensite localhost

#RUN  "groupadd" "varwwwusers"
#RUN  "adduser" "www-data" "varwwwusers"
#RUN  "chgrp" "-R" "varwwwusers" "/var/www/mysite/cache"
#RUN  "chmod" "-R" 760 "/var/www/mysite/cache"



#Clean up.
RUN rm -rf /installdata/*

# Expose Apache
EXPOSE 8080
 
# Launch Apache
WORKDIR /var/www/mysite
CMD ["/usr/sbin/apache2ctl", "stop"]
CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]


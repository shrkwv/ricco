#!/bin/bash
# Fix permissions on bind-mounted ricco source so Apache (www-data) can read it
chmod -R a+rX /var/www/html/ricco-web/ricco
exec apache2-foreground

# MISC-waf

*Description*

This repository provides all the configuration and scripts described in the MISC (May 2019) French Magazine regarding ModSecurity deployment.

**Directories content**
- The *etc/* contains configuration files described (bigcorp.ch.conf, waf-bigcorp.ch.conf, 00-crs-setup.conf etc.)
- The *honeyweb/* directory contains configurations files and instruction to implement the Honeypot with transparent redirection use case described in the article
- The *tool/* contains a script which could be used to extract Mod Security information from Apache error_log, this could be useful for statistical analysis about blocking and false positives handling

### Hexlet tests and linter status:
[![Actions Status](https://github.com/AnastasiaTimoshe/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AnastasiaTimoshe/python-project-83/actions)
[![Page_analizer CI](https://github.com/AnastasiaTimoshe/python-project-83/actions/workflows/page_analyzer.yml/badge.svg)](https://github.com/AnastasiaTimoshe/python-project-83/actions/workflows/page_analyzer.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/bbd27598e212c93e0e5a/maintainability)](https://codeclimate.com/github/AnastasiaTimoshe/python-project-83/maintainability)


### Description
Page Analyzer is a site that analyzes websites for SEO suitability.  
The application uses Python library 
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse websites.  
The results of the checks of websites are parsing: 
h1, title, description and code status.
The application saves all of it on a remote postgres database.

### Demonstration

The production version of the app is available at the following URL:
[Page analyzer](https://page-analyzer-app-6hjz.onrender.com)

## Install

Prepare the database.

Before installing the application, prepare your environment variables:
+ **DATABASE_URL** - variable for connecting to the database.
+ **SECRET_KEY**

After cloning from GitHub, run the commands:
+ *make build*
+ *make start*

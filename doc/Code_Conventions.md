# Code/Naming Conventions

## Python3/Flask

### PEP8

* import
    * always use absolute package path but relative path for current directory

### Route and methods

Basic Structure

| Route | Function method | HTTP method |
|-------|-----------------|-------------|
| / | index | GET |
| /index | index | GET |
| /<unique_id> | detail | GET |
| /create | index | GET/POST |
| /edit/<unique_id> | edit | GET/POST |
| /delete/<unique_id> | index | GET/POST |

## HTML

### Jinja2 Template

## Javascript

## IDE

I use PyCharm Professional Edition in order to develop the Flask application. I recommend to use PyCharm Community Edition if your budget doesn't allow.

I utilize the following features not provided by PyCharm Community Edition:

* Jinja2 Template engine syntax highlight
* Database/SQL

However, it is not a huge barrier to develop the Flask application. Most of configurations are up to developers because Flask is a micro web framework.

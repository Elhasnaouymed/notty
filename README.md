> This app is not yet completed !

# Notty

Simple multi-user Notes web app, for educational purposes.

- Has a REST API built using [flask-restx](`https://github.com/python-restx/flask-restx`).
- Has a Front-End build using [Bootstrap](https://getbootstrap.com/).
- Has a [WYSIWYG](https://itsfoss.com/open-source-wysiwyg-editors/) feature *(Nice Formatting of Notes)*.
- Very Readable/Commented code.
- Not Licensed ! Free to use and Redistribute.

## Structure:

```shell
├── app.py                    # the __main__
│ 
├── app_root                  # contains the Flask app
│   │
│   ├── api                   # contains the REST API resources
│   │   ├── __init__.py           # has the API factory method
│   │   ├── note_resource.py
│   │   └── user_resource.py
│   │
│   ├── blueprints            # holds the Blueprints for the web app
│   │   ├── __init__.py           # not important
│   │   ├── auth.py
│   │   └── views.py
│   │
│   ├── __init__.py           # has the Flask app factory method
│   ├── config.py             # has the Config class for the Flask app
│   ├── constants.py          # where all the constants defined 
│   ├── exceptions.py         # full of error types        
│   ├── jinja.py              # inits jinja shell context processor and filters
│   ├── models.py             # all Database models (no SQLAlchemy object is in here)
│   │
│   ├── static                # the static directory
│   └── templates             # templates directory
│       ├── components            # html components like nav-bars and footers
│       ├── pages                 # visual pages
│       └── roots                 # base pages to inherit from jinja
│
├── encryptman                # handles encryption/hashing/encoding
│   └── __init__.py
│
├── logs                      # automatically created to hold app logs
│   ├── log-24-01-18.log
│   ├── log-24-01-21.log
│   ├── log-24-01-25.log
│   ├── log-24-01-26.log
│   └── log-24-01-27.log
│
└── README.md                 # this damn file
```

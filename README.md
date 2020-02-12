#Mailing Logins

###Descripion


###Step taken to create this

First I needed to create python script that could interact with existing database. I used [sqlacodegen 2.1.0](https://pypi.org/project/sqlacodegen/).
It is very simple to use
```
pip3 install sqlacodegen
 ```
And then connect it to existing database to create a mapping as python3 code.
```
sqlacodegen mysql+oursql://user:password@localhost/dbname >> models.py
```
You just need to fill the user, password and database parts with your own settings. As you can see from the codeblock I'm using mysql.
Also I'm using the >> to pipe it to python file.

### Less secure apps ON
To use this script you must enable Less secure apps from your gmail user security settings.

### Unlock captcha
Because this is running on the server I needed to unlock captcha otherwise you get an error i
This is how I unlocked it. First I needed to log in with my gmail account. Then I navigated to this link
```
https://accounts.google.com/unlockcaptcha
```

### conf_env.py file
Includes all the configurations for the project.

```
conf_env.py:

    class Config:
        GMAIL_SERVER = ""
        SENDER_EMAIL = ""
        RECEIVER_EMAIL = ""
        EMAIL_PASSWORD = ""
        DB = ''


```




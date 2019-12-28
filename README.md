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






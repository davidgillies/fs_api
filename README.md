# Form System Extension 

This version is based on an external relational database that is connected to Django only in the local_settings.py and not in Django settings.  It doesn't use models by default.  It uses an example MySQL database and Fenland.xml which matches up to the database data.  You can change both local_settings varaibles for DATABASE and XML_FILE and it should all work right away as long as your XML file's field names match your database names.

This project works with a local database that needs to set up in MySQL.  There are Dumps of the test database included in the project.  If you set up a MySQL database using the dumps and change the DATABASE setting in fs_proj/fs_renderer/local_settings.py then hopefully it should all work when installed.

WARNING: Probably best to use a virtualenv!!

    pip install -r requirements.txt
    
No need for a migration.  Import the database dumps into your MySQL server and change the fs_proj/fs_renderer/local_settings.py file's DATABASE setting to match with your database details.  It is set to use the Fenland.xml file that comes with it and this matches to the database.  It should work then.

Visit http://localhost:8000/html/0/ # should be a search page.  Stick in 'Gill', it return a few names and link to the next section.


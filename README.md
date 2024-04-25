# COP4521 Quiz Website (Group 9)
Group members: 
Benjamin Horvath (@borvath), Brian Nelson (@bnnelson1), Aditi Anandijawala (@aditianan), Shelley Bercy (@shell155), Anoushka Ahuja (@aahuja82)

### Topic: Quiz Application
This project is a quiz application where users can view and create quizzes.

### Libraries  Used

- bcrypt (v. 4.1.2)
- blinker (v. 1.7.0)
- click (v. 8.1.7)
- colorama (v. 0.4.6)
- Flask (v. 3.0.2)
- Flask-Bcrypt (v. 1.0.1)
- Flask-WTF (v. 1.2.1)
- itsdangerous (v. 2.1.2)
- Jinja2 (v. 3.1.3)
- MarkupSafe (v. 2.1.5)
- mysql-connector-python (v. 8.3.0)
- Werkzeug (v. 3.0.1)
- WTForms (v. 3.1.2)

The libraries used are also in requirements.txt and can be installed locally by using
`python3 -m pip install -r requirements.txt`

### Docker
Should you choose to use Docker for the application, note that docker-compose is required to build and run the containers.
Additionally, at least one modification will need to be made. In database.py, the value of the 'host' key for db_config
in connect_to_database() needs to be changed from 'localhost' to 'mysql-db' for the Flask app to connect to the MySQL container.
It is also possible the port numbers in docker-compose.yml will need to be changed but that depends on the host machine.

### Notes about User Interface
When registering and logging in, be sure to select the correct type of user/account from the dropdown.

When updating a user from the admin management page, clicking "update" should cause a basic form to appear above the table.
From there, the values in the input boxes can be edited and submitting should update the user data according to those values.

Quiz Creator: 
Buttons for adding questions and saving the quiz should be in the bottom left corner of the page.
The radio button next to an answer is how you mark an answer as the correct answer.
The 'X' next to an answer under the radio button is how you remove an answer.

### Other Features
There is also a review feature where users can rate quizzes that have been created.
Once logged in, this can be accessed by clicking the Ratings tab.
From there, at the top are dropdowns to select the course the quiz belongs to and the quiz itself and an input box to submit a short review.


### Separatation of Work

Ben was responsible for the database, authentication, and role based access part of the app, and had various other contributions to the project.
Brian was responsible for the admin side of the application and Docker. 
Shelley was responsible for the login page and ratings.
Aditi was responsible for quizzes and courses.
Anoushka was also responsible for quizzes.


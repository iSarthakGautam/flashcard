RUN THE CODE:

App:
1) To run the app run app.py It would automatically start the app on local host. 

2) Access the app in browser using the the host address (typically local host).

3) If you don't see any app running check the port on which flask app is running on your machine.

API:
1) You can tests api when app.py is running OR You can explicitly run api.py after stopping app.py

2) Access the apitest.yaml file provided in the file.

3) Use this yaml in apps such as insomnia where you would get GUI to check the working of API's


In App Functionality:

1) A user can signup and get a new username of choice by clicking on create new account

2) If a new user is created, the user can now add words/deck by clicking on add/update/delete then clicking on add.

3) Every deck has unique name so to add another word in a deck one has to give exact name of the deck/language (Case sensitive)

4) There is a predefined user name → “qwe” that contains several decks so one can see the working of the app without adding words.

5) One can access card from a deck by clicking on the name of the deck in the table on the dashboard. A random card would be generated. To view the meaning of the card one has to hover over the card. The card would rotate and expose the meaning of the given word.

6) User can review the difficulty level of the word given and click next to get a new card. (Note: As the card is randomly generated  by Python's random module so it is possible that a card might repeat over several clicks. This thing vanishes as the size of the deck grows.) User can go to dashboard by clicking on Dashboard button

7) To update or delete a word, the user has to go to the dashboard then add/update/delete. Then, delete/update. Here a table containing all the words for the given user is shown. This is sorted and grouped by deck name. To update click on the update button in the row of the word to be updated. It would open a form that can be used to update a word or it’s meaning. Similarly you can delete the word using the delete button provided next to the update button.

8) You can access/update your profile by accessing the profile through the profile button given on the dashboard.

9) You can logout using the logout button. This would redirect you to the login page.



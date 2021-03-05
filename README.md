# MSP3 Movie Review Website

![Screenshot]()

This is the Website for [Movie Review](https://the-snap-movie-review.herokuapp.com/) which allows
users to search the database for movies and leave reviews of movies stored in the database. Useres will be able to register/login 
to manipulate the database by creating reviews/add movie titles, searching for movies, updating movies or delete reviews/movies 
they have inputted.  

## User Experience (UX)


**User stories**

**External User Goals:**
* I want to easily search the site for Movies that interest me.
* I want to be able to see key information regarding this movie.
* I want to be able to leave a review. 
* I would like to add missing movie titles.
* I want to be able to change or delete any reviews I have left.


**Site Owner's Goals:**
* I want the users to be able to navigate the site easily.
* I want the users to leave reviews on the site.
* I want the users to be able to follow a link to buy the movie. 


**Design**
*  Colour Scheme:

    The colours used throughout the app are Materialized colours
    - blue-grey darken-1 used for the background colour for cards and forms
    - teal lighten-1 was used for the Navbar and buttons.
    - blue-grey-text text-lighten-5 was used on all input fields on the forms.


*  Typography: 
    
    The Font Dosis was used from google fonts.
        
*  Imagery:  

    The main image has been chosen to be eye catching and clearly explains what the website is about.
    The images for the movies have been chosen  so users can identify the film on recognisable images. 
    
    
* Wireframes
[The Snap Wireframe](docs/MovieReview.pdf)
 

 ## Features

### Existing Features

*  Navbar - The Navbar allows users an easy navigation through the site for registered and non-registered users. 
*  Homepage - The homepage welcomes new users with a brief explination and offers the users to find a movie, register or log in. 
*  All Movies - The Movie Page displays all movies alphabeticaly as cards. The movie poster and the movie title are the main 
card content but when the card reveal is clicked the movie information is displayed and users can click on the more information 
to be directed to the movie details page.   
*  Search Bar - The search bar in the Movies page allows users to search for film titles, actors name or a directors name and returns
users query. The reset button removes users query and returns all movies. 
*  Movie Detail Page - The Movie details page can be accessed by all users via the card revealon the movies page. This page displays more 
information regarding the movie and shows all reviews of this movie and allows users to view the movie trailer. The close icon at top right 
allows users to close this view and return back to all movies.
*  Regiser - Each user has the opportunity to register an account and have access to additional features such as adding to favourites, editing, 
deleting and creating movies and the ability to add and delete reviews.
*  Add & Edit Movies - As part of the CRUD funtion required for this site, registered users
can create a new Movies by using the Add movie link in the Navbar. Users can update the movie details of the movies they 
have added using the visable link in the card reveal panel on the movie cards. 
*  Delete Movies - Another part of the CRUD function required users can delete the movie they 
have added by using the visable link in the card reveal panel on the movie cards.
*  Add Movie to Favourites - Registered users who are logged in will see the option to add a movie to their favourites by clicking the heart icon
on the movie details page.
*  Add Reviews - As part of the CRUD funtion required for this site, registered users
can create a review of the movies by using the Add Review link in the Navbar. these reviews are displayed in the movie details page and on the user profile page.
*  Delete Reviews - Another part of the CRUD function required users can delete any of their own reviews.
*  User Profile Page - The users profile page displays the username at the top of the page along with any reviews they have left and also any films added to their
favourites.

## Future Development
* Users ability to edit their profile page, change username and reset password.
* Return review rating value to 5 stars instaead of value.

 ## Technologies Used
 
 **Languages Used** 
- HTML
- CSS
- Python
 

**Frameworks, Libraries & Programs Used**
   
[Materialize](https://materializecss.com/):
 Materialize was used as an alternative to bootstrap and was used to ensure the site was responsive
 and 

[Font Awesome](https://fontawesome.com/):
 Font Awesome was used to provide the Icons throughout this website.

[Google Fonts](https://fonts.google.com/):
 Google fonts was used to import the font into the style.css file

[JQuery](https://jquery.com/):
 JQuery was used to run the scripts for the following:
 - to create a mobile sidenav
 - to activate the collapsible headers
 - to enable the drop down select options on the forms 
 - to change the rating value in the input to star rating
 - to enable the confirmation modal
 - to enable the datepicker input on forms
 - to add validation colour on input fields on the form

[Git](https://git-scm.com/): 
 Git was used by utilizing the Gitpod terminal to commit to Git and push to GitHub.

[GitHub](https://github.com/):
 GitHub was used to create a repository and store the code after it was pushed from Git.

[Heroku](https://www.heroku.com):
 Heroku was used to deploy my app.

[Balsamiq](https://balsamiq.com/):
 Wireframes were created using Balsamiq

[Pixabay](https://pixabay.com/):
 Pixabay was used to source the background imagery for the webpage.

[MONGODB](https://www.mongodb.com/):
 MongoDB was used to create and store data in my collection

[Flask](https://flask.palletsprojects.com/en/1.1.x/):
 Flask was used to create a base template that allowed us to Jinja for template inheritance and for-loops.

[YouTube](https://www.youtube.com/):
 YouTube was used to source the embeded movie trailers. 

[Giphy](https://giphy.com/):
 Giphy was used to source the images for the Error 403, 404, 410 & 500.html pages.

## Testing

The Freeformatter HTML Validator and W3C CSS Validator were used to validate every page of the project to ensure there were no errors in the project.

[CSS Validator](http://jigsaw.w3.org/css-validator/) - [Results]()

[HTML Validator](https://validator.w3.org/) - [Results]()


**Manual Tests for functionality of features**
    
* 

**Testing User Stories**

**External User Goals:**
    
* I want to easily search the site for Movies that interest me.
* I want to be able to see key information regarding this movie.
* I want to be able to leave a review. 
* I would like to add missing movie titles.
* I want to be able to change or delete any reviews I have left. 


**Site Owner's Goals:**
* I want the users to be able to navigate the site easily.
* I want the users to leave reviews on the site.
* I want the users to be able to follow a link to buy the movie. 

(a)  
![]()


## Bugs


## Deployment 

The project was deployed to [Heroku](https://dashboard.heroku.com/apps) Pages using the following steps...

1. 



## Credits

**Code**
* Error Pages - [Flask Pallets Projects](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/) was read to understand how to create
custom error pages.



**Content & Media**

- The Homepage background image was sourced from [Pixabay](https://pixabay.com/photos/starwars-fantasy-movie-figure-5355787/) and the authours was enriquelopezgarre 
- All other images are links to the url from google search for movie posters
- Giphy was used to source the Images on the error pages.


**Acknowledgements**

* My Mentor Aaron Sinnott for feedback
* Code Institute for training

 
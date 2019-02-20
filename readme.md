# User Profile Django
This is a simple django app that lets a user sign up and create a profile. The main goal was to get familiar working with forms in django and validating
form data. After making an account users can upload an image, create a simple profile and change their password.

## New Password rules
  *  Must be at least 8 charcters long
  *  Must contain both lower and upper case letters
  *  Must contain at least one number
  *  Can not contain the user's first or last name
  *  Can not contain the username associated with the account
  *  Must contain one of the following characters: @ ! $ # *

## Technologies Used
* django

# Cheers! The Drinks db

'Cheers!' is an app built on the Flask micro web framework and using MongoDB as the database. Its purpose is to provide users with a number of different types of (mainly alcoholic) drinks and cocktails.

My goal is to allow users to create drinks and cocktails using the information provided, as well as allowing them to add their own to share with others, and much more.

The deployed site can be found at [cheers-drinksdb.herokuapp.com](https://cheers-drinksdb.herokuapp.com)

## Jump To A Section

[UX](#ux) || [User Stories](#user-stories) | [Design](#design) | [Wireframes](#wireframes)

[Features](#features) || [Current Features](#current-features)  | [Planned Features](#planned-features)

[Technologies Used](#technologies-used) || [Languages](#languages) | [Libraries](#libraries) | [Tools](#tools) | [Hosting](#hosting)

[Testing](#testing) || [Testing Introduction](#testing-introduction) | [Code Validation](#code-validation) | [Responsiveness & Rendering](#responsiveness--rendering) | [Browser Compatibility](#browser-compatibility) | [Features Testing](#features-testing)

[Deployment](#deployment) || [Deployment To Heroku](#deployment-to-heroku) | [Local Deployment](#local-deployment)

[Credits](#credits) || [Content](#content) | [Media](#media) | [Acknowledgements](#acknowledgements)

## UX

The site itself follows standard web design conventions and therefore the layout and initial use of the site should be immediately recognisable to all but the most inexperienced of web users.

The landing page is used to tell the user this is a site about drinks. Thanks to the success of sites like the IMDB, many users now associate 'db' with database, so I felt the tagline 'The Drinks db' was clear enough to convey the sites purpose as part of the landing experience, but even for those who don't make that connection, it soon becomes clear when the home page loads.

### User Stories

#### As a user, I want to be able to:

- View a list of drinks for inspiration on what to make / drink

- Add drinks of my own [CREATE]

- Get instructions on how to make the drinks on this site [READ]

- Edit drinks I have submitted [UPDATE]

- Delete drinks I have submitted [DELETE]

- Easily see all of the drinks I have submitted

- See how popular the drinks I have submitted are by seeing which ones have been

	- Looked at the most

	- Added to the most users favorites list

	- Commented on the most

- Add drinks to a list of my favorites

- Comment on other user’s drinks, and reply to comments left by users for my drinks

- Choose whether to see one large list of all drinks available or filter those drinks in a way of my choosing - such as by category, glass type, or difficulty.

- Choose how the information is presented to me, for example:

	- Number of drinks per page

	- Sort by name, views, comments, favorites, difficulty, and date

	- Sort either ascending or descending

- Search the database for drinks that match key words of my choosing and order the results either based on their relevance to what I searched for, or some other criteria of my own choosing.

- Do this on any device and browser of my choosing and have the same experience, and access to the same data, regardless of device and browser type.

Most importantly, as a user I want to be able to do this with minimal effort. I want to instinctively know how to use the site, and not have to search for how to do something. I want it to just work, and not have to fight to make it work. Finally, above all else, I want to enjoy using the site.

#### As the site admin, I want to be able to:

- Build up a collection of drinks to continually provide the user with more choice on every visit, and to encourage them to return.

- Give users the ability to interact with each other through the comments to help build a community.

- Allow the users to personalise their own experience through the ability to display results how they choose and have their own section of the site (Account Page) that is all about them and their drinks.

Most importantly, I want the site to work and provide enjoyment for its users so that at a later date, once there is more content and an active user base, the site can be monetised.

### Design

#### Application Framework

When designing this project, the brief stated Flask must be used to run the application.

#### Database

For the database, I could choose between SQL or NoSQL, and I decided in this instance to use MongoDB. This decision was driven in the most part by my understanding that my next project states I must use SQL, therefore this was an opportunity to gain experience using a NoSQL database.

The database is made up of the following collections

##### categories

```

_id: <ObjectId()>

category: <string>

categoryDescription: <string>

```

##### difficulty

```

_id: <ObjectId()>

difficulty: <string>

```

##### drinks

```

_id: <ObjectId()>

name: <string>

category: <string>

userName: <string>

date: <date>

ingredients: <array>

0:<string>

1:<string>

2:<string>

....

instructions: <string>

difficulty: <string>

glassType: <string>

imageUrl: <string>

views: <Int32>

favoritesTxt: <array>

0:<string>

1:<string>

2:<string>

....

favorites: <Int32>

commentsTxt: <array>

0:<string>

1:<string>

2:<string>

....

comments: <Int32>

```

##### glass

```

_id: <ObjectId()>

glassType: <string>

```

##### quotes

```

_id: <ObjectId()>

difficulty: <array>

0:<string>

1:<string>

2:<string>

....

```

##### users

```

_id: <ObjectId()>

userName: <string>

password: <string>

favoritesTxt: <array>

0:<string>

1:<string>

2:<string>

....

```

Examples of the above in .json format can be found [here](documentation/schema).

#### CSS Framework

I chose Materialize as the CSS Framework. Having previously only really used Bootstrap I wanted to use a different one this time around more out of curiosity than anything else. Unfortunately, I felt I spent more time fighting Materialize than actually working with it, so the quest continues to find another CSS Framework for my next project.

Despite my struggles with Materialize, I was still able to produce a fully responsive site that works and displays well across all the most popular browsers and devices.

#### Color Scheme

For the color scheme, I initially went with a neon 80's style look, but it ended up looking more like a Myspace page from the mid 2000's. Instead, I went with a simple black and white approach, injecting color via the drink cards and labels. I did keep one neon effect, limiting its use to the landing page, nav bar, and drink card links.

#### Typography

The following fonts were used:

- [Grand Hotel](https://fonts.google.com/specimen/Grand+Hotel) was used for the full screen navigation elements.

- [Cormorant SC](https://fonts.google.com/specimen/Cormorant+SC) was used for h1 and h2 elements - mostly the display of drink names and section titles. The original plan was to use [Playfair Display SC](https://fonts.google.com/specimen/Playfair+Display+SC) but a display bug made within the font itself made this not an option. (The bug was when displaying the characters 'F' & 'I' together, it formed them in lowercase.)

- [Playfair Display](https://fonts.google.com/specimen/Playfair+Display) was used in the most part for smaller subheadings such as h3, h4 and h5 elements.

- Finally, [Muli](https://fonts.google.com/specimen/Muli) was used for h6 and p elements as I feel it's a nice, clean and easily readable font for general text, that pairs well with Playfair Display.

#### Icon Set

It seemed natural to use Materialize Icons with the Materialize framework, but I couldn't always find the right icon with Materialize. Rather than use 2 different sets, I decided instead to go with [Font Awesome](https://fontawesome.com/) for all the icons.

### Wireframes

Mock-ups were created early on in this project, before any code was committed. The early designs differ only slightly to the finished product, and in the most part, the final result has turned out very much as I originally envisioned.

You can view the wireframes for each page using the links below

- [Home Page - Guest / Non User](https://i.imgur.com/HI498hv.png)

- [Home Page - User Logged In](https://i.imgur.com/PAJoEjJ.png)

- [Search](https://i.imgur.com/UIyBcB4.png)

- [Account Page](https://i.imgur.com/2syYTs6.png)

- [Add Drink](https://i.imgur.com/V398o7i.png)

- [Edit Drink](https://i.imgur.com/zlJFrwt.png)

- [Login / Register](https://i.imgur.com/UV6dOtu.png)

Alternatively, you can download them all directly from [here](documentation/wireframes).

## Features

### Current Features

**Flashed Messages**

The app uses the flask flash method to communicate important events to the user. These are displayed at the top of each page, just below the navbar. The messages are contained within a black box which contrasts against the background so even if the user isn't looking for it, it is almost unmissable.

Once read, it can be easily dismissed by clicking the close button in the upper right of the box.

**Landing Page**

A simple landing page that contains the text "Cheers! The Drinks db" on top of a full screen image of some filled shot glasses. This makes the visitor aware that the drinks in question are alcoholic and as such the site is a database of alcoholic drinks, most likely spirits, given the contents of the image.

**Register A New Account**

Users can use the site as a guest, but certain features are unavailable unless logged in. There is no barrier to registering. Users provide a username of their choosing and a password, and if accepted, they are stored in the database.

When a user registers, assuming they pass the validation checks, they are automatically logged in and taken to the home page.

Data validation on the registration form checks to make sure the username is a minimum of 3, and maximum of 12 characters. There is a small 'i' icon next to the placeholder text which the user can hover over / click on for a tooltip explaining this.

The same applies to the password field, the only difference being a minimum of 5 and maximum of 15 characters are required.

If a user attempts to register with a name which has already been registered, the system flashes a message informing them of this, and to choose another.

If a user finds themselves at the register page but they intended to log in, there is a helpful link at the bottom of the form to redirect them to the log in page.

**Log In To An Account**

Much like the registration form, users can enter their username and password to log in to a previously created account. Data validation is in place to prevent submission of an empty input field and the app checks any details submitted against values held in the database.

Flashed messages are used to inform the user if they enter an incorrect username / password, or if the user they tried to log in with does not exist.

On successful log in to a previously registered account, the user is taken to the home page.

**Log Out**

Users can log out of their account at any point, using the link at the top right of the nav bar (or the bottom option on mobile). This clears the session variable that stores their username and returns them to the home page.

**Navigation**

The site provides two types of navigation depending on the current view width. On widths > 992px there is a fixed navigation bar at the top of the window. Its contents vary depending on whether or not a user is logged in and allows the user to access areas of the site they are allowed to.

On widths <993px the options remain the same, but they are instead accessed using a side navigation element which can be accessed through the traditional 'burger' icon at the top left or by swiping across from the left edge of the screen on mobile devices.

If the user is currently viewing a page that is listed within the nav bar, that element is highlighted to show the users current position within the site. If they are viewing a page that is not part of the nav bar, such as a specific drink, then there is no highlight.

**Browse Drinks**

From the homepage, the user can browse all the drinks currently in the database. Using materialize cards, individual drinks are displayed as an image with the drink name underneath.

Each card contains 3 labels which show the category, glass type, and difficulty of the drink. These are small, but still readable, and positioned in the top right of the card so as to interfere with the image as little as possible.

If the drink card is a drink which has been submitted by the user who is viewing it, an edit icon is displayed between the image and drink title, allowing the user to go direct to the edit screen for that particular drink, should they wish.

The cards have been kept intentionally simple so as to not overload the user with information, and instead let the images 'pop' and draw the user in.

Pagination options have been placed both before and after the drinks, making it easier for the user to move through the drinks.

**Suggested Drinks**

When a user is logged in, the home page can display some suggested drinks to the user. The criteria for display is to only show drinks not submitted by current user, to not show the same drink in this section, and to display a total of 4 drinks in a row.

If all of these conditions cannot be satisfied, then nothing will be shown.

**Browse Options**

On the home page, there is a ``browse`` button. Clicking this opens a box containing 3 tabs; category, glass type, and difficulty. This allows the user to browse the different categories, glasses, and difficulties and choose to view drinks only from one of these sections.

The categories have been divided into cards, each containing some text describing that particular category. Where there is too much text to display, the text has been truncated. The full text is shown on the individual category screen.

In the case of glass types, an image of each glass is provided to better help the user choose, especially as it is expected that not all users will be immediately familiar with what each glass looks like.

Even though the difficulty levels are quite self-explanatory, an image has been provided for each to give the user more of an idea as to the difficulty level of one versus the other.

Each type, when clicked, takes the user to a page that shows only drinks of the type chosen, and provides a way for the user to quickly filter the drinks without the need of using the search function.

**'Showing Only' Pages**

These pages are shown when the user chooses a particular drink category, glass type, or difficulty, from the browse tabs on the home page.

The layout of the resulting drinks is identical to that on the home page (and also the search page) so will be familiar to the user, but it contains just the drinks they have chosen to view.

It also contains the same sorting options as found on the home page.

**Sort Options**

Whenever drinks are displayed on the home page, search results page, or the 'showing only' pages, the user is given the option to sort the results in a way of their own choosing, rather than having to rely on how the site initially chooses for them.

The user has the option to sort the displayed drinks by:

- Drink Name

- How many times it has been viewed

- How many comments it has received

- How many times it has been favorited

- How difficult the drink is to make

- The date it was added to the database

Additionally, the user also has the option to sort these results either ascending or descending.

On top of this, the user can also choose how many drinks they want to see on each page at once. They can select from, 4, 8, 12, or even every drink in the database, all in one go!

Users can also sort by 'relevance' - which is explained in more detail as part of the search page functionality.

Finally, session variables are used to store the users sort preferences so these settings persist across the whole site. Whenever a user sorts their drinks / results, they always start from where they last left off.

**Search**

Users can search for specific keywords, filter by category, glass type, or difficulty, or any combination of these.

When the results are displayed, they are displayed in the same familiar format as how drinks are displayed on the home and 'showing only' pages.

If as part of the search, the user has entered keywords to search on, when the results are displayed, the cards will contain a small white box in the lower left corner with a % value inside. This is the drinks relevance to the search term and allows the user to select the ``sort results by relevance first`` option. This is only available when a keyword has been used and allows the user to order the results by most relevant first. If 2 or more drinks have the same score, they are then secondary sorted by name, views, comments, etc - whichever the user specified.

The score is calculated by using MondoDB text indexes. A text index on the drinks collection was created using

```

db.drinks.createIndex(

{

category: "text",

difficulty: "text"

glassType: "text"

ingredients: "text"

name: "text"

userName: "text"

}

)

```

This created text indexes for the above fields. No value was given for the weight of each index, which meant they all defaulted to 1 and carry equal significance when searching.

**Drink Page**

Each drink has its own page that contains all information relating to that drink. When a user clicks on a drink, this is the page they are taken to. It shows the name of the drink, along with the name of who submitted it, and when. If the user viewing is the user who submitted, they will have additional options here too, namely ``edit`` and ``delete``.

There is a picture of the drink, which can be clicked to provide a full screen version of the image, alongside the ingredients required to make this drink.

Further down are instructions on how to make the drink, as well as a picture and name of the glass it should be served in. There is also an ``extra info`` section that contains other relevant pieces of information such as number of views, category, and so on.

There is a ``favorites`` section that allows registered users (not the author) to add this drink to their favorites, and also a comments section, which allows registered users to share and discuss the drink.

Finally, as a way of adding something a little different to each page, there is a quote box. The database contains a collection of over 40 drinking related quotes, and a different one is displayed every page load.

**Add Drink**

Users, when logged in, can add their own drinks. The user is provided with a form to complete, and once submitted, creates the drink in the db, and takes the user to the drink page to view it. The system will flash a message to inform the user the drink was added successfully.

Data validation is used throughout to ensure the information is entered in the correct format, and the user will not be able to submit the form until all fields pass.

Once a user has completed a field, it will turn either green or red, and text of the same color will show underneath to guide the user. If the field has been completed correctly, the green text will state ``passed``. If the field has not been completed correctly then red text will state what the error is and how to rectify. Some examples being:

- Drink Name ``Name must be between 5 and 26 chars``

- Image Url ``Url must begin with http(s):// and be a minimum of 12 chars``

- Instructions ``Instructions length must be at least 5 chars``

- Ingredients & Measures ``Cannot be empty``

There is a tooltip letting users know, when entering instructions, to put each one in its own sentence. When displaying instructions on the drinks page, each instruction is separated by splitting the string at each '. ' (full stop and space).

The site doesn't currently host the images for drinks ( - on the planned features list) and instead stores the url of the image to display. If a user is adding a drink but doesn't have an image to use, they can click the '+' button at the end of the input field and it will populate the field with a link to a placeholder image. This avoids the individual drinks pages looking 'broken' if there is no image to display.

Each drink can have up to 10 measures and ingredients, but a minimum of 1. The page defaults to 4 but using the ``+`` and ``-`` icons the user can adjust the number of boxes to match the number of measures and ingredients they require.

**Edit Drink**

The edit drink form is identical in layout to the add drink form, and very similar in functionality.

The important differences from a UX perspective is the '+' icon is not present for the default image. As there will already be an image stored (even if only a placeholder) the user has the option to update with their own or keep the existing.

The number of measures and ingredients boxes shown match the number of measures and ingredients, as opposed to the default 4 with the add drink page.

Finally, there is a ``delete drink`` button, allowing the user to completely remove the drink from the database.

**Delete Drink**

If the user clicks the ``delete drink`` a popup modal will appear asking for confirmation and advising that this action cannot be undone. Should the user still choose to delete, the drink will be permanently deleted.

**'My Account' Page**

Each user has their own account page, which is used to store user specific information and stats.

Every account page, regardless of the user’s time on site and activity, will display a welcome message, along with some stats for the user and the site overall. It will show combined totals for views, favorites, and comments for all user submitted drinks. It will also show how many drinks are currently in the database, along with the total number of categories, types of glass, and levels of difficulty.

If the user has submitted drinks, it will also scan all these drinks and display the ones which have received the most views, comments, and additions to other users favorite lists.

Further down, the page shows all drinks submitted by the user in groups of 4 (or 8 if there are more than 21 total) and pagination options are provided to allow the user to browse.

Finally, the users favorite drinks are displayed. Any drinks the user has added to their favorites list will appear here, with pagination options provided if there are more than 4 in the list.

**Views**

Each drink keeps tracks of how many times it has been viewed. Views from the author do not count towards this total.

**Comments**

Users can leave comments on any drink in the database. Users can leave comments on their own drinks too, allowing them to engage in conversation with others about their own drinks.

Only registered users can leave comments - guests are told they must be logged in and the input field is disabled.

**Favorites**

All registered users have their own favorites lists. To add a drink to their favorites they just need to click the ``add favorite`` button on the drink page. Providing it isn't their own drink, and they are logged in, the drink is added to their favorites list.

A list of the users favorite drinks can be viewed from their account page.

### Planned Features

**Image Hosting**

Currently, images are stored by pointing to an external url and pulling the image from there. I plan to eventually add the option to allow the user to upload an image to the server instead as this will make it easier for the user, it will ensure more drinks have a proper image, and ultimately result in a better user experience.

**Security Log**

I want to add a log that initially stores every action that performs a write to the database, and eventually expand it to read actions too. The log will be a simple record that contains the username, date, time, action performed, and if it was successful or not.

It would also capture new user registrations, as this is the only database write action an unregistered user can undertake.

**Deleted Items**

When a drink is deleted it is gone forever. Instead, I'd like to have them stored in a deleted items list for review by an admin.

**Admin Panel**

To make managing the site easier, an admin panel will need to be added. Initially this will contain options such as reviewing logs, moderating comments, checking deleted items, and so on, but has the potential to contain so much more.

## Technologies Used

### Languages

- [HTML](https://html.spec.whatwg.org/multipage/) used as the markup language

- [CSS](https://www.w3.org/Style/CSS/) used to style the HTML

- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) used mostly for DOM manipulation

- [Python3](https://www.python.org/) used to run the backend application

### Libraries

- [Materialize](https://materializecss.com/) v1.0.0 used as the CSS framework for the project

- [Font Awesome](https://fontawesome.com/) v5.8.2 to provide the icon set

- [Google Fonts](https://fonts.google.com/) provided the fonts used throughout the project

- [jQuery](https://jquery.com/) is used to manipulate the DOM, for example buttons, and showing / hiding elements

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) v1.0.2 is the micro web framework that runs the application

- [PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) 2.3.0 was used to enable the python application to access the Mongo database

- [Jinja](https://jinja.palletsprojects.com/en/2.10.x/) v2.10.1 is the default templating language for flask and is used to display data from the python application in the frontend html pages

### Tools

- [AWS Cloud9](https://aws.amazon.com/cloud9/) is the IDE used to put all this together

- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) is the database used

- [MongoDB Compass](https://www.mongodb.com/products/compass) is an app that allowed me to access the database directly and perform CRUD operations separate to the project

- [Git](https://git-scm.com/) is used for version control

- [GitHub](https://github.com/) provides hosting for software development version control using Git

- [Imgur](https://imgur.com/) is used to host some image files externally.

- [Balsamiq](https://balsamiq.com/) was used to create the wireframes when initially planning this project

- [Photoshop](https://www.photoshop.com/) was used to edit and alter images as required

- [TinyJpg](https://tinyjpg.com/) was used to reduce the file size of .jpg's and .png's

### Hosting

- [Heroku](https://www.heroku.com/) is used to host the app

## Testing

### Testing Introduction

Most of the testing was completed by myself. The majority of which was manual testing during the development of the site with additional testing completed at the end, before this write up.

The python terminal and browser console were monitored throughout development to catch bugs and errors as they occurred.
The console does display a verbose message when navigating between pages. This is linked to the Materialize .js file so cannot be helped and doesn't impact the site in any way that I have been able to identify, and is therefore ignored. 
The Materialize devs are aware of it [here](https://github.com/angular/components/issues/4221) but the issue has been closed so it's safe to say the issue isn't going away soon.

Friends and family have also tested by creating accounts and using the site on their own devices. They have tested how the page displays, registered their own accounts, created their own drinks, added favorites, and left comments. I have removed all the content that was added as part of friends & family testing, partly due to it not always being of the same quality as the initial data I added, but also because when people are given a new toy, they tend to do silly things with it.

To test the site yourself, you can
- Browse as a guest, but with limited functionality.
- Create your own user. Do not use a password you use elsewhere as the passwords are not secure.
- Use an existing user to see how the app handles user drinks submissions for views, comments, favorites, etc. You can do this with:
	- Username: Kelly
	- Password: flare

If testing with user 'Kelly', for the benefit of other testers, please refrain from deleting any drinks. To test this aspect of the site, you can create and delete submissions with users you create yourself.

### Code Validation

#### HTML

All HTML was passed through the HTML validator at [validator.w3.org](https://validator.w3.org). Outside of errors thrown due to using the Jinja templating language, which are unavoidable given the nature of the project, everything came back fine.

#### CSS

The CSS style sheet was first passed through [Autoprefixer CSS online](https://autoprefixer.github.io/) to add required vendor prefixes for the last 4 versions of supported browsers.
It was then passed through [jigsaw.w3.org/css-validator/](https://jigsaw.w3.org/css-validator/) and returned with no errors, just warnings about the vendor prefixes which is normal as it doesn't recognise any of them.

#### JavaScript

The JS file was run through [jshint.com](https://jshint.com/) and outside of numerous instances of ``$`` being undefined due to using jQuery, there were no errors.

#### Python

The Python script was checked using [pep8online.com](http://pep8online.com/) and one warning is given ``no newline at end of file``. Within the IDE there is a blank line at the end, but this doesn't carry over to GitHub. Otherwise the script is fully PEP8 compliant.

### Responsiveness & Rendering

Chrome DevTools and physical devices were used throughout development for a number of purposes, one of which was to test the responsiveness and rendering across a range of sizes and devices. As issues were found they were either fixed at the time or noted and returned to later.

On touch devices, any button with a hover effect, keeps the effect until something else is pressed. Whilst not ideal behavour, it doesn't detract from the overall experience, and is something that can be changed at a later date.

The site has been tested successfully on the following devices,

- Windows 10 desktop at HD, QHD, and UWQHD on various browsers

- Apple Macbook - Safari browser

- Google Pixel 2XL - Chrome browser

- Apple iPhone 8S - Safari Browser

- iPad Mini - Safari Browser

### Browser Compatibility

The site has been tested successfully on the following desktop browsers,

- Chrome v76

- Firefox v68

- Opera v62

- Edge v42

- Safari v12

Even though the project isn't aiming to be compatible with Internet Explorer 11, I tested it to see how close it came and was surprised to see that aside from some minor rendering issues it actually works ok. It hasn't been tested extensively, but on the surface it is functional and could be used if it had to.

### Features Testing

Features were tested alongside the user stories to ensure the site was able to do what was intended, in the correct way, accurately, and without breaking. Most tests involved outputting print statements to the python console and using MongoDB Compass to check the data was as expected. In this section, I will detail what tests I carried out and for each feature, I will also identify which of the basic CRUD functions were tested.

#### Permissions & Access - CRUD operations tested: Read.

Depending on whether the user is viewing the site as a guest, or logged in as a registered user, the options available differ.

The table below show what each user type should and shouldn't be able to do, and tests were conducted to ensure this was the case.

| User Type | Home | Search | Register | Log In | Log Out | Account | Add Drink | Edit Drink | Delete Drink | Showing Only |
|-|-|-|-|-|-|-|-|-|-|-|
|Guest|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:x:|:x:|:x:|:x:|:x:|:heavy_check_mark:|
|Registered User|:heavy_check_mark:|:heavy_check_mark:|:x:|:x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark::one:|:heavy_check_mark::one:|:heavy_check_mark:|

:one: Confirmed that only the user who submitted the drink is able to edit / delete.

In the most part this testing took the form of seeing if the required navigation options were available to the user, but I also tested by entering the url for the routes I wanted to access to make sure the app prevented unauthorised access.

#### Flashed Messages - CRUD operations tested: None.

When important information needs communicating to the user, flashed messages are used. To test, I performed the actions necessary to force a flashed message and confirmed it was displayed. All messages display when expected, close when clicked, and if not clicked, disappear when the user moves to another page.

#### Account Management - CRUD operations tested: Create & Read.

##### Register A New Account

Account creation was tested by creating 10 test accounts using different names and passwords, with a mix of upper / lower case, numbers and special characters. All accounts were created successfully.

##### Log In To An Existing Account

The accounts created as part of the previous test were used to test the log in functionality and I was able to log in with each of them.

##### Log Out

All accounts could also be successfully logged out. Print statements were used in the python console to confirm the username variable had been removed from the session.

#### Navigation - CRUD operations tested: None.

Navigation links for both desktop view, and the sidebar for smaller views were tested and all are confirmed as working as intended.

#### Suggested Drinks - CRUD operations tested: Read.

Suggested drinks should display only 4 drinks from other users with no repetition of drinks within the section. To test this was working as intended I created a user with 4 test drinks. All other drinks in the database at this point had been created by my main user.

When viewing as my user, the suggested drinks showed the 4 drinks created by the test user. I then deleted 1 of these drinks and refreshed. As expected, this section was now no longer displaying as there were not 4 unique drinks available to display.

I then created 5 more test drinks, bring the total to 8, and kept refreshing the page. Each refresh, the section displayed 4 of the 8 drinks in a seemingly random manner.

#### Browse Options - CRUD operations tested: Read.

The button was tested to confirm the section was shown / hidden as required on each press. The tabs were also tested to confirm they displayed the correct content each time. Finally, the links were tested to confirm they directed the user to the correct 'Showing Only' page for their selection.

#### 'Showing Only' Pages - CRUD operations tested: Read.

These pages were checked to ensure they only displayed drinks from the stated section. For example, if the user had chosen to see only drinks served in a shot glass, when viewing this page, I would check 2 things. Firstly, that the drink card labels showed only shot glasses, and secondly, I would open the drinks into their own tab, confirm the shot glass, then close.

Across all options for category, glass type, and difficulty I tested 2 choices from each section and confirmed a maximum of 5 drinks were correct. No issues were found.

#### Sort Options - CRUD operations tested: Read.

The button was tested to confirm the section was shown / hidden as required on each press. Users can sort by name, views, comments, favorites. difficulty, and date. They can also choose to sort ascending or descending. I tested in 2 ways.

Firstly, I accessed the cursor that was returned with the sort and used it to print the drink name and the field it was sorted on to the console so I could confirm the sort order.

Secondly, I would review the sort results from within the site itself and confirm they are correct.

I did this 20 times for each test. The sort always performed exactly as intended.

#### Search - CRUD operations tested: Read.

I tested the search functionality by searching for terms I knew did not exist, and confirmed no results were returned. I also searched for common terms, to ensure results weren't limited and all records were returned.

I created a test drink with random strings that were contained within various fields that I knew had been indexed and searched for these to ensure they were returned.

I also added random strings to fields I knew were not indexed, for example, the comments, and searched for this term to ensure nothing was returned.

I deleted the test drinks and searched again, to ensure the test strings within the indexed fields no longer returned any results.

I tested the search score results by creating drinks with certain words repeated multiple times to ensure they would be weighted heavily and would result in the highest score.

I searched on username to ensure drinks from the searched user were returned. I searched by ingredient, category, glass type, and difficulty to ensure these also returned results as expected.

I also discovered that on devices with limited height, when a user searches either by keyword or filter, the results are displayed below the search criteria (and sort options, if previously opened / selected) and this can mean the returned results are initially displayed off the screen. For users unfamiliar with the site, they could think nothing was returned. To fix this, when results are returned, the page will anchor to the #search-results section.

#### Add / Edit Drinks - CRUD operations tested: Create, Read, Update & Delete.

##### Add A Drink

With the exception of the first 4 drinks, all 96 (at time of writing this) drinks in the database were added using the ``Add Drink`` form that the users will use. The form works as intended. The data validation is solid and only accepts input in the correct format.

Any messages generated due to incorrect input are clear and intuitive.

##### Edit A Drink

This form was tested by editing test drinks, and also drinks added by other testers and no issues were found. The data validation is the same as ``Add Drink`` and works as it should.

##### Delete A Drink

This was tested by deleting my test drinks, and test drinks submitted by friends & family testing for me. When the delete button is pressed, a pop-up modal asks to confirm deletion. If a user selects cancel, they are taken back and I've confirmed the drink isn't deleted.

I've confirmed drinks are deleted by searching for them afterwards and also checking the database directly.

#### Individual Drinks Pages - CRUD operations tested: Read & Update.

##### The View Counter

Every time a drink is viewed, the view counter increases by 1. This was checked  by just accessing the page multiple times from different pages to confirm the counter was increasing both on screen and in the database.

Views from the drink author do not count so I also checked the counter didn't increase when doing the same actions as above whilst logged in as the author.

##### Leaving Comments

| User Type | Add Comments|
|-|-|
|Guest|:x:|
|Registered User| :heavy_check_mark:|

Comments can only be left by registered users so I first confirmed that when logged out, the comments input is disabled.

I then tested the comments by leaving comments on various drinks when logged in as both the author, and a different user.

All comments were recorded and displayed exactly as intended.

##### Adding / Removing Favorites

| User Type | Add / Remove Favorites
|-|-
|Guest|:x:|
| Drink Author| :x:|
|Registered User|:heavy_check_mark:|

Depending on the user type, this dictates whether or not a drink can be added to a favorites list.

Guests cannot have favorites, so I checked this by trying to add favorites as a guest and made sure they were unable to do so.

Registered users can add any drink to their favorites list, providing they are not the author of the drink they are trying to add.

This was tested by trying to add a drink to the favorites list of the author, which I was unable to do.

I tested the same with drinks not submitted by the author and they could be added / removed at will.

This was checked by viewing the users account page confirm the favorites list was updated accordingly. The individual drink page was also checked to confirm it showed the correct users as favorited and this was cross checked against the values in the database.

## Deployment

### Deployment To Heroku

The site has been deployed to [Heroku](https://www.heroku.com/) and the latest version can be found [here]([https://cheers-drinksdb.herokuapp.com/). The following steps were taken in order to deploy:

**AWS Cloud9 IDE**

- I prepared my code for deployment to Heroku by firstly removing my secret key. I created a different secret_key within .bashrc so I could still run the project from my own IDE

- I turned off Flask debugging by setting ``debug=False``

- I created a requirements file with the command ``sudo pip3 freeze --local > requirements.txt``. Unfortunately, AWS Cloud9 makes this list longer than it should be by adding everything that is installed to environments by default to this list too, so I went through and manually removed anything that wasn't required.

- A file named ``Procfile`` was created, containing a single line, ``web: python app.py`` to tell Heroku to run ``app.py`` on start-up.

- Once up to date, everything was pushed to GitHub master branch.

**Heroku**

- From the Heroku dashboard I created a new app, using the name ``cheers-drinksdb`` and set the region to Europe.

- In the settings tab I clicked ``reveal config vars`` and entered the required environment variables, which in this case were:

- IP ``0.0.0.0``

- PORT ``5000``

- MONGO_URI ``mongodb+srv://root:<password_removed>@myfirstcluster-fai9p.mongodb.net/drinksdb?retryWrites=true&w=majority``

- SECRET ``<secret key for flask session>``

- I made sure the secret key used was different to the one used within my IDE.

- On the deploy tab, in the ``Deployment method`` section I chose to deploy from my GitHub repo.

- I did this by clicking the GitHub option, then in the box underneath, and next to my GitHub username, I searched for and selected the ``drinks-db`` repo and clicked connect.

- Then, I selected the ``Enable Automatic Deploys`` option on the master branch so that all pushes to this branch would be automatically deployed to Heroku.

By completing the above steps I was able to take my code from AWS Cloud9 and successfully deploy my project to Heroku.

### Local Deployment

The following instructions are based on the user running VSCode on Windows 10. If your IDE / OS is different, your commands may differ slightly, but the process remains the same.

As a minimum you will need [Python 3](https://www.python.org/downloads/) installed on your machine. You will also need [PIP](https://pypi.org/project/pip/) which comes preinstalled with Python versions 3.4 and later. Having [Git](https://git-scm.com/) is also highly recommended.

To deploy locally on your own machine, follow these steps:

- Save a copy of the repo on your local machine or use ``git clone https://github.com/steview-d/drinks-db.git`` and cd into the correct folder using the terminal.

- Create a virtual environment, using ``python -m venv venv`` where the 2nd ``venv`` is the environment name.

- Activate the virtual environment with ``venv\Scripts\activate ``

- Install any required modules with ``pip install -r requirements.txt``

- Within the file ``app.py`` change the line ``app.config['SECRET_KEY'] = os.getenv('SECRET')`` to ``app.config['SECRET_KEY'] = os.getenv('SECRET', '<your_key>)`` where ``<your_key>`` is a secret key of your choosing.

- Also change ``app.config["MONGO_URI"] = os.getenv('MONGO_URI')`` to ``app.config["MONGO_URI"] = os.getenv('MONGO_URI', <your mongo_uri string>)`` where ``<your mongo_uri string>`` is the string that points to your own MongoDB.

- Your database should be named ``drinksdb`` with collections set up as outlined in the [database design](#database) section of this document. To help, you can also refer to these included [JSON examples](documentation/schema)

- From the terminal you can then run the app with ``python app.py`` and view in a browser at ``http://127.0.0.1:5000/``

## Credits

### Content

All code, outside of frameworks and libraries, is my own.

The recipes for the drinks were sourced from [Mr.Boston](https://mrbostondrinks.com/)

The text for the drink categories was taken from [Wikipedia](https://en.wikipedia.org/wiki/Main_Page)

The quotes used within the drink pages were sourced from various sites across the internet. Too many to list (or remember) but every quote is attributed to its (supposed) author.

All other words and text are my own.

### Media

The images for the drinks have been sourced from their respective recipes at [Mr.Boston](https://mrbostondrinks.com/)

The images used for the background, favicon and the footer cocktail logo were all originally sourced from google image search. Minor modifications have been made and they are being used in a non-profit educational capacity. If the site were to ever be monetised, these images would be replaced, or permission sought for their use

The background for the quotes on the drinks page was created using this [Background Image Generator](http://bg.siteorigin.com/)

The images for the landing page, error page, home page header image, and the individual drinks glasses were all licensed from [Adobe Stock](https://stock.adobe.com/uk/)

### Acknowledgements

Thanks once again go to [Antonija Šimić](https://github.com/tonkec), my Code Institute mentor, for her guidance and advice whilst working on this project.

Additional thanks to [Shane Muirhead](https://github.com/ShaneMuir) for his help with testing, and also helping me get my head around form resubmissions early on in the project, as it was driving me nuts.
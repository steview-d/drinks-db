# Cheers! The Drinks db

'Cheers!' is an app built on the Flask micro web framework and using MongoDB as the database. It's purpose is to provide users with a number of different types of (mainly alcoholic) drinks and cocktails.

At it's most basic level, my goal is to allow users to create drinks and cocktails using the information provided, as well as add their own to share with other users.

This initial brief has been expanded on considerably and I plan to use the following documentation to not only show what else this app can do, but also how it does it, and why.
 
## UX

The site itself follows standard web design conventions and therefore the layout and initial use of the site should be immediately recongnisable to all but the most inexperienced of web users.

The landing page is used to tell the user this is a site about drinks. Thanks to the success of sites like the IMDB, many users now associate 'db' with database, so I felt the tagline 'The Drinks db' was clear enough to convey the sites purpose as part of the landing experience, but even for those who don't make that connection, it soon becomes clear when the home page loads.

### User Stories

#### As a user, I want to be able to:

- View a list of drinks for inspiration on what to make / drink
- Add drinks of my own [CREATE]
- Get instructions on how to make certain cocktails [READ]
- Edit drinks I have submitted [UPDATE]
- Delete drinks I have submitted [DELETE]
- Easily see all of the drinks I have submitted
- See how popular the drinks I have submitted are by seeing which ones have been
	- Looked at the most
	- Added to the most users favorites list
	- Commented on the most
- Add drinks to a list of my favorites
- Comment on other users drinks, and reply to comments left by users for my drinks
- Choose whether to see one large list of all drinks available, or filter those drinks in a way of my choosing - such as by category, glass type, or difficulty.
- Choose how the information is presented to me, for example:
	- Number of drinks per page
	- Sort by name, views, comments, favorites, difficulty, and date
	- Sort either ascending or descending
- Search the database for drinks that match key words of my choosing and order the results either based on their relevance to what I searched for, or some other criteria of my own choosing.
- Do this on any device and browser of my choosing and have the same experience, and access to the same data, regardless of device and browser type.

Most importantly, as a user I want to be able to do this with minimal effort. I want to instinctively know how to use the site, and not have to search for how to do someting. I want it to just work, and not have to fight to make it work. Finally, above all else, I want to enjoy using the site.

#### As the site admin, I want to be able to:

- Build up a collection of drinks to continually provide the user with more choice on every visit.
- Give users the ability to interact with each other through the comments to help build a community.
- Allow the users to personalise their own experience through the ability to display results how they choose, and have their own section of the site (Account Page) that is all about them and their drinks.

Most importantly, I want the site to work and provide enjoyment for it's users so that at a later date, once there is more content and an active user base, the site can be monetised.

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
Examples of the above in .json format can be found [here](documenation/schema).

#### CSS Framework
I chose Materialize as the CSS Framework. Having previously only really used Bootstrap I wanted to use a different one this time around more out of curiosity than anything else. Unfortunately, I felt I spent more time fighting Materialize than actually working with it so the quest continues to find another CSS Framework for my next project.
Despite my struggles with Materialize, I was still able to produce a fully responsive site that works and displays well across all the most popular browsers and devices.

#### Color Scheme
For the color scheme, I initially went with a neon 80's style look, until I realised it looked more like a Myspace page from the mid 2000's. Instead, I went with a simple black and white approach, injecting color via the drink cards and labels. I did keep one neon effect, limiting it's use to the landing page, nav bar, and drink card links.

#### Typography
Fonts were kept to a minimum.
- [Grand Hotel](https://fonts.google.com/specimen/Grand+Hotel) was used for the full screen navigation elements.
- [Cormorant SC](https://fonts.google.com/specimen/Cormorant+SC) was used for h1 and h2 elements - mostly the display of drink names and section titles. The original plan was to use [Playfair Display SC](https://fonts.google.com/specimen/Playfair+Display+SC) but a display bug made within the font itself made this not an option. (The bug was when displaying the characters 'F' & 'I' together, it formed them in lowercase.)
- [Playfair Display](https://fonts.google.com/specimen/Playfair+Display) was used in the most part for smaller subheadings such as h3, h4 and h5 elements.
- Finally, [Muli](https://fonts.google.com/specimen/Muli) was used for h6 and p elements as I feel it's a nice, clean and easily readable font for general text, that pairs well with Playfair Display.

#### Icon Set
It seemed natural to use Materialize Icons with the Materiaze framework, but I couldn't always find the right icon with Materialize. Rather than use 2 different sets, I decided instead to go with [Font Awesome](https://fontawesome.com/) for all the icons.

### Wireframes

Mock ups were created early on in this project, before any code was committed. The early designs differ only slightly to the finished product, and it is clear to see that in the most part, the final result has turned out very much as I originally envisioned.
You can view the wireframes for each page using the links below

- [Home Page - Guest / Non User](static/wireframes/home_o.png)
- [Home Page - User Logged In](static/wireframes/home_i.png)
- [Search](static/wireframes/search_io.png)
- [Account Page](static/wireframes/account_i.png)
- [Add Drink](static/wireframes/add_i.png)
- [Edit Drink](static/wireframes/edit_i.png)
- [Login / Register](static/wireframes/log_reg_o.png)



## Features

### Current Features

**Flashed Messages**
The app uses the flask flash method to communicate important events to the user. These are displayed at the top of each page, just below the navbar. The messages are contained within a black box which contrasts against the background so even if the user isn't looking for it, it is almost unmissable.
Once read, it can be easily dismissed by clicking the close button in the upper right of the box.

**Landing Page**
A simple landing page that contains the text "Cheers! The Drinks db" on top of a full screen image of some filled shot glasses. This makes the visitor aware that the drinks in question are alcohlic and as such the site is a database of alcoholic drinks, most likley spirits, given the contents of the image.

**Register A New Account**
Users can use the site as a guest, but certain features are unavailable unless logged in. There is no barrier to registerin. Users provide a user name of their choosing and a password, and if accepted, they are stored in the database.
When a user registers, assuming they pass the validation checks, they are automatically logged in and taken to the home page.
Data validation on the registration form checks to make sure the user name is a minimum of 3, and maximum of 15 characters. There is a small 'i' icon next to the placeholder text which the user can hover over / click on for a tooltip explaining this.
The same applies to the password field, the only difference being a minimum of 5 characters are required.
If a user attempts to register with a name which has already been registered, the system flashes a messgage informing them of this, and to choose another.
If a user finds themselves at the register page but they intended to log in, there is a helpful link at the bottom of the form to redirect them to the log in page.

**Log In To An Account**
Much like the registration form, users can enter their username and password to log in to a previously created account. Data validation is in place to prevent submission of an empty input field and the app checks any details submitted against values held in the database.
Flashed messages are used to inform the user if they enter an incorrect username / password, or if the user they tried to log in with does not exist.
On successful log in to a previously registered account, the user is taken to their own account page.

**Log Out**
Users can log out of their account at any point, using the link at the top right of the nav bar (or the bottom option on mobile). This clears the session variable that stores their username and returns them to the home page.

**Navigation**
The site provides two types of navigation depending on the current view width. On widths > 992px there is a fixed navigation bar at the top of the window. It's contents vary depending on whether or not a user is logged in and allows the user to access areas of the site they are allowed to.

On widths <993px the options remain the same, but they are instead accessed using a side navigation element which can be accessed through the traditional 'burger' icon at the top left or by swiping across from the left edge of the screen on mobile devices.

If the user is currently viewing a page that is listed within the nav bar, that element is highlighted to show the users current position within the site. If they are viewing a page that is not part of the nav bar, such as a specific drink, then there is no highlight.

**Browse Drinks**
From the homepage, the user can browse all the drinks currently in the database. Using materialize cards, individual drinks are displayed as an image with the drink name underneath.

Each card contains 3 labels which show the category, glass type, and difficulty of the drink. These are small, but still readable, and positioned in the top right of the card so as to interfere with the image as little as possible.
If the drink card is a drink which has been submitted by the user who is viewing it, an edit icon is displayed between the image and drink title, allowing the user to go direct to the edit screen for that particular drink, should they wish.

The cards have been kept intentionally simple so as to not overload the user with information, and instead let the images 'pop' and draw the user in.

Pagination options have been placed both before, and after the drinks, make it easier for the user to move through the drinks.

**Suggested Drinks**
When a user is logged in, the home page can display some suggested drinks to the user. The criteria for display is to only show drinks not submitted by current user, to not show the same drink in this section, and to dsiplay a total of 4 drinks in a row.

If all of these conditions cannot be satsfied, then nothing will be shown.

**Browse Options**
On the home page, there is a button called browse options. Clicking this opens a box containing 3 tabs; category, glass type, and difficulty. This allows the user to browse the different categories, glasses, and difficulties and choose to view drinks only of a specific type.

The categories have been divided into cards, each containing some text describing that particular category. The text has been taken from [Wikipedia](https://en.wikipedia.org/wiki/Main_Page) and where there is too much text to display, the text has been truncated. The full text is shown on the individual category screen.

In the case of glass types, an image of each glass is provided to better help the user choose, especially as it is expected that not all users will be immediately familiar with what each glass looks like.

Even though the difficulty levels are quite self explanatory, an image has been provided for each to give the user more of an idea as to the difficulty level of one versus the other.

Each type, when clicked, takes the user to a page that shows only drinks of the type chosen, and provides a way for the user to quickly filter the drinks without the need of using the search function.


**'Showing Only' Pages**
These pages are shown when the user chooses a particular drink category, glass type, or difficulty, from the browse tabs on the home page.

The layout of the resulting drinks is identical to that on the home page (and also the search page) so will be familiar to the user, but it contains just the drinks they have chosen to view.

It also contains the same sorting options as found on the home page.

**Sort Options**
Whenever drinks are displayed on the home page, search results page, or the 'showing only' pages, the user is given the option to sort the results in a way of their own choosing, rather than having to rely on how the site iniitally chooses for them.

The user has the option to sort the displayed drinks by:
- Drink Name
- How many times it has been viewed
- How many comments it has recieved
- How many times it has been favorited
- How difficult the drink is to make
- The date it was added to the database

Additionally, the user also has the option to sort these results either ascending, or descending.
On top of this, the user can also choose how many drinks they want to see on each page at once. They can select from, 4, 8, 12, or even every drink in the database, all in one go!

Users can also sort by 'relevance' - which is explained in more detail as part of the seach page functionality.

**Search**
Users can search for specific keywords, filter by category, glass type, or difficulty, or any combination of these.
When the results are displayed, they are displayed in the same familiar format as how drinks are displayed on the home and 'showing only' pages.

If as part of the seach, the user has entered keywords to search on, when the results are displayed, the cards will contain a small yellow box in the lower left corner with a % value inside. This is the drinks relevance to the search term and allows the user to select the 'sort results by relevance first' option. This is only available when a keyword has been used, and allows the user to order the results by most relevant first. If 2 or more drinks have the same score, they are then sorted by name, views, comments, etc - whichever the user specified.

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
This created text indexes for the above fields. No value was given for the weight of each index, which meant they all defaulted to 1 and carrry equal significance when searching.

**Drink Page**
Each drink has it's own page that contains all information relating to that drink. When a user clicks on a drink, this is the page they are taken to. It shows the name of the drink, along with the name of who submitted it, and when. If the user viewing is the user who submitted, they will have additional options here too, namely ``edit`` and ``delete``.

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

There is a tooltip letting users know, when entering instructions, to put each one in it's own sentence. When displaying instructions on the drinks page, each instruction is separated by splitting the string at each '. ' (full stop and space).

The site doesn't currently host the images for drinks ( - on the planned features list) and instead stores the url of the image to display. If a user is adding a drink but doesn't have an image to use, they can click the '+' button at the end of the input field and it will populate the field with a link to a placeholder image. This avoids the individual drinks pages looking 'broken' if there is no image to display.

Each drink can have up to 10 measures and ingredients, but a minimum of 1. The page defaults to 4, but using the ``add ingredient`` and``remove ingredient`` buttons the user can adjust the number of boxes to match the number of measures and ingredients they require.

**Edit Drink**
The edit drink form is identical in layout to the add drink form, and very similar in functionality.

The important differences from a UX perspective is the '+' icon is not present for the default image. As there will already be an image stored (even a placeholder) the user has the option to update with their own, or keep the existing.

The number of measures and ingredients boxes shown match the number of measures and ingredients, as opposed to the default 4 with the add drink page.

Finally, there is a ``delete drink`` button, allowing the user to completely remove the drink from the database.

**Delete Drink**
If the user clicks the ``delete drink`` a popup modal will appear asking for confirmation, and advising that this action cannot be undone. Should the user still choose to delete, the drink will be permanently deleted.

**'My Account' Page**
Each user has their own account page, which is used to store user specific information and stats.

Every account page, regardless of the users time on site and activity, will display a welcome message, along with some stats for the user and the site overall. It will show combined totals for views, favorites, and comments for all user submitted drinks. It will also show how many drinks are currently in the database, along with the total number of categories, types of glass, and levels of difficulty.

If the user has submitted drinks, it will also scan all these drinks and display at the top which ones have received the most views, comments, and additions to other users favorite lists.

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
I want to add a log that initially stores every action that performs a write to the database, and eventually expand it to read actions too. The log will be a simple record that contains the user name, date, time, action performed, and if it was succesful or not.
It would also capture new user registrations, as this is the only database write action an unregistered user can undertake.

**Deleted Items**
When a drink is deleted it is gone forever. Instead, I'd like to have them stored in a deleted items list for review by an admin.

**Admin Panel**
To make managing the site easier, an admin panel will need to be added. Initially this will contain options such as reviewing logs, moderating comments, checking deleted items, and so on, but has the potential to contain so much more.



## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X
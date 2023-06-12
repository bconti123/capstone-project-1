# Capstone Proposal

1. What goal will your website be designed to achieve?
    - This website shows card images, information about the card type (monster, spell, trap), the monster's stats (Level, ATK, DEF, attribute, type, etc.), and what the effect does. Addresses the misinterpretation of game states and rulings due to card descriptions' often overlooked semicolon and colon symbols. This website highlights card text like the pay cost to activate an effect, the condition/meet requirement, and other complex interactions in the game.

2. What kind of users will visit your site? In other words, what is the demographic of
your users?
    - The viewers are players and judges who rely on accurately interpreting card effects and game mechanics. The users, who are fans, players, and judges, discuss the game state and make clear the interaction with cards' effect in the game state. They want to make sure rulings are corrected and reduce misinterpreted game states.

3. What data do you plan on using? You may have not picked your actual API yet,
which is fine, just outline what kind of data you would like it to contain.
    - I will use Yu-Gi-Oh! API by YGOPRODeck. From API, get data on card images and information on the card type (monster, spell, and trap), stats (ATK, DEF, Level, Attribute, Type), effect descriptions, etc.

4. In brief, outline your approach to creating your project (knowing that you may not
know everything in advance and that these details might change later). Answer
questions like the ones below, but feel free to add more information:
    - a. What does your database schema look like?
    ![Database Schema](/images/DatabaseSchemaDesign.png)
    I am not sure about API database already has **card id**
    - b. What kinds of issues might you run into with your API?
        - Rate Limit is 20 requests per 1 second.
        - Download and store all data pulled from API
        - **NOTES ON IMAGES:** Do not continually hotlink images directly from the site.
        - Card Information endpoint in the documentation is a straightforward.
    - c. Is there any sensitive information you need to secure?
        - Users need to have an account with a password and email for allowing create/update/delete posts and save information in their favorite card storage from my own SQL database.
    - d. What functionality will your app include?
        - Search cards with the name, monster/spell/trap card, card types, and card description from Yu-Gi-Oh! API.
        - Check top most views cards.
        - The posts and comments for card ruling discussion.
        - Highlight specific symbols and words with color in the card description's text to make it easy to read for users.
        - Ruling explanation with specific words and symbols. If a user needs more info, click the link directly to Yu-Gi-Oh! Wiki ruling website. **(Possibly)**
        - The number of views on each card in history **(Possibly)**
        - **Legacy cards with pre-errata and old errata are not supported.**
    - e. What will the user flow look like?
        - Sign Up/Login Account (Optional), including hashed password
        - Search form
        - Favorite
        - Navbar - Home, Search Card, Top most viewed cards, Login/Sign Up.
        - Posts/Comments for ruling discussion.
    - f. What features make your site more than CRUD? Do you have any stretch
    goals?
        - User Session for login/logout. If account is not in session, user is a guest.
        - Display card data from Yu-Gi-Oh! API
        - Create/Update/Delete accounts, posts, and comments.
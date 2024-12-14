# Capstone Project 1 - YGOEffectCheck App

YGOEffectChecker is a website designed to provide users with the ability to quickly access card text, rulings, and card interactions for Yu-Gi-Oh! trading card game. The website allows users to search for any card they want to learn more about.

This website retrieve card information in data from YGOProDeck API. I used Python to download all card images in data from YGOProDeck API to my own cloud API that called Cloudinary (https://cloudinary.com/).

Website URL: [https://yugioh-eff-checker.onrender.com/](https://capstone-project-1-nine.vercel.app/)

![YGO_EFF_CHECKER_Search](/static/images/search.png)

### Features

**Efficient Card Reading:** YGOEffectChecker streamlines the process of understanding card effects, rulings, and interactions, helping players grasp complex card mechanics easily.

**Comprehensive Card Data:** The website retrieves card information using the YGOProDeck API, ensuring that the database is up-to-date with the latest card releases and rulings.

**Cloudinary Integration:** To enhance performance, all card images are downloaded and stored on Cloudinary, a reliable cloud API, ensuring smooth and fast loading times.
> I wrote function carefully in Python for download all images from YGOPRODeck API. Download image per 0.5 second or 1 second by setting up time.sleep(0.5) or time.sleep(1). I don't want to stress server.

**You try this out**
1. Find the card titled **"Magic Cylinder"**. 
2. Hover the mouse cursor over the card to see it highlighted or raised slightly, indicating it's clickable.
3. Click on the white card to trigger the desired action or view additional information.

![Magic_Cylinder](/static/images/magic_c.png)

You notice **Effect Checker** that it display **Condition**, **Activation**, and **Resolution**. You want to learn more about PSCT (https://yugiohblog.konami.com/articles/?p=4514#more-4514)

### YGOProDeck API: https://ygoprodeck.com/api-guide/

### Database Schema Design
![Database_Schema_Design](/Database-Schemas/DatabaseSchemaDesign-2.png)

**Tech Slack Used:** 
- Python 3.8.10
- Flask as a framework
- Bootstrap
- PostgreSQL
- Render as website hosting service
- Cloudinary as a Cloud API service

### Future Features:
- Develop more complex card interactions.
- Add favorite cards to the user's list.


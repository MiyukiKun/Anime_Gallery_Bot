
# Anime Gallery Robot

<p align="center">
  <img src="https://telegra.ph/file/59587a1cbf5047d72a807.jpg">
</p>

A Bot which uses unofficial gogoanime and kissmanga api to search and provide anime and manga respectively to the user.  
 <p align='center'>
  <a href="https://www.python.org/" alt="made-with-python"> <img src="https://img.shields.io/badge/Made%20with-Python-00ead3.svg?style=flat-square&logo=python&logoColor=00ead3&color=00ead3" /> </a>
  <a href="https://github.com/MiyukiKun/Anime_Gallery_Bot/" alt="Maintenance"> <img src="https://img.shields.io/badge/Maintained%3F-Yes-green.svg?style=flat-square&logo=serverless&logoColor=00ead3&color=00ead3" /> </a>
</p>

# Table of Content

- [FEATURES](#features)
- [TEST THE BOT (DEMO)](#bot)
- [ENV](#environment-variables)
- [DEPLOYMENT](#deployment)
- [SUPPORT](#support)
- [FAQ](#faq)

## Features

This Bot have some awesome features listed below everything add free
- Download any anime avilable on GoGoAnime website
  - Easy access to currently airing anime with  `/latest` command
  - Download any particular episode via search
  - Batch download upto 15 episodes in telegram itsel
  - Batch download upto 100 episodes via **1DM** app

- Read manga.
  - The Manga is provided as HTML file instead of pdf as its much faster and u can simply open it in **Google Chrome** for easy reading

- Support for nhentai.
    use `/nh <code>` to get the doujin in HTML format same as Mangas

  
## Bot 

You can find our bot on Telegram by [@Anime_Gallery_Robot](https://t.me/anime_gallery_robot).
  
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_ID` You Can Get it from [here](https://my.telegram.org/) .

`API_HASH` You Can Get it form [here](https://my.telegram.org/) .

`BOT_TOKEN` Search [@BotFather](https://t.me/botfather) in telegram.

## Deployment 

### Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/MiyukiKun/Anime_Gallery_Bot)

*Note that this wont work for now yet to add app.json file to the repo  

## Support
To report any problems, bugs, suggestions visit [@Anime_Gallery_Robot_Support](https://t.me/anime_gallery_robot_support).

Easier to contact me there than through github

  
## FAQ

#### Q1. How can i make my own bot?

Ans. U can deploy to heroku manually by forking and adding env vars manually, i will add app.json soon so you can use the direct deploy method 

#### Q2. How to use the bot?

Ans. Open the bot and type `/help`.
nice and detailed explination is given there

## Creator

- [Miyuki](https://github.com/MiyukiKun/Anime_Gallery_Bot)
- Special thanks to [BaraniARR](https://github.com/BaraniARR/gogoanimeapi) for the base of unofficial gogoanime api

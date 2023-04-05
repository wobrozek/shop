# shop
E commerce website

## Overview
Website allows user to:

- Show current and archive listings
- Create own auctions
- Customize profile
- Bid offerts
- Add comments
- Create own watchlist


https://user-images.githubusercontent.com/64639878/229930149-7da2a9d2-f2b1-41d6-b5d9-479c1a69cb80.mp4

# Features
## Api 
Some features on website are using http api to provide changes on site without refreshing

## Web Sockets 
Website is using Django channels due to users get instant information about current prices and comments on listing site

## Optimization 
Website was optimized using Django Toolbar due to it sends the minimal amount of database queries  
![sql_querry](https://user-images.githubusercontent.com/64639878/229934013-75d569de-ae7a-4b13-91c3-bdc7f1423059.PNG)

## TODO

Add celery cronjob that sends mails to owner and winner when the date of auction expired

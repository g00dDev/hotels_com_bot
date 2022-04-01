<h1 align="center">hotels_com_bot</h1>

## What the bot can do
<div>
<p>Bot works using 
<a href="https://telegram.org/" target="_blank">Telegram</a> и
<a href="https://rapidapi.com/apidojo/api/hotels4/" 
target="_blank">API Hotels</a>. Some parts of the bot use the 
third party calendar
<a href="https://libraries.io/pypi/telebot-calendar/1.2" 
target="_blank">telebot-calendar</a>. 
Бот uses data from the site 
<a href="https://hotels.com" target="_blank">Hotels.com</a>, 
leading provider of hotel accommodation in the world. Сайт
<a href="https://hotels.com" target="_blank">Hotels.com</a> gives 
travellers one of the widest selections of accommodation on the net, 
including both independent and major chain hotels as well as self-catering 
in over hundreds of thousands properties worldwide.</p>
<p>The bot helps to quickly collect data from the site about the cheapest,
the most expensive and most suitable hotels.</p>
</div>

## Communication between the user and the bot
<div>
List of commands that the user can use:

    /help — help with bot commands
    /start — choose language and currency
    /lowprice — search the cheapest hotels in the city
    /highprice — search the most expensive hotels in the city
    /bestdeal — search the most suitable hotels in accordance with 
                specified range of prices and range of distances 
                to the city center
    /history — display hotels search history
    /delete_history — delete hotels search history
</div>
<div>
Using the command <a href="">/start</a>, language and currency 
can be specified.<br/>
If language and currency are not specified, default values are used.<br/>
</div>
<div><br/>
Commands <a href="">/lowprice</a>, <a href="">/highprice</a> и 
<a href="">/bestdeal</a> allow to get:
</div>
<div>
<ul style="display: inline-block; padding: 10; margin: 0px auto;">
    <li>hotel name,</li>
    <li>address,</li>
    <li>distance from the hotel to the center,</li>
    <li>price in specified currency,</li>
    <li>photos of the hotel (if the user has found it necessary 
        to display them)</li>
</ul>
</div>
<div><br/>
The command <a href="">/history</a> allows to display information 
blocks containing:
</div>
<div>
<ul style="display: inline-block; padding: 10; margin: 0px auto;">
    <li>date and time of command entry,</li>
    <li>the command,</li>
    <li>list of hotels with address and price</li>
</ul>
</div>

## Communication between the administrator and the bot
List of commands for controlling the bot by the administrator:

    /stop — stop the bot
    /delete_all_history — delete hotel search history of all users

## Configuration file setup
List of tokens for connecting the bot to
<a href="https://telegram.org/" target="_blank">Telegram</a> and to
<a href="https://rapidapi.com/apidojo/api/hotels4/" target="_blank">
API Hotels</a>,
are located in the file <a href="">.env</a><br/>
Parameters and settings are collected in a file 
<a href="">/data/config.py</a><br/>
Logging settings are collected in a file 
<a href="">/utils/misc/project_logging.py</a>

## Bot demo
<img src="demo.gif"></img>

### [Developer site](https://github.com/g00dDev/hotels_com_bot)

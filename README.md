This program creates a web page that asks a user for their address and a message they would like to send to the governor of their state. It uses Google's civic information api https://developers.google.com/civic-information/docs/v2/representatives/representativeInfoByAddress) to find the governor of the state by zipcode. It then uses Lob's API to create a letter object which gets rendered to a PDF using html. You can play around with the code to change which government representative you want to write to. You can also send a postcard via Lob's API.

You need python3, Flask and an internet connection to run this app.
You can install Flask via the terminal/command prompt using pip: pip install Flask
To run the app, navigate to this folder on your terminal and enter the following command:
	python backend.py
Navigate to your local host(should be http://127.0.0.1:5000/) to view the app

NOTE: You need to add your lob API and Google API key at the appropriate locations in the lob_backend.py file. The code will not work unless you do that
	
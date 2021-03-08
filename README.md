# Robo-Advisor


# prerequisites
+ Anaconda 3.7
+ Python 3.7
+ Pip

# Installation 

#Clone or download from [GitHub source] then navigate into the project repository

cd robo_advisor 

#Create and activate a new Anaconda virtual environment:

conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env

#From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

pip install -r requirements.txt

# Set Up 

#Before using or developing this application, take a moment to obtain an AlphaVantage API Key (e.g. "abc123").

#After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

API_KEY = "abc123"

# Usage 

#run the program

python app/robo_advisor.py

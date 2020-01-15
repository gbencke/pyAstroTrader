# AstroTrader

AstroTrader is a project to investigate the correlation between Astrological events and the price fluctuations in the stock market as Trends, this is a research project and it is not meant to be used in the real market.  

Although Financial Markets and Astrology seems to be totally unrelated subjects, the fact is that many of the great bankers and traders of the last 200 years, took astrology seriously on its capability to predict medium and long-term trends in the Financial Market  

![](docs/jpmorgan.jpg)

The subject of financial astrology has been well research for the last 70 years, and I recommend the following books on the subject:

* [Financial-Astrology, David-Williams](https://www.amazon.com/Financial-Astrology-David-Williams/dp/0866900454)
* [The Bull, The Bear and The Planets: Trading the Financial Markets Using Astrology](https://www.amazon.com/Exploring-Financial-Universe-Planets-Finance/dp/0892542187/ref=pd_sbs_14_t_1/145-5392391-6321207)
* [Exploring the Financial Universe: The Role of the Sun and Planets in the World of Finance](https://www.amazon.com/Exploring-Financial-Universe-Planets-Finance/dp/0892542187/ref=pd_sbs_14_t_1/145-5392391-6321207)

## Why Astrology?

Nature on planet earth uses the movement of the planets around itself, in order to mark the seasons and its biological and geological cycles. The study of the relation between the movement of the planets and such cycles is called Astrology.

Astrology is mankind`s first science, and its research allowed us to leave the hunter-gatherer societies and evolve to large, complex, agricultural-based ones. As the ancient civilizations were able to predict the best time to sow and to rip its harvests, it allowed agriculture to be a safer activity than hunting and/or gathering fruits.  

The first uses of Math and Written language were to record both the stocks of granaries and also the movement of the planets on the Sky. Great Megalithic structures like Stonehenge and the Ziggurats of Sumer were primarily used as astrological observatories.

## Astrology and Financial Markets

It is well known that Astrology was one of the enablers of the Agricultural Revolution, about 5k-6k years ago, but what is its relation to the stock market? *As all Nature on Earth is influenced by the position of the planets on the sky, the human psychology is also subconsciously influenced by such movements as well.*

It is a well know fact that crime rates sour during the Full Moon and decrease during the New Moon, that certain planet alignments also have influence on pregnancy rates, because we are part of Nature and we also use the movement of the planets around us to measure biological cycles. 

So, what causes the prices fluctuation on the stock market?

**The prices on the stock market are merely a projection of the risk perception of a certain asset**

So, as any trader knows, the price on the market is 100% determined by psychological perception of Fear or Greed. And the objective of this project is to measure and determine the influence of the movement of the planets on the perception of risk for a certain Asset traded in a Stock Exchange.
 
## Install and Usage

The Software consists of python jupyter notebooks that download data from a public stock quotes API, creates a machine learning model, and then runs predictions for the future on the probabilities of price increase and decrease for the certain commodity.

It is required the following software:

* Linux OS (Have tested with Arch and Ubuntu Distributions)
* Python 3.6 installed globally.

It is necessary to obtain a public token from Alphavantage in order to retrieve the quotes for the assets, this key is free and can be obtained here:

[https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

In order to use the software, it is necessary to clone this repository, and run the following scripts:

    set ASSET_TO_CALCULATE=<<Ticker of the Asset to use>>
    set ALPHAVANTAGE_KEY=<<Token for the use of Alphavantage API>>

    mkdir notebooks/input
    mkdir notebooks/output
    ./start_notebooks.sh

The start_notebooks script will create the python environment, install the necessary modules and then start the jupyter lab server. The startup procedure will print on the terminal screen, a URL that can be accessed using any browser in order to access the notebooks.

If there is no need to access the notebooks, they can be run directly on the CLI:

    set ASSET_TO_CALCULATE=<<Ticker of the Asset to use>>
    set ALPHAVANTAGE_KEY=<<Token for the use of Alphavantage API>>

    mkdir notebooks/input
    mkdir notebooks/output
    ./run_notebooks.sh

The script above will run the entire process and save in notebooks/output the results of the computations.

## Software Architecture

The project is developed using Jupyter Notebooks, which allow for a very fast development and also a very intuitive analysis of the data being processed by the python notebook. 

It also contains a module: ```pyastrotrader``` that provides astrological computations using the ```swiss ephemeris```.   

The project contains 3 main notebooks:

* **DownloadData.ipynb**: This notebook downloads the stock quotes of the last 20 years, for the asset specified in the environment variable: ```ASSET_TO_CALCULATE```, and saves the quotes as a CSV file in the ```notebooks/input``` folder   
* **CreateModel.ipynb**: This notebooks creates a pandas dataframe with the downloaded quotes for the specified asset in ```ASSET_TO_CALCULATE```, calculates the astrological positions of the planets for each day, and then run a XGBoost training algorithm in order to detect the correlation between each astrological aspect and the price trend for the next 5 days. The model then is saved in the ```notebooks/output``` folder. 
* **Predict.ipynb**: This notebook loads the model created in the previous notebook and then runs prediction of the price trend for the next 180 days, storing the results in the ```notebooks/output``` folder.

Inside each notebook there are explanations for the algorithms being used, please start the jupyter lab server and then navigate the notebooks in order to examine in details its architecture and design.


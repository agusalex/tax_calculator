# Tax Calculator

Python is a requirement to run this project
Install python first https://www.python.org/downloads/release/python-3115/


## Then install requirements
```shell
pip install -r requirements.txt
```
## Run program using input csv

```python
python main.py --input_csv=ibkr_input.csv
```

## function tests
are defined in here: /tests/taxable_amount_test.py

## InteractiveBrokers Input file location
/ibkr_input.csv

## venv
python3 -m venv .venv


## TODOs

Stocks
    long - working
    shorts - working
    long_to_short // short_to_long
        - the more complex part here is the switch from the long to short or the other way around (short to long), as this will be 2 calculations.
        - example: having 10 stocks long, and then selling 30 stocks, means we have to calculate profit for 10 longs when selling, and then calculate entry price (moving average) for the 20 pieces shorts.

    check currency conversion
        https://docs.google.com/spreadsheets/d/1xL9GxZ5TpXgERhIxJxkpTD5m-w1mRvOf5lBV6GEDSlY/edit?disco=AAAA5k5LYEE
        https://wusatiuk.slack.com/archives/D05RFNSDFLG/p1695304170263319



Currencies
    - every time I buy a currency, there is an entry price in baseCurrency.
    - every time I sell a currency, we need to calculate profit / loss compared to the baseCurrency buying price.
    When it comes to currencies, we have to calculate them with every transaction at real conversion rate (when we have a real converion from/to EUR) or ECB daily conversion rate (from API; when we buy/sell stocks in a foreign currency) to the baseCurrency (EUR)
    - calcuations there, but no taxes calculated in them right now.


Options
    currently not supported
    - will be the same as stocks, as long as there is only buying and selling.
    - later on we will have some further stuff to do, when it comes to options executions. :)


There was other stuff we were missing that we discussed in Slack but can't remember and Slack is not allowing us to see back more than 90 days because of the trial.

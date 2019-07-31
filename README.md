# Introduction to Data Science with Python

## Setup:

- Create virtual environment
> python -m venv venv

- Activate virtual environment
> source venv/bin/activate

- Install dependencies
> pip install -r requirements.txt

## Usage

- To collect more tweets, listen to twitter stream using

> $ python fetchTweet.py

    `db name` : `analysis`

    `collection name`: `brexit`

## Information

-  `.keys.json` will store all credentals as:

    ```javascript
    [{
        "consumer_key": "",
        "consumer_secret": "",
        "access_token": "",
        "access_token_secret": ""
    }]
    ```
    Find using apps.twitter.com

- All analysis is present in `analysis.py`

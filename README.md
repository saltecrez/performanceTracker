# performanceTracker

- **Goal**: Checks stocks performance and gives valuable hints in real time.

- **Description**: Flask application that allows to visualize stocks performance on the browser. Sends alerts at maxima/minima.

- **Requirements**:
    - pip install virtualenv
    - virtualenv env
    - source env/bin/activate
    - pip3 install flask
    - pip3 install bokeh
    - pip3 install yfinance
    - pip3 install numpy

- **Configuration parameters**:
    - "email": email address to be alerted
    - "sender": email address of the sender
    - "smtphost": hostname of the machine hosting the smtp server
    - "assets": information characterizing the assets; in particular:
        - "label": stocks label (e.g. AFX.DE for Zeiss on the Frankfurt stocks market)
        - "multiple": yes or no. Specifies if a stock was bought in multiple tranches
        - "nested": information characterizing a stock asset bought in multiple tranches:
                - "buyprice": buy price for that asset tranche
                - "buydate": date in which the asset was bougth (format YYYY-MM-DD))
                - "wealth": capital invested in that asset

- **Usage**:
    - python app_stocks.py

#!/bin/bash
echo Start running scripts ...
echo Executing puppeteer scripts ...
node ./puppeteer-scripts/sushi_doma.js
node ./puppeteer-scripts/mama_pizza.js
node ./puppeteer-scripts/dodo_pizza.js
node ./puppeteer-scripts/dakicho.js
echo Entering virtualenv ...
source ../env/bin/activate
python3 imperio.py
python3 sushi-bro.py
python3 sushi_doma.py
python3 hochu_sushi.py
python3 izh_sensei.py
python3 mama_pizza.py
python3 eshe_kusochek.py
python3 dodo_pizza.py
python3 dakicho.py
python3 sender.py
echo Exiting virtualenv ...
deactivate
echo End of the script
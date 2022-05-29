#!/bin/bash
echo Start running scripts ...
echo Executing puppeteer scripts ...
node ./puppeteer-scripts/sushi_doma.js
echo Entering virtualenv ...
source ../env/bin/activate
python3 imperio.py
python3 sushi-bro.py
python3 sushi_doma.py
python3 hochu_sushi.py
python3 izh_sensei.py
echo Exiting virtualenv ...
deactivate
echo End of the script
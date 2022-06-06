#!/bin/bash
echo Deleting old files ...
python3 preparation.py
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
python3 ronny_burgers.py
python3 ronny_combo.py
python3 ronny_shawarma.py
python3 tri_bogatirya.py
python3 kinza.py
python3 perepechka.py
python3 sender.py
echo Exiting virtualenv ...
deactivate
echo End of the script
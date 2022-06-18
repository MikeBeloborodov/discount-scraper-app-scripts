#!/bin/bash
echo Preparing ...
python3 preparation.py
echo Start running scripts ...
echo Executing puppeteer scripts ...
node ./puppeteer_scripts/sushi_doma.js
node ./puppeteer_scripts/mama_pizza.js
node ./puppeteer_scripts/dodo_pizza.js
node ./puppeteer_scripts/dakicho.js
node ./puppeteer_scripts/meatproject.js
echo Entering virtualenv ...
source ../env/bin/activate
python3 ./python_scripts/imperio.py
python3 ./python_scripts/sushi-bro.py
python3 ./python_scripts/sushi_doma.py
python3 ./python_scripts/hochu_sushi.py
python3 ./python_scripts/izh_sensei.py
python3 ./python_scripts/mama_pizza.py
python3 ./python_scripts/eshe_kusochek.py
python3 ./python_scripts/eshe_kusochek_combo.py
python3 ./python_scripts/dodo_pizza.py
python3 ./python_scripts/dakicho.py
python3 ./python_scripts/dakicho_combo.py
python3 ./python_scripts/ronny_burgers.py
python3 ./python_scripts/ronny_combo.py
python3 ./python_scripts/ronny_shawarma.py
python3 ./python_scripts/tri_bogatirya.py
python3 ./python_scripts/kinza.py
python3 ./python_scripts/perepechka.py
python3 ./python_scripts/papa_lavash.py
python3 ./python_scripts/odin_kg_schastya.py
python3 ./python_scripts/parus18.py
python3 ./python_scripts/kfc_burgers.py
python3 ./python_scripts/rocket_roll.py
python3 ./python_scripts/fresh_kebab.py
python3 ./python_scripts/meatproject.py
python3 ./python_scripts/moomooizhevsk.py
python3 ./python_scripts/pandagrill.py
python3 sender.py
echo Exiting virtualenv ...
deactivate
echo End of the script

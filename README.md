## Generate more complete energy quotes!

Modify the variables
```python
MY_POSTCODE = "SW1A1AA" # insert postcode here
ELECTRICITY_USE = 50 # units: kWh
GAS_USE = 50 # units: kWh
```


And run the script
```bash
python octopus_scraper.py
```

It will print out an ordered list of json objects; the lower down a tariff is in the list, the cheaper it will be for you to use.
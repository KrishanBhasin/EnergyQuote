import requests
import json 
from typing import List, Callable

def get_tariff_info(postcode: str):

    api_url = f"https://octopus.energy/api/v1/postcodes/{postcode}/products/"

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def mock_get_tariff_info(postcode: str):
    with open('octopus_test_data.json', 'r') as myfile:
        data=myfile.read()

    return json.loads(data)


def tariff_calculator(elec_use: int, gas_use: int, tariff_info):
    days_per_year = 365
    elec_standing_charge = float(tariff_info.get("elec_standing_charge")) * days_per_year / 100
    gas_standing_charge =  float(tariff_info.get("gas_standing_charge")) * days_per_year / 100

    print(elec_standing_charge, gas_standing_charge)

    elec_usage_charge = float(tariff_info.get("elec_std_unit_rate")) * elec_use / 100
    gas_usage_charge = float(tariff_info.get("gas_unit_rate")) * gas_use / 100

    print(gas_usage_charge, elec_usage_charge)

    return(sum([elec_standing_charge, elec_usage_charge, gas_standing_charge, gas_usage_charge]))

def remove_historic_tariffs(tariff_list):
    return [t for t in tariff_list if t.get("live")=="TRUE"]

def remove_eco7_notes(tariff_list):
    for t in tariff_list:
        t.pop("elec_eco7_day_unit_rate")
        t.pop("elec_eco7_night_unit_rate")
        t.pop("elec_eco7_standing_charge")
    return tariff_list


def calculate_all_tariffs(elec_use: int, gas_use: int, tariff_list: List, calculator: Callable):
    for counter, t in enumerate(tariff_list):
        try:
            cost = calculator(elec_use,gas_use,t)
        except TypeError as e:
            continue
        tariff_list[counter]['total_cost'] = cost

    return tariff_list

if __name__ == "__main__":
    MY_POSTCODE = "SW1A1AA" # insert postcode here
    ELECTRICITY_USE = 50 # units: kWh
    GAS_USE = 50 # units: kWh


    tariff_list: List = get_tariff_info(MY_POSTCODE)
    tariff_list: List = remove_historic_tariffs(tariff_list)
    tariff_list: List = remove_eco7_notes(tariff_list)
    updated_tariff_list: List = calculate_all_tariffs(ELECTRICITY_USE,GAS_USE,tariff_list, tariff_calculator)
   
    lines = sorted(updated_tariff_list, key=lambda k: k.get('total_cost', 9999999999999), reverse=True)
    for l in lines: 
        if l.get('total_cost'):
            print(json.dumps(l, indent=4, sort_keys=True))

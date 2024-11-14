import ast
import os
from pathlib import Path
import pandas as pd
import requests
import csv
from itertools import product
from car import Car


def load_data(path: str) -> dict:
    properties = {}

    with open(path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Parse possible values, split by semicolon
            possible_values = [value.strip() for value in row['Possible_Values'].split(';')]

            # Parse condition, if it exists
            condition = row['Condition'].strip() if row['Condition'] else None

            # Store each property as a dictionary
            properties[row['Property_Name']] = {
                'possible_values': possible_values,
                'condition': condition
            }

            # Special handling for JSON-like data in 'Possible Values'
            if row['Property_Name'] == 'Q5-ModelData':
                properties['Q5-ModelData']['possible_values'] = [
                    ast.literal_eval(data) for data in row['Possible_Values'].split(';')
                ]

    return properties


def generate_unique_cars(properties: dict) -> set:
    # Prepare a dictionary of property names with their possible values
    possible_values = {name: prop['possible_values'] for name, prop in properties.items()}
    unique_cars = set()

    # Generate all possible combinations of property values
    for values_combination in product(*possible_values.values()):
        # Map each property to a value from the current combination
        car_attributes = dict(zip(possible_values.keys(), values_combination))

        # Apply conditions to each property if specified
        for name, prop in properties.items():
            condition = prop.get('condition')
            if condition:
                condition_name, expected_value = map(str.strip, condition.split('=='))
                # Set attribute to None if condition is not met
                if car_attributes.get(condition_name) != expected_value:
                    car_attributes[name] = None

        # Create a Car object using the filtered attributes
        car = Car(
            is_electric=car_attributes.get('Q1-IsElectric') == 'True',
            km=int(car_attributes.get('Q2-KM', 0)) if car_attributes.get('Q2-KM') else None,
            engine_size=float(car_attributes.get('Q3-EngineSize', 0.0)) if car_attributes.get(
                'Q3-EngineSize') else None,
            color=car_attributes.get('Q4-Color'),
            model_data=car_attributes.get('Q5-ModelData')
        )
        unique_cars.add(car)

    return unique_cars


def get_exchange_rate():
    """
    Fetch the current exchange rate between USD and CLP using the Coinbase API.

    Returns:
    - float: The current exchange rate from USD to CLP.
    """
    url = "https://api.coinbase.com/v2/exchange-rates?currency=USD"
    response = requests.get(url)
    data = response.json()

    # Extract the CLP exchange rate
    try:
        exchange_rate = float(data['data']['rates']['CLP'])
        return exchange_rate

    except (KeyError, TypeError, ValueError) as e:
        print("Error fetching exchange rate:", e)
        return None


def generate_output(cars_set: set, exchange_rate: float, output_path: str):
    cars_list = []

    for car in cars_set:
        price = car.calculate_price(exchange_rate)
        cars_list.append({
            "Q1-IsElectric": car.is_electric,
            "Q2-KM": car.km,
            "Q3-EngineSize": car.engine_size,
            "Q4-Color": car.color,
            "Q5-ModelData": car.model_data,
            "Price (CLP)": price
        })

    # Save to Excel
    df = pd.DataFrame(cars_list)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Print debugging information
    print(f"Output directory exists: {os.path.exists(output_dir)}")
    print(f"Output directory is writable: {os.access(output_dir, os.W_OK)}")

    # Write to Excel file
    try:
        df.to_excel(output_path, index=False)
        print(f"Successfully wrote output to {output_path}")
    except Exception as e:
        print(f"Error writing to Excel file: {str(e)}")
        raise


def main():
    # Use paths relative to the container's working directory
    csv_file_path = 'data/inputs/cars_data.csv'

    # Set the output path to use the mounted volume directory
    output_path = "/data/outputs/car_permutations.xlsx"

    print(f"Current working directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir(os.getcwd())}")
    print(f"Data directory exists: {os.path.exists('/data')}")
    print(f"Data directory contents: {os.listdir('/data') if os.path.exists('/data') else 'Directory does not exist'}")

    try:
        # Load data
        properties_data = load_data(csv_file_path)

        # Fetch exchange rate
        exchange_rate = get_exchange_rate()
        if exchange_rate is None:
            print("Failed to fetch exchange rate.")
            return

        # Generate unique cars and output results
        unique_cars = generate_unique_cars(properties_data)

        generate_output(unique_cars, exchange_rate, output_path)
        print(f"Output successfully written to {output_path}")
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
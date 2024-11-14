# Car Permutation Generator

This project generates unique car permutations based on property data and conditions defined in a CSV file. The program then calculates the price of each car configuration and outputs the results to an Excel file.

## Project Structure

- **`main.py`**: The main script that loads data, generates unique car permutations, calculates prices, and outputs results to Excel.
- **`car.py`**: Contains the `Car` class, which represents each car's properties and calculates the price.
- **`Property.py`**: Handles property data with conditions and checks if conditions are met.
- **`cars_data.csv`**: A CSV file that defines car properties, their possible values, and conditions.
- **`Tests/`**: Contains unit tests for the project.

## Features

- **Load Property Data**: Load car properties and possible values from a CSV file.
- **Apply Conditions**: Conditions allow you to set specific rules, like "EngineSize can only be set if IsElectric is False."
- **Generate Unique Permutations**: Creates all possible unique car configurations based on the property values and conditions.
- **Calculate Price**: Calculates each car's price based on its KM value, manufacturing year, and an exchange rate fetched from a live API.
- **Export to Excel**: Saves all unique car permutations with their calculated prices to an Excel file.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ofiregev1/Cars.git
   cd Cars
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv cars_assignment
   source cars_assignment/bin/activate  # On Windows: cars_assignment\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Program in Docker (Optional)**
   Build and run the Docker container to generate the output file:
   ```bash
   docker build -t car-permutations .
   docker run -v "$(pwd)/data/outputs:/data/outputs" car-permutations
   ```

## Usage

1. **Run the Main Script**
   The script will load `cars_data.csv`, fetch the exchange rate, generate unique car permutations, calculate prices, and save the output to `car_permutations.xlsx`.

   ```bash
   python main.py
   ```

2. **Run Tests**
   To verify functionality, run the unit tests:
   ```bash
   python -m unittest discover Tests
   ```

## CSV File Structure

The CSV file (`cars_data.csv`) should contain the following columns:

- `Property_Name`: Name of the car property.
- `Possible_Values`: Semi-colon separated list of possible values for the property.
- `Condition`: Optional condition for setting the property (e.g., `Q1-IsElectric==False` for EngineSize).

## Example CSV

```csv
Property_Name,Possible_Values,Condition
Q1-IsElectric,True;False,
Q2-KM,100;1000;10000;1000000;10000000,
Q3-EngineSize,1.0;1.2;1.4;3.0;4.8,Q1-IsElectric==False
Q4-Color,Black;Red;White;Yellow,
Q5-ModelData,"{
  ""brand"": ""Ford"",
  ""model"": ""Mustang"",
  ""year"": 1964
};
{
  ""brand"": ""BMW"",
  ""model"": ""M3"",
  ""year"": 1981
};
{
  ""brand"": ""Tesla"",
  ""model"": ""Model 3"",
  ""year"": 2020
}",
```

## Code Explanation

1. **load_data**: Reads the CSV file and sets up each property with its possible values and conditions.
2. **generate_unique_cars**: Creates all unique car configurations by applying conditions and ensuring all configurations meet the specified requirements.
3. **get_exchange_rate**: Fetches the latest USD to CLP exchange rate from Coinbase’s API.
4. **generate_output**: Exports the generated car data to an Excel file, with calculated prices included.

## Example Output

The program saves the final results to an Excel file (`car_permutations.xlsx`) with the following structure:

| Q1-IsElectric | Q2-KM   | Q3-EngineSize | Q4-Color | Q5-ModelData              | Price (CLP) |
|---------------|---------|---------------|----------|---------------------------|-------------|
| False         | 10000   | 1.2           | Black    | {'brand': 'Ford', ...}    | 125,000     |
| True          | 100     | None          | Red      | {'brand': 'Tesla', ...}   | 10,000      |
| ...           | ...     | ...           | ...      | ...                       | ...         |


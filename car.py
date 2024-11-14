from datetime import datetime

class Car:
    def __init__(self, is_electric, km, engine_size, color, model_data):
        if is_electric and engine_size is not None:
            raise ValueError("Electric cars should not have an engine size.")
        self.is_electric = is_electric
        self.km = km
        self.engine_size = engine_size
        self.color = color
        self.model_data = model_data

    def __eq__(self, other):
        if not isinstance(other, Car):
            return False
        return (self.is_electric == other.is_electric and
                self.km == other.km and
                self.engine_size == other.engine_size and
                self.color == other.color and
                self.model_data == other.model_data)

    def __hash__(self):
        return hash((self.is_electric, self.km, self.engine_size, self.color,
                     frozenset(self.model_data.items()) if self.model_data else None))

    def __repr__(self):
        return (f"Car(is_electric={self.is_electric}, km={self.km}, "
                f"engine_size={self.engine_size}, color={self.color}, model_data={self.model_data})")

    def calculate_price(self, exchange_rate):
        if exchange_rate is None:
            raise ValueError("Exchange rate cannot be None")
        # Extract the car's manufacturing year from model_data
        year = self.model_data.get('year')
        if not year:
            raise ValueError("Car's manufacturing year is missing")

        # Calculate days passed since January 1 of the car's manufacturing year
        start_date = datetime(year, 1, 1)
        today = datetime.now()
        days_passed = (today - start_date).days
        # Calculate price
        price = self.km * days_passed * exchange_rate
        return price
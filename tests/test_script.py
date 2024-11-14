from main import Car, generate_unique_cars, load_data
import unittest


class TestCarGeneration(unittest.TestCase):
    def setUp(self):
        # Load sample properties data for testing
        self.properties_data = load_data('data_for_test.csv')
        # Assert that properties_data loaded as expected
        self.assertIsNotNone(self.properties_data, "Failed to load test data for properties")

    def test_unique_cars_generation_returns_non_empty_set(self):
        """Test that unique car generation returns a non-empty set."""
        unique_cars = generate_unique_cars(self.properties_data)
        self.assertIsInstance(unique_cars, set, "Expected a set of unique cars.")
        self.assertGreater(len(unique_cars), 0, "Expected some cars to be generated.")

    def test_electric_car_with_engine_size_raises_error(self):
        """Test that creating an electric car with an engine size raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Car(
                is_electric=True,
                km=1000,
                engine_size=3.0,
                color="Red",
                model_data={"brand": "Ford", "model": "Mustang", "year": 1964}
            )
        self.assertEqual(str(context.exception), "Electric cars should not have an engine size.")


class TestCarPriceCalculation(unittest.TestCase):
    def test_calculate_price(self):
        # Define car properties
        is_electric = False
        km1, km2 = 1000, 10000
        engine_size, color = 3.0, "Red"
        model_data = {"brand": "Ford", "model": "Mustang", "year": 1964}

        # Create two Car instances
        car1 = Car(is_electric=is_electric, km=km1, engine_size=engine_size, color=color, model_data=model_data)
        car2 = Car(is_electric=is_electric, km=km2, engine_size=engine_size, color=color, model_data=model_data)

        # Mock exchange rate
        exchange_rate = 800

        # Calculate and compare prices
        price_car1 = car1.calculate_price(exchange_rate)
        price_car2 = car2.calculate_price(exchange_rate)

        self.assertAlmostEqual(price_car1, price_car2 * 0.1, places=2,
                               msg="Price of car1 should be 1/10th of car2 due to km difference")
        self.assertGreater(price_car2, price_car1, "Car with higher km should have a higher price")

        # Ensure calculate_price raises ValueError if exchange_rate is None
        with self.assertRaises(ValueError):
            car1.calculate_price(None)


if __name__ == '__main__':
    unittest.main()

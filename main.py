# This program inputs the price and performance of a cloud GPU
# calculates and outputs a letter grade (A-F)
import pandas as pd
import logging
import unittest

# Path to the Excel dataset.
DATAFILE = r"C:\Users\Ben\Desktop\pythonProject1\Data\1xA100_80GB_On-Demand_Pricing_Perf_Data.xlsx"

# Initialize logging with DEBUG level to capture all messages.
logging.basicConfig(level=logging.DEBUG)

# Configuration dictionary containing weights for scoring components
# and min-max values for normalization of hardware attributes and pricing.
config = {
  'weights': {
    'form_factor': 0.10,
    'vram': 0.20,
    'ram': 0.18,
    'vcpus': 0.16,
    'internal_storage': .11,
    'price_on_demand': -0.25
  },
  'min_max': {
        'form_factor': {'min': 'PCIe', 'max': 'SXM'},
        'vram': {'min': 40, 'max': 80},                 # VRAM in GB
        'ram': {'min': 90, 'max': 251},                 # RAM in GB
        'vcpus': {'min': 8, 'max': 30},
        'internal_storage': {'min': 0, 'max': 4000},    # Internal Storage in GB
        'price_on_demand': {'min': 1.10, 'max': 3.36}
  }
}


# Function to normalize all attributes in the dataset using pre-defined min-max values.
def normalize_data(df):
    print(df.dtypes)
    form_factor_map = {'PCIe': 0, 'SXM': 1}
    df['Normalized_form_factor'] = df['form_factor'].map(form_factor_map)

    # Loop over all features in the config for normalization
    for feature, values in config['min_max'].items():
        print(feature, df[feature].unique())
        if feature != 'form_factor':
            df[f'Normalized_{feature}'] = (df[feature] - values['min']) / (values['max'] - values['min'])

    # Adjust normalized price, such that lower prices get higher scores.
    df['adjusted_price_score'] = 1 - df['Normalized_price_on_demand']

    return df


# Function to load dataset from an Excel file (DATAFILE).
# Logs successful data loading or any errors encountered.
def load_data():
    try:
        data = pd.read_excel(DATAFILE, sheet_name="Python_Data")
        data['price_on_demand'] = data['price_on_demand'].astype(float)
        logging.info("Data loaded successfully from the Excel file.")
        return data
    except Exception as e:
        logging.error("Error loading the Excel file: %s", e)
        raise e


# Function to convert a numeric score into a letter grade.
def score_to_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


# Main
# Calculate the Price/Performance Score using the normalized values and weights
def run_main():
    data = normalize_data(load_data())

    data['Price/Perf_Score'] = (data['Normalized_form_factor'] * config['weights']['form_factor']) + \
        (data['Normalized_vram'] * config['weights']['vram']) + \
        (data['Normalized_ram'] * config['weights']['ram']) + \
        (data['Normalized_vcpus'] * config['weights']['vcpus']) + \
        (data['Normalized_internal_storage'] * config['weights']['Internal_Storage']) + \
        (data['adjusted_price_score'] * config['weights']['price_on_demand'])


# TESTING
class TestNormalization(unittest.TestCase):
    data = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.data = load_data()
            logging.info("Data loaded successfully from the Excel file.")

            cls.data = normalize_data(cls.data)
            logging.info("Data normalized successfully.")
        except Exception as e:
            logging.error("Error loading the Excel file: %s", e)
            raise e

        logging.info("Data loaded and normalized successfully.")

    def test_score_to_grade(self):
        self.assertEqual(score_to_grade(95), 'A')
        self.assertEqual(score_to_grade(85), 'B')
        self.assertEqual(score_to_grade(65), 'D')
        self.assertEqual(score_to_grade(25), 'F')

    def test_normalized_form_factor(self):
        # Checking if the normalization is within bounds
        self.assertTrue(self.data['Normalized_form_factor'].max() <= 1)
        self.assertTrue(self.data['Normalized_form_factor'].min() >= 0)

    def test_normalized_vram(self):
        # Checking if the normalization is within bounds
        self.assertTrue(self.data['Normalized_vram'].max() <= 1)
        self.assertTrue(self.data['Normalized_vram'].min() >= 0)

    def test_normalized_ram(self):
        self.assertTrue(self.data['Normalized_ram'].max() <= 1)
        self.assertTrue(self.data['Normalized_ram'].min() >= 0)

    def test_normalized_vcpus(self):
        # Checking if the normalization is within bounds
        self.assertTrue(self.data['Normalized_vcpus'].max() <= 1)
        self.assertTrue(self.data['Normalized_vcpus'].min() >= 0)

    def test_normalized_internal_storage(self):
        self.assertTrue(self.data['Normalized_internal_storage'].max() <= 1)
        self.assertTrue(self.data['Normalized_internal_storage'].min() >= 0)

    def test_normalized_price_on_demand(self):
        self.assertTrue(self.data['Normalized_price_on_demand'].max() <= 1)
        self.assertTrue(self.data['Normalized_price_on_demand'].min() >= 0)


# This condition ensures the unittest module's test discovery mechanism
# will execute the tests in this script when the script is run directly.
# It won't execute if the script is imported as a module elsewhere.
if __name__ == '__main__':
    unittest.main()

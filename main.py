import pandas as pd
import logging
import unittest

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Configuration
config = {
  'weights': {
    'Form_factor': 0.125,
    'VRAM': 0.15,
    'RAM': 0.15,
    'vCPUs': 0.15,
    'Internal_Storage': 0.075,
    'Price_On_Demand': -0.25
  },

  'min_max': {
    'Form_factor': {
      'min': 'PCIe',
      'max': 'SXM'
    },
   'VRAM': {
      'min': 40,
      'max': 80
    },
    'RAM': {
      'min': 90,
      'max': 251
    },
    'vCPUs': {
      'min': 8,
      'max': 30
    },
    'Internal_Storage': {
      'min': 0,
      'max': 4000
    },
    'Price_On_Demand': {
      'min': 1.10,
      'max': 3.36
    }
  }
}

# Normalize function
def normalize_data(df):

  # Form factor
  form_factor_map = {'PCIe': 0, 'SXM': 1}
  df['Normalized_Form_factor'] = df['Form_factor'].map(form_factor_map)

  # VRAM
  min_val = config['min_max']['VRAM']['min']
  max_val = config['min_max']['VRAM']['max']
  df['Normalized_VRAM'] = (df['VRAM'] - min_val) / (max_val - min_val)

  # Similarly for other columns

  return df


# Loading data
def load_data():
    try:
        data = pd.read_excel("C:\\Users\\Ben\\Desktop\\pythonProject1\\Data\\1xA100_80GB_On-Demand_Pricing_Perf_Data.xlsx", sheet_name="Python_Data")
        logging.info("Data loaded successfully from the Excel file.")
        return data
    except Exception as e:
        logging.error("Error loading the Excel file: %s", e)
        raise e  # re-raise the exception so that the script halts if there's an error

data = normalize_data(load_data())

# Convert the Price_On_Demand column from a string to a float
data['Price_On_Demand'] = data['Price_On_Demand'].astype(float)

# Normalize and process the data

form_factor_map = {'PCIe': 0, 'SXM': 1}
data['Normalized_Form_factor'] = data['Form_factor'].map(form_factor_map)

data['Normalized_VRAM'] = (data['VRAM'] - config['min_max']['VRAM']['min']) / (config['min_max']['VRAM']['max'] - config['min_max']['VRAM']['min'])

for feature, values in config['min_max'].items():
    if feature != 'Form_factor':  # since we already handled Form_factor
        data[f'Normalized_{feature}'] = (data[feature] - values['min']) / (values['max'] - values['min'])

max_price = data['Price_On_Demand'].max()
min_price = data['Price_On_Demand'].min()
data['Normalized_Price'] = (data['Price_On_Demand'] - min_price) / (max_price - min_price)

data['Adjusted_Price_Score'] = 1 - data['Normalized_Price']



data['Price/Perf_Score'] = (data['Normalized_Form_factor'] * config['weights']['Form_factor']) + \
                          (data['Normalized_VRAM'] * config['weights']['VRAM']) + \
                          (data['Normalized_RAM'] * config['weights']['RAM']) + \
                          (data['Normalized_vCPUs'] * config['weights']['vCPUs']) + \
                          (data['Normalized_Internal_Storage'] * config['weights']['Internal_Storage']) + \
                          (data['Adjusted_Price_Score'] * config['weights']['Price_On_Demand'])

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


#TESTING
class TestNormalization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()
        cls.data = normalize_data(cls.data)

        # Normalize Form factor
        form_factor_map = {'PCIe': 0, 'SXM': 1}
        cls.data['Normalized_Form_factor'] = cls.data['Form_factor'].map(form_factor_map)

        # Normalize VRAM
        min_val = config['min_max']['VRAM']['min']
        max_val = config['min_max']['VRAM']['max']
        cls.data['Normalized_VRAM'] = (cls.data['VRAM'] - min_val) / (max_val - min_val)

        # Normalize RAM
        min_val = config['min_max']['RAM']['min']
        max_val = config['min_max']['RAM']['max']
        cls.data['Normalized_RAM'] = (cls.data['RAM'] - min_val) / (max_val - min_val)

        # Normalize vCPUs
        min_val = config['min_max']['vCPUs']['min']
        max_val = config['min_max']['vCPUs']['max']
        cls.data['Normalized_vCPUs'] = (cls.data['vCPUs'] - min_val) / (max_val - min_val)

        # Normalize Storage
        min_val = config['min_max']['Internal_Storage']['min']
        max_val = config['min_max']['Internal_Storage']['max']
        cls.data['Normalized_Internal_Storage'] = (cls.data['Internal_Storage'] - min_val) / (max_val - min_val)

        # Normalize Price
        min_val = config['min_max']['Price_On_Demand']['min']
        max_val = config['min_max']['Price_On_Demand']['max']
        cls.data['Normalized_Price'] = (cls.data['Price_On_Demand'] - min_val) / (max_val - min_val)

        try:
            logging.info("Data loaded successfully from the Excel file.")
        except Exception as e:
            logging.error("Error loading the Excel file: %s", e)
            raise e  # If there's an error loading the data, you probably want to halt execution.

    def test_score_to_grade(self):
        self.assertEqual(score_to_grade(95), 'A')
        self.assertEqual(score_to_grade(85), 'B')
        self.assertEqual(score_to_grade(65), 'D')
        self.assertEqual(score_to_grade(25), 'F')

    def test_normalized_Form_factor(self):

        # Print the maximum normalized value
        print(self.data['Normalized_Form_factor'].max())  # <--- Add this line

        # Checking if the normalization is within bounds
        self.assertTrue(self.data['Normalized_Form_factor'].max() <= 1)
        self.assertTrue(self.data['Normalized_Form_factor'].min() >= 0)

    def test_normalized_VRAM(self):
        # Assuming you have similar min and max for VRAM in your config
        min_val = config['min_max']['VRAM']['min']
        max_val = config['min_max']['VRAM']['max']

        # Checking if the normalization is within bounds
        self.data['Normalized_VRAM'] = (self.data['VRAM'] - min_val) / (max_val - min_val)
        self.assertTrue(self.data['Normalized_VRAM'].max() <= 1)
        self.assertTrue(self.data['Normalized_VRAM'].min() >= 0)

    def test_normalized_RAM(self):
        min_val = config['min_max']['RAM']['min']
        max_val = config['min_max']['RAM']['max']
        self.data['Normalized_RAM'] = (self.data['RAM'] - min_val) / (max_val - min_val)
        self.assertTrue(self.data['Normalized_RAM'].max() <= 1)
        self.assertTrue(self.data['Normalized_RAM'].min() >= 0)

    def test_normalized_vCPUs(self):
        min_val = config['min_max']['vCPUs']['min']
        max_val = config['min_max']['vCPUs']['max']

        # Print the maximum normalized value
        print(self.data['Normalized_vCPUs'].min(), self.data['Normalized_vCPUs'].max())

        # Checking if the normalization is within bounds
        self.data['Normalized_vCPUs'] = (self.data['vCPUs'] - min_val) / (max_val - min_val)
        self.assertTrue(self.data['Normalized_vCPUs'].max() <= 1)
        self.assertTrue(self.data['Normalized_vCPUs'].min() >= 0)

    def test_normalized_Internal_Storage(self):
        min_val = config['min_max']['Internal_Storage']['min']
        max_val = config['min_max']['Internal_Storage']['max']
        self.data['Normalized_Internal_Storage'] = (self.data['Internal_Storage'] - min_val) / (max_val - min_val)
        self.assertTrue(self.data['Normalized_Internal_Storage'].max() <= 1)
        self.assertTrue(self.data['Normalized_Internal_Storage'].min() >= 0)

    def test_normalized_Price_On_Demand(self):
        min_val = config['min_max']['Price_On_Demand']['min']
        max_val = config['min_max']['Price_On_Demand']['max']

        # Print the maximum normalized value
        print(self.data['Normalized_Price'].min(), self.data['Normalized_Price'].max())

        self.data['Normalized_Price'] = (self.data['Price_On_Demand'] - min_val) / (max_val - min_val)
        self.assertTrue(self.data['Normalized_Price'].max() <= 1)
        self.assertTrue(self.data['Normalized_Price'].min() >= 0)

# Remember to run the tests if this is your main testing script
if __name__ == '__main__':
    unittest.main()

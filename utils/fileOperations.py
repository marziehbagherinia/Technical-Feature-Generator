from utils.config import *
from utils.libraries import *

def prepare_input_filename(coin):
    filename = INPUT_PATH + INPUT_FILE_NAME.format(coin_name = coin, duration = DURATION)
    return filename

def prepare_output_filename(coin):
    filename = OUTPUT_PATH + OUTPUT_FILE_NAME.format(coin_name = coin, duration = DURATION)
    return filename

def read_input_data(filename):    
    data = pd.read_csv(filename)
    return data

def write_output_data(filename, data):
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    data.to_csv(filename, sep = ',')
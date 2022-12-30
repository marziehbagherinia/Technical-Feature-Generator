from utils.config import *
from utils.fileOperations import *
from FeatureGenerator.FeatureGenerator import FeatureGenerator

def main():
    for coin in COINS:
        print('Strat {coin_name} Feature Extraction: '.format(coin_name = coin))
        filename = prepare_input_filename(coin)

        data = read_input_data(filename)

        featureGenerator = FeatureGenerator(data)
        featureGenerator.generate()

        filename = prepare_output_filename(coin)
        write_output_data(filename, featureGenerator.data)

    print('Feature Extraction Finished Successfuly ...')

if __name__ == "__main__":
    main()
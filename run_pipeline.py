from data_pipeline.to_json import parse_drug_details, parse_diseases, \
    parse_drug_reviews, parse_pharmaceutical_companies, \
    parse_sicknesses
from data_pipeline.wikipedia_scraper import get_companies, get_diseases


if __name__ == '__main__':

    print("Parsing drug details...")
    parse_drug_details()

    print("\nParsing sicknesses...")
    parse_sicknesses()

    print("\nParsing drug reviews...")
    parse_drug_reviews()

    while True:
        answer = input("\nDo you wish to download pharmaceutical company data from Wikipedia? (may take 1-3 minutes) (y/n): ")
        if answer[0].lower() == 'y':
            print("Downloading pharmaceutical company data...")
            get_companies()
            print("Parsing pharmaceutical company data...")
            parse_pharmaceutical_companies()
            break
        elif answer[0].lower() == 'n':
            print("Skipping company data download.")
            break
        else:
            print("Please answer yes or no.")

    while True:
        answer = input("\nDo you wish to download disease data from Wikipedia? (may take 1-3 minutes) (y/n): ")
        if answer[0].lower() == 'y':
            print("Downloading disease data...")
            get_diseases()
            print("Parsing disease data...")
            parse_diseases()
            break
        elif answer.lower() == 'n':
            print("Skipping disease data download.")
            break
        else:
            print("Please answer yes or no.")

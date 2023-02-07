import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    response = urllib.request.urlopen(url)
    csv_content = response.read().decode("utf-8")
    return csv_content


def processData(file_content):
    lines = file_content.strip().split("\n")
    personData = {}
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="errors.log", level=logging.ERROR, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger("assignment2")
    for i, line in enumerate(lines):
        values = line.strip().split(",")
        id = int(values[0])
        name = values[1]
        try:
            birthday = datetime.datetime.strptime(values[2], "%d/%m/%Y").date()
            personData[id] = (name, birthday)
        except ValueError:
            logger.error(f"Error processing line #{i+1} for ID #{id}")
    return personData


def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    try:
        csvData = downloadData(url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    personData = processData(csvData)
    while True:
        try:
            id = int(input("Enter an ID (0 to exit): "))
            if id == 0:
                break
            displayPerson(id, personData)
        except ValueError:
            print("Invalid input, please enter a valid number")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    

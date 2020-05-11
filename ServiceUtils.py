import logging

def getDataByZipCode(data, zipCode):
    try:
        for zip_value in data["zip_values"]:
            if zip_value["zip"] == zipCode:
                zip_value.update({ "LastUpdateDate" : data["LastUpdateDate"]})
                return zip_value
        return "Could not find requested zipcode!"
    except ValueError:
            logging.error("Decoding json has failed!")
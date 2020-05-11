import requests, requests_cache, logging, json
from flask import Flask
from flask_restful import Resource, Api
import ServiceUtils

app = Flask(__name__)
api = Api(app)

# Logging Properties and Conditions
isProdEnvironment = False
loggingLevel = logging.INFO if isProdEnvironment else logging.DEBUG
logFileName = "ICDS.log" if isProdEnvironment else "ICDS_Debug.log"

# Enable logging
logging.basicConfig(filename=logFileName,
                    filemode="a",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt="%H:%M:%S", 
                    level=loggingLevel)
logging.info("Running Illinois Covid19 Data Service...")
logging = logging.getLogger("ICDS")

# This is required to cache calls for x seconds for any request
requests_cache.install_cache(cache_name="ICDS_cache", backend="sqlite", expire_after=180)

# Gets data from datasource
def getData():
    try:
        response = requests.get('https://www.dph.illinois.gov/sitefiles/COVIDZip.json')
        data = json.loads(response.text)
        logging.info(response.from_cache)
        return data
    except requests.exceptions.RequestException as e:
        logging.error(e)

## Service Endpoints ##
class ZipCodeDump(Resource):
    def get(self):
        return getData()

class ZipCode(Resource):
    def get(self, zipCode):
        logging.info("ZipCode Endpointed Called.")
        return ServiceUtils.getDataByZipCode(getData(), zipCode)

api.add_resource(ZipCodeDump, "/zip")
api.add_resource(ZipCode, "/zip/<string:zipCode>")

if __name__ == "__main__":
    app.run(debug=True)
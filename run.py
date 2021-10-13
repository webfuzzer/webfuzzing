from src import fuzz
import yaml

with open('url.yml') as f:
    URL_LIST = yaml.load(stream=f, Loader=yaml.FullLoader)
    print(URL_LIST)
    fuzz(URL_LIST)

    exit()
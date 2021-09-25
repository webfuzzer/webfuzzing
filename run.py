import yaml

with open('url.yml') as f:
    URL_LIST = yaml.load(stream=f, Loader=yaml.FullLoader)
"""
Modules for parsing the input file utilizing LUTs, GPT, and other methods.
"""

import json
import openai
from . import extractor


def csv_to_dict(file_path: str):
    tempDict = {}
    with open(file_path) as csvFile:
        for line in csvFile:
            # Get index of first comma
            firstComma = line.find(",")  
            tempValue = line[firstComma+1:].strip()
            tempValue = tempValue[1:-1] if tempValue.startswith("\"") and tempValue.endswith("\"") else tempValue
            tempDict[line[:firstComma]] = tempValue
    print(tempDict)
    return tempDict

def json_to_dict(json_path: str):
    with open(json_path) as f:
        return json.load(f)



def parse_config_with_lut(self, config: dict):
    # Modify the config dict so for every value which is a list, use the LUT to lookup and create
    # new key-value pairs within this config
    tempConfig = {}
    print(config)
    for key, value in config.items():
        if isinstance(value, list):
            for i, item in enumerate(value):
                if item in self.LUT.keys():
                    tempConfig[f"{key}_{i + 1}_KEY"] = item
                    tempConfig[f"{key}_{i + 1}_VALUE"] = self.LUT[item]
                else:
                    self.logger.log(f"└-- {self.logger.format(item, 2)} not found in LUT.", 2)
                    tempConfig[f"{key}_{i + 1}_KEY"] = item
                    tempConfig[f"{key}_{i + 1}_VALUE"] = item
        else:
            tempConfig[key] = value
    return tempConfig

def parse_config_with_gpt(self, config: dict, openai_key: str, gpt_model: str = "gpt-3.5-turbo"):
    # Do the same as parse_config_with_lut, but use GPT-3 to lookup the values
    # Requires the required library and your own API code. (Promise wont mess with your API)
    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
        ]
    )
    pass

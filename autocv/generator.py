"""
Modules for generating paragraphs based on keywords and other methods.
"""

import json
import openai

def generate_para_with_lut(self, config: dict):
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

def generate_para_with_gpt(config: dict, openai_key: str, gpt_model: str = "gpt-3.5-turbo"):
    # Do the same as parse_config_with_lut, but use GPT-3 to lookup the values
    # Requires the required library and your own API code. (Promise wont mess with your API)
    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
                {"role": "system", "content": "You are a helpful assistant who will help me generate a cover letter paragraph based on the given skill, my resume, and the job description."},
                {"role": "user", "content": "Who won the world series in 2020?"},
        ]
    )
    pass



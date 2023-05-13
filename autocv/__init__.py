import os
import json
import glob
import re
import timeit
import time
import pylumber
import copy

from docx import Document
from dotenv import dotenv_values

from . import parser
from . import extractor

# Credits to Scanny for the code below:
def paragraph_replace_text(paragraph, regex, replace_str):
    """Return `paragraph` after replacing all matches for `regex` with `replace_str`.

    `regex` is a compiled regular expression prepared with `re.compile(pattern)`
    according to the Python library documentation for the `re` module.
    """
    # --- a paragraph may contain more than one match, loop until all are replaced ---
    while True:
        text = paragraph.text
        match = regex.search(text)
        if not match:
            break

        # --- when there's a match, we need to modify run.text for each run that
        # --- contains any part of the match-string.
        runs = iter(paragraph.runs)
        start, end = match.start(), match.end()

        # --- Skip over any leading runs that do not contain the match ---
        for run in runs:
            run_len = len(run.text)
            if start < run_len:
                break
            start, end = start - run_len, end - run_len

        # --- Match starts somewhere in the current run. Replace match-str prefix
        # --- occurring in this run with entire replacement str.
        run_text = run.text
        run_len = len(run_text)
        run.text = "%s%s%s" % (run_text[:start], replace_str, run_text[end:])
        end -= run_len  # --- note this is run-len before replacement ---

        # --- Remove any suffix of match word that occurs in following runs. Note that
        # --- such a suffix will always begin at the first character of the run. Also
        # --- note a suffix can span one or more entire following runs.
        for run in runs:  # --- next and remaining runs, uses same iterator ---
            if end <= 0:
                break
            run_text = run.text
            run_len = len(run_text)
            run.text = run_text[end:]
            end -= run_len

    # --- optionally get rid of any "spanned" runs that are now empty. This
    # --- could potentially delete things like inline pictures, so use your judgement.
    # for run in paragraph.runs:
    #     if run.text == "":
    #         r = run._r
    #         r.getparent().remove(r)

    return paragraph  


class docx_template():
    def __init__(self, lut: dict, template: str, output_dir: str = "output", silent: bool = False):
        # Loading template docx file for editing
        self.logger = pylumber.lumberjack(silent=False)
        self.logger.log(f"Loading template `{self.logger.format(template, 2)}`", "INFO")
        
        # Setting self variables
        self.LUT = lut
        self.TEMPLATE = Document(template)
        
        # Check to see if output directory exists
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            self.logger.log(f"Created output directory: {output_dir}")
        self.OUTPUT_DIR = output_dir

    def keyword_extraction(self, text: str):
        # Extract keywords from text
        pass

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

    def find_and_replace_single(self, config: dict):
        # config: requires UID field
        try:
            assert "UID" in config.keys()
        except AssertionError:
            self.logger.log(f"└-- {self.logger.format('UID', 2)} field not found in config file.", 2)
            return
        tempConfig = config
        tempDocx = copy.deepcopy(self.TEMPLATE)
        tempConfig = self.parse_config_with_lut(tempConfig)
    
        for key, value in tempConfig.items():
            reMFR = re.compile(r"\$\{" + key + r"\}")
            for paragraph in tempDocx.paragraphs:
                paragraph = paragraph_replace_text(paragraph, reMFR, value)

        # Save the edited document within output directory
        savePath = f"{self.OUTPUT_DIR}/{tempConfig['UID']}.docx"
        tempDocx.save(savePath)
        self.logger.log(f"└-- Saved document at `{self.logger.format(savePath, 2)}`", "OK")
        return savePath

    def find_and_replace_folder(self, config_path: str, parser: callable = parser.json_to_dict):
        # Obtain all .json files from config directory
        outputList = []
        for config_file in glob.glob(f"{config_path}/*.json"):
            self.logger.log(f"Processing `{self.logger.format(config_file, 2)}` configuration file.", "INFO")
            outputList.append(self.find_and_replace_single(parser(config_file)))
        return outputList
        
    def __exit__(self):
        print("Exiting...")

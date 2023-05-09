import os
import json
import glob
import re

from docx import Document
from dotenv import dotenv_values

print(os.path.exists(".env.example"))

# Check .env file exists
if not os.path.exists(".env.example"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

# Load environment variables
ENV = dict(dotenv_values(".env.example"))


def json_to_dict(json_path: str):
    with open(json_path) as f:
        return json.load(f)

def csv_to_dict(file_path: str):
    tempDict = {}
    with open(file_path) as csvFile:
        for line in csvFile:
            # Get index of first comma
            firstComma = line.find(",")
            tempDict[line[:firstComma]] = line[firstComma+1:].strip()
            
    print(tempDict)
    return tempDict

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


class template():
    def __init__(self, lut: dict, template: str):
        # Open and parse json config file:
        self.LOOKUP = lut
        self.TEMPLATE = template

    def find_and_replace_single(self, config: json):
        # Returns: Docx Document
        tempConfig = json_to_dict(config)
        tempDocx = Document(self.TEMPLATE)

        print(tempConfig)

        # Do reactjs replacement 
        reMFR = re.compile(r"\{([^}]*)\}")
        for paragraph in tempDocx.paragraphs:
            paragraph = paragraph_replace_text(paragraph, reMFR, "TEMPTEXT")
        # Save the edited document within output directory
        tempDocx.save(f"{ENV['OUTPUT_DIR']}/{tempConfig['UID']}.docx")
        print(tempConfig)
        
        
    
    def find_and_replace_group(self, config_path: str):
        print(config_path)

    def __exit__(self):
        print("Exiting...")

# Iterate through all .json files in the config directory

CVGeneration = template(csv_to_dict(ENV["LUT_PATH"]), ENV["TEMPLATE_PATH"])
for config_file in glob.glob(f"{ENV['CONFIG_DIR']}/*.json"):
    CVGeneration.find_and_replace_single(config_file)

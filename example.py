import os
import glob
import autocv
import timeit

from dotenv import dotenv_values


# Check .env file exists
if not os.path.exists(".env.example"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

# Load environment variables
ENV = dict(dotenv_values(".env.example"))

# Get current time
start = timeit.default_timer()
# Iterate through all .json files in the config directory
CVGeneration = autocv.template(autocv.csv_to_dict(ENV["LUT_PATH"]), ENV["TEMPLATE_PATH"], ENV["OUTPUT_DIR"])
for config_file in glob.glob(f"{ENV['CONFIG_DIR']}/*.json"):
    CVGeneration.find_and_replace_single(config_file)

# Get current time
stop = timeit.default_timer()
print(f"Time taken: {stop - start}")



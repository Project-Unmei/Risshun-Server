import os
import glob
import autocv
import timeit
import pylumber as log


from dotenv import dotenv_values

currDir = os.path.dirname(os.path.realpath(__file__))

# Check .env file exists
if not os.path.exists(f"{currDir}/.env.example"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

# Load environment variables
ENV = dict(dotenv_values(f"{currDir}/.env.example"))
for key, value in ENV.items():
    ENV[key] = f"{currDir}/{value}"

print(ENV)

# Get current time
start = timeit.default_timer()
# Iterate through all .json files in the config directory
CVGeneration = autocv.docx_template(autocv.csv_to_dict(ENV["LUT_PATH"]), ENV["TEMPLATE_PATH"], ENV["OUTPUT_DIR"])
CVGeneration.find_and_replace_folder(f"{ENV['CONFIG_DIR']}")

# Get current time
stop = timeit.default_timer()
print(f"Time taken: {stop - start}")



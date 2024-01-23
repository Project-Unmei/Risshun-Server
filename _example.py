import os
import glob
import risshun
import timeit
import pylumber

from dotenv import dotenv_values

currDir = os.path.dirname(os.path.realpath(__file__))

# Check .env file exists
if not os.path.exists(f"{currDir}/.env"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

# Load environment variables
ENV = dict(dotenv_values(f"{currDir}/.env"))
#for key, value in ENV.items():
#    ENV[key] = f"{currDir}/{value}"

# Get current time
start = timeit.default_timer()
# Iterate through all .json files in the config directory
CVGeneration = risshun.docx_template(ENV["TEMPLATE_PATH"],
                                    ENV["RESUME_PATH"],
                                    ENV["OUTPUT_DIR"], 
                                    openai_key=ENV["OPENAI_KEY"], 
                                    silent=False)
genOutput = CVGeneration.find_and_replace_folder(f"{ENV['CONFIG_DIR']}", risshun.parser.json_path_to_dict)

print(genOutput)


# Get current time
stop = timeit.default_timer()
print(f"Time taken: {stop - start}")



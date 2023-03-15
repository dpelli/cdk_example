import logging
from pathlib import Path
from os import makedirs
from concurrent.futures import ProcessPoolExecutor
import pandas as pd

# filename = Path(__file__).stem
# logger = logging.getLogger(filename)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logging.basicConfig()


# save data to a file
def save_file(path, idx, data):
    logger.info("Starting df to excel.")

    filepath = f"{path}/{idx+1}.xlsx"

    try:
        df = pd.DataFrame(data.dict(), index=[0])
        df.to_excel(filepath, engine="xlsxwriter")
    except Exception as e:
        logger.error("Issue creating df excel.", exc_info=True)


# generate many data files in a directory
def process_via_threading(path, data_list):
    logger.info("Starting threading.")

    # create a local directory to save files
    makedirs(path, exist_ok=True)
    # create the process pool
    with ProcessPoolExecutor() as executor:
        try:
            # submit tasks to generate files
            _ = [
                executor.submit(save_file, path, idx, data)
                for idx, data in enumerate(data_list)
            ]
        except Exception as e:
            logger.error("Issue with threading.", exc_info=True)


def process_normal(path, data_list):
    logger.info("Starting normal process.")

    # create a local directory to save files
    makedirs(path, exist_ok=True)

    for idx, data in enumerate(data_list):
        save_file(path, idx, data)

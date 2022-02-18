import logging
import logging.config
from datetime import date
# Format
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Set file logger
filename = f"app.{date.today().isoformat()}.log"
logging.basicConfig(filename=filename, filemode='a', format=format)

# create logger
logger = logging.getLogger('vc')
logger.setLevel(logging.DEBUG)

# create console handler and add to logger
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(format))
logger.addHandler(ch)
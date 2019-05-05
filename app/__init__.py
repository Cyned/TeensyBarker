from app.logger.logger import create_parser_logger, create_collection_logger, create_app_logger, create_basic_logger

app_logger     = create_app_logger()
parser_logger  = create_parser_logger()
collect_logger = create_collection_logger()
basic_logger   = create_basic_logger()

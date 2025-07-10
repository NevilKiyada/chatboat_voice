"""
Logger Configuration
Sets up logging for the application
"""

import os
import logging
from logging.handlers import RotatingFileHandler
import colorlog
from datetime import datetime

def setup_logger(name: str = None, log_file: str = None) -> logging.Logger:
    """
    Set up application logger with both file and console handlers
    
    Args:
        name: Logger name (default: 'voice_chatbot')
        log_file: Log file path (default: from environment)
    
    Returns:
        Configured logger instance
    """
    
    # Get logger name
    logger_name = name or 'voice_chatbot'
    logger = logging.getLogger(logger_name)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    # Get log level from environment
    log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())
    logger.setLevel(log_level)
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up log file path
    if not log_file:
        log_file = os.getenv('LOG_FILE', os.path.join(log_dir, 'chatbot.log'))
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s: %(message)s',
        datefmt='%H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log startup message
    logger.info(f"Logger '{logger_name}' initialized with level {logging.getLevelName(log_level)}")
    logger.info(f"Log file: {log_file}")
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Get existing logger or create new one
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    logger_name = name or 'voice_chatbot'
    logger = logging.getLogger(logger_name)
    
    # If logger doesn't have handlers, set it up
    if not logger.handlers:
        return setup_logger(logger_name)
    
    return logger

def log_function_call(func):
    """
    Decorator to log function calls
    
    Usage:
        @log_function_call
        def my_function():
            pass
    """
    def wrapper(*args, **kwargs):
        logger = get_logger()
        func_name = func.__name__
        
        # Log function entry
        logger.debug(f"Entering {func_name} with args={args}, kwargs={kwargs}")
        
        try:
            # Execute function
            result = func(*args, **kwargs)
            
            # Log successful completion
            logger.debug(f"Completed {func_name} successfully")
            return result
            
        except Exception as e:
            # Log exception
            logger.error(f"Error in {func_name}: {str(e)}")
            raise
    
    return wrapper

def log_api_request(request_data: dict, response_data: dict = None, endpoint: str = None):
    """
    Log API request and response
    
    Args:
        request_data: Request data to log
        response_data: Response data to log
        endpoint: API endpoint name
    """
    logger = get_logger()
    
    endpoint_name = endpoint or 'unknown'
    
    # Log request
    logger.info(f"API Request to {endpoint_name}: {request_data}")
    
    # Log response if provided
    if response_data:
        logger.info(f"API Response from {endpoint_name}: {response_data}")

def log_performance(func):
    """
    Decorator to log function performance
    
    Usage:
        @log_performance
        def slow_function():
            pass
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger()
        func_name = func.__name__
        
        # Record start time
        start_time = time.time()
        
        try:
            # Execute function
            result = func(*args, **kwargs)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log performance
            logger.info(f"Performance: {func_name} executed in {execution_time:.4f} seconds")
            
            return result
            
        except Exception as e:
            # Log error with performance info
            execution_time = time.time() - start_time
            logger.error(f"Error in {func_name} after {execution_time:.4f} seconds: {str(e)}")
            raise
    
    return wrapper

def setup_flask_logging(app):
    """
    Set up Flask application logging
    
    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        # Set up file logging for production
        logger = setup_logger('flask_app')
        app.logger.handlers = logger.handlers
        app.logger.setLevel(logger.level)
        
        # Log application startup
        app.logger.info('Voice Chatbot application startup')

class DatabaseLogHandler(logging.Handler):
    """
    Custom log handler to store logs in database
    (Optional - can be used for advanced logging)
    """
    
    def __init__(self, db_manager=None):
        super().__init__()
        self.db_manager = db_manager
    
    def emit(self, record):
        """
        Emit a log record to database
        """
        try:
            if self.db_manager:
                log_entry = {
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno,
                    'timestamp': datetime.fromtimestamp(record.created)
                }
                # Here you would save to database
                # self.db_manager.save_log_entry(log_entry)
        except Exception:
            # Don't let logging errors crash the application
            pass

"""
Validation Utility Module

This module provides input validation functions for the Google Ads MCP Server to ensure
data integrity, parameter correctness, and API compliance.
"""

import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple, Callable

logger = logging.getLogger(__name__)

def validate_customer_id(customer_id: str) -> bool:
    """
    Validate that a customer ID is in the correct format.
    
    Args:
        customer_id: The customer ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not customer_id:
        logger.warning("Customer ID is empty")
        return False
    
    # Remove any dashes
    clean_id = customer_id.replace("-", "")
    
    # Check if it's 10 digits
    if not clean_id.isdigit() or len(clean_id) != 10:
        logger.warning(f"Invalid customer ID format: {customer_id}")
        return False
    
    return True

def validate_date_format(date_str: str) -> bool:
    """
    Validate that a date string is in YYYY-MM-DD format.
    
    Args:
        date_str: The date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not date_str:
        return False
    
    # Check format
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not date_pattern.match(date_str):
        logger.warning(f"Invalid date format: {date_str}, expected YYYY-MM-DD")
        return False
    
    # Check if it's a valid date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        logger.warning(f"Invalid date: {date_str}")
        return False

def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate that a date range is valid.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        True if valid, False otherwise
    """
    # Validate each date format
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return False
    
    # Check if start_date is before end_date
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    if start > end:
        logger.warning(f"Invalid date range: start_date {start_date} is after end_date {end_date}")
        return False
    
    return True

def validate_enum(value: str, valid_values: List[str], case_sensitive: bool = False) -> bool:
    """
    Validate that a value is one of a list of valid values.
    
    Args:
        value: The value to validate
        valid_values: List of valid values
        case_sensitive: Whether the comparison should be case-sensitive
        
    Returns:
        True if valid, False otherwise
    """
    if value is None:
        return False
    
    if not case_sensitive:
        value = value.upper()
        valid_values = [v.upper() for v in valid_values]
    
    if value not in valid_values:
        logger.warning(f"Invalid value: {value}, expected one of: {', '.join(valid_values)}")
        return False
    
    return True

def validate_numeric_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None, 
                          max_value: Optional[Union[int, float]] = None) -> bool:
    """
    Validate that a numeric value is within a specified range.
    
    Args:
        value: The value to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        
    Returns:
        True if valid, False otherwise
    """
    if value is None:
        return False
    
    if min_value is not None and value < min_value:
        logger.warning(f"Value {value} is less than minimum {min_value}")
        return False
    
    if max_value is not None and value > max_value:
        logger.warning(f"Value {value} is greater than maximum {max_value}")
        return False
    
    return True

def validate_string_length(text: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
    """
    Validate that a string length is within specified bounds.
    
    Args:
        text: The string to validate
        min_length: Minimum allowed length (inclusive)
        max_length: Maximum allowed length (inclusive)
        
    Returns:
        True if valid, False otherwise
    """
    if text is None:
        return False
    
    if len(text) < min_length:
        logger.warning(f"String length {len(text)} is less than minimum {min_length}")
        return False
    
    if max_length is not None and len(text) > max_length:
        logger.warning(f"String length {len(text)} is greater than maximum {max_length}")
        return False
    
    return True

def validate_regex(text: str, pattern: str) -> bool:
    """
    Validate that a string matches a regex pattern.
    
    Args:
        text: The string to validate
        pattern: Regular expression pattern
        
    Returns:
        True if valid, False otherwise
    """
    if text is None:
        return False
    
    regex = re.compile(pattern)
    if not regex.match(text):
        logger.warning(f"String '{text}' does not match pattern '{pattern}'")
        return False
    
    return True

def validate_all(validations: List[Tuple[Callable, List, Dict]]) -> bool:
    """
    Run multiple validation functions and return True only if all pass.
    
    Args:
        validations: List of tuples (validation_function, args, kwargs)
        
    Returns:
        True if all validations pass, False otherwise
    """
    for validation_func, args, kwargs in validations:
        if not validation_func(*args, **kwargs):
            return False
    
    return True

def validate_any(validations: List[Tuple[Callable, List, Dict]]) -> bool:
    """
    Run multiple validation functions and return True if any pass.
    
    Args:
        validations: List of tuples (validation_function, args, kwargs)
        
    Returns:
        True if any validation passes, False otherwise
    """
    for validation_func, args, kwargs in validations:
        if validation_func(*args, **kwargs):
            return True
    
    return False

def sanitize_input(value: str, max_length: Optional[int] = None, allowed_chars: Optional[str] = None) -> str:
    """
    Sanitize input string by applying length limits and character restrictions.
    
    Args:
        value: Input string to sanitize
        max_length: Maximum allowed length
        allowed_chars: Regex pattern of allowed characters
        
    Returns:
        Sanitized string
    """
    if value is None:
        return ""
    
    # Apply length limit
    if max_length is not None and len(value) > max_length:
        value = value[:max_length]
    
    # Apply character restrictions
    if allowed_chars is not None:
        regex = re.compile(f"[^{re.escape(allowed_chars)}]")
        value = regex.sub("", value)
    
    return value

# This file now serves as a compatibility layer for the new modular analysis structure
from .analysis import perform_stock_analysis

# Re-export the main function for backward compatibility
__all__ = ["perform_stock_analysis"] 
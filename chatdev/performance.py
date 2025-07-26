"""
Performance monitoring and optimization utilities for ChatDev.
"""

import time
import logging
import functools
from typing import Callable, Any


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapped function with timing
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            if execution_time > 1.0:  # Log slow operations
                logging.info(f"Function {func.__name__} took {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logging.error(f"Function {func.__name__} failed after {execution_time:.2f} seconds: {e}")
            raise
    return wrapper


class PerformanceMonitor:
    """
    Simple performance monitoring for ChatDev operations.
    """
    
    def __init__(self):
        self.metrics = {}
        
    def start_timer(self, operation: str) -> None:
        """Start timing an operation."""
        self.metrics[operation] = time.time()
        
    def end_timer(self, operation: str) -> float:
        """End timing an operation and return duration."""
        if operation in self.metrics:
            duration = time.time() - self.metrics[operation]
            del self.metrics[operation]
            return duration
        return 0.0
        
    def log_slow_operations(self, threshold: float = 5.0) -> None:
        """Log operations that exceed the threshold."""
        current_time = time.time()
        for operation, start_time in self.metrics.items():
            duration = current_time - start_time
            if duration > threshold:
                logging.warning(f"Long-running operation: {operation} ({duration:.2f}s)")


def cache_result(max_size: int = 128):
    """
    Simple LRU cache decorator for expensive operations.
    
    Args:
        max_size: Maximum cache size
        
    Returns:
        Cache decorator
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        access_order = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                # Move to end (most recently used)
                access_order.remove(key)
                access_order.append(key)
                return cache[key]
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Add to cache
            cache[key] = result
            access_order.append(key)
            
            # Remove oldest if cache is full
            if len(cache) > max_size:
                oldest = access_order.pop(0)
                del cache[oldest]
                
            return result
            
        return wrapper
    return decorator


def optimize_file_operations():
    """
    Provide recommendations for file operation optimizations.
    
    Returns:
        List of optimization recommendations
    """
    recommendations = [
        "Use os.makedirs(exist_ok=True) instead of checking existence first",
        "Use shutil.copytree with ignore patterns for large directories",
        "Consider using pathlib.Path for cross-platform compatibility",
        "Cache file stat operations when checking multiple files",
        "Use context managers for file operations to ensure proper cleanup"
    ]
    return recommendations


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
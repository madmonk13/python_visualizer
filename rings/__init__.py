"""
Ring Shapes Package
Auto-discovers and loads all ring shape classes
"""

import os
import importlib
import inspect
from rings.base_ring import BaseRing


# Global registry of ring shapes
_ring_registry = {}
_display_name_to_internal = {}


def _discover_ring_shapes():
    """Auto-discover all ring shape classes in the rings directory"""
    global _ring_registry, _display_name_to_internal
    
    # Get the directory where this __init__.py file is located
    rings_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Scan all .py files in the rings directory
    for filename in os.listdir(rings_dir):
        if filename.endswith('.py') and filename not in ['__init__.py', 'base_ring.py']:
            module_name = filename[:-3]  # Remove .py extension
            
            try:
                # Import the module
                module = importlib.import_module(f'rings.{module_name}')
                
                # Find all classes in the module that inherit from BaseRing
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseRing) and obj != BaseRing:
                        # Instantiate the ring shape
                        ring_instance = obj()
                        internal_name = ring_instance.get_internal_name()
                        display_name = ring_instance.get_name()
                        
                        # Register it
                        _ring_registry[internal_name] = ring_instance
                        _display_name_to_internal[display_name] = internal_name
                        
            except Exception as e:
                print(f"Warning: Could not load ring shape from {filename}: {e}")


def get_all_ring_shapes():
    """
    Get all available ring shapes
    
    Returns:
    --------
    dict : {internal_name: ring_instance}
        Dictionary of all registered ring shapes
    """
    if not _ring_registry:
        _discover_ring_shapes()
    
    return _ring_registry


def get_ring_shape(internal_name):
    """
    Get a specific ring shape by its internal name
    
    Parameters:
    -----------
    internal_name : str
        The internal identifier for the ring shape
    
    Returns:
    --------
    BaseRing instance or None
        The ring shape instance, or None if not found
    """
    shapes = get_all_ring_shapes()
    return shapes.get(internal_name)


def get_ring_display_names():
    """
    Get all ring shape display names, alphabetically sorted
    
    Returns:
    --------
    list : [(display_name, internal_name), ...]
        List of tuples with display names and internal names, sorted alphabetically
    """
    shapes = get_all_ring_shapes()
    
    # Create list of (display_name, internal_name) tuples
    name_pairs = [(shape.get_name(), internal_name) 
                  for internal_name, shape in shapes.items()]
    
    # Sort alphabetically by display name
    name_pairs.sort(key=lambda x: x[0])
    
    return name_pairs


def get_shape_code_from_display_name(display_name):
    """
    Convert a display name to its internal shape code
    
    Parameters:
    -----------
    display_name : str
        The display name shown in the GUI (e.g., "4-Point Star")
    
    Returns:
    --------
    str : The internal shape code (e.g., "star4")
    """
    if not _display_name_to_internal:
        _discover_ring_shapes()
    
    # Direct lookup
    internal_name = _display_name_to_internal.get(display_name)
    
    if internal_name:
        return internal_name
    
    # If not found, return 'circle' as default
    print(f"Warning: Ring shape '{display_name}' not found, defaulting to 'circle'")
    print(f"Available shapes: {list(_display_name_to_internal.keys())}")
    return 'circle'


# Auto-discover on import
_discover_ring_shapes()
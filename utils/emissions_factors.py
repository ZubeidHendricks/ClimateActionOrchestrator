"""
Emissions Factors Utility for Climate Action Orchestrator

This module provides access to emissions factors used in carbon footprint calculations,
including factors for electricity, fuels, transportation, and other emission sources.
"""

import logging
import os
from typing import Dict, Any, Optional
import json
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

# Default emissions factors file path
DEFAULT_FACTORS_PATH = os.path.join(os.path.dirname(__file__), '../data/emissions_factors.json')

def get_emissions_factors(factors_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Get emissions factors for carbon calculations.
    
    Args:
        factors_path: Path to emissions factors file (optional)
    
    Returns:
        Dictionary of emissions factors
    """
    try:
        # Use provided path or default
        path = factors_path or DEFAULT_FACTORS_PATH
        
        # Check if custom emissions factors file exists
        if os.path.exists(path):
            with open(path, 'r') as f:
                factors = json.load(f)
            logger.info(f"Loaded emissions factors from {path}")
            return factors
        
        # If no file exists, return default factors
        logger.info("Using default emissions factors")
        return get_default_emissions_factors()
    
    except Exception as e:
        logger.error(f"Error loading emissions factors: {e}")
        logger.info("Falling back to default emissions factors")
        return get_default_emissions_factors()

def get_default_emissions_factors() -> Dict[str, Any]:
    """
    Get default emissions factors.
    
    Returns:
        Dictionary of default emissions factors
    """
    # These factors are based on standard sources like EPA, IEA, and DEFRA
    # In a real implementation, these would be more comprehensive and regularly updated
    return {
        # Electricity emissions factors by region (tCO2e/kWh)
        'electricity': {
            'US average': 0.000429,  # EPA eGRID 2019
            'WECC': 0.000350,        # Western US
            'ERCOT': 0.000400,       # Texas
            'SERC': 0.000420,        # Southeast US
            'RFC': 0.000450,         # Midwest US
            'NPCC': 0.000250,        # Northeast US
            'EU average': 0.000275,
            'UK': 0.000233,
            'China': 0.000623,
            'India': 0.000708,
            'Global average': 0.000475
        },
        
        # Natural gas (various units)
        'natural_gas': {
            'therms': 0.005302,  # tCO2e/therm (EPA)
            'mmbtu': 0.05310,    # tCO2e/mmbtu (EPA)
            'mcf': 0.05444,      # tCO2e/mcf (EPA)
            'kwh': 0.00018,      # tCO2e/kWh (EPA)
            'm3': 0.00195        # tCO2e/m3 (EPA)
        },
        
        # Mobile combustion (tCO2e per unit)
        'mobile': {
            'gasoline': {
                'gallons': 0.008887,  # tCO2e/gallon (EPA)
                'liters': 0.002348    # tCO2e/liter (EPA)
            },
            'diesel': {
                'gallons': 0.010180,  # tCO2e/gallon (EPA)
                'liters': 0.002689    # tCO2e/liter (EPA)
            },
            'jet_fuel': {
                'gallons': 0.009750,  # tCO2e/gallon (EPA)
                'liters': 0.002575    # tCO2e/liter (EPA)
            },
            'lpg': {
                'gallons': 0.005679,  # tCO2e/gallon (EPA)
                'liters': 0.001500    # tCO2e/liter (EPA)
            }
        },
        
        # Refrigerants (GWP - Global Warming Potential, 100-year)
        'refrigerants': {
            'R-410A': 2088,    # IPCC AR5
            'R-32': 675,       # IPCC AR5
            'R-134a': 1430,    # IPCC AR5
            'R-404A': 3922,    # IPCC AR5
            'R-407C': 1774,    # IPCC AR5
            'R-22': 1810,      # IPCC AR5
            'R-290': 3,        # Propane, IPCC AR5
            'R-600a': 3,       # Isobutane, IPCC AR5
            'R-744': 1         # CO2, IPCC AR5
        },
        
        # Waste disposal (tCO2e per ton)
        'waste': {
            'landfill': {
                'tons': 0.382,  # tCO2e/ton (EPA WARM model)
                'kg': 0.000382  # tCO2e/kg (EPA WARM model)
            },
            'recycling': {
                'tons': 0.042,  # tCO2e/ton (EPA WARM model)
                'kg': 0.000042  # tCO2e/kg (EPA WARM model)
            },
            'composting': {
                'tons': 0.018,  # tCO2e/ton (EPA WARM model)
                'kg': 0.000018  # tCO2e/kg (EPA WARM model)
            },
            'incineration': {
                'tons': 0.164,  # tCO2e/ton (EPA WARM model)
                'kg': 0.000164  # tCO2e/kg (EPA WARM model)
            }
        },
        
        # Air travel (tCO2e per passenger mile)
        'air_travel': {
            'economy_short_haul': 0.0002,      # tCO2e/mile (DEFRA)
            'economy_medium_haul': 0.00015,    # tCO2e/mile (DEFRA)
            'economy_long_haul': 0.00014,      # tCO2e/mile (DEFRA)
            'business_short_haul': 0.0003,     # tCO2e/mile (DEFRA)
            'business_medium_haul': 0.00022,   # tCO2e/mile (DEFRA)
            'business_long_haul': 0.00041,     # tCO2e/mile (DEFRA)
            'first_short_haul': 0.0004,        # tCO2e/mile (DEFRA)
            'first_medium_haul': 0.0003,       # tCO2e/mile (DEFRA)
            'first_long_haul': 0.00056         # tCO2e/mile (DEFRA)
        },
        
        # Ground travel (tCO2e per mile)
        'ground_travel': {
            'car': 0.000403,         # tCO2e/mile (EPA), average passenger car
            'taxi': 0.000242,        # tCO2e/mile (DEFRA)
            'bus': 0.000104,         # tCO2e/mile (DEFRA), per passenger
            'rail': 0.000041,        # tCO2e/mile (DEFRA), per passenger
            'subway': 0.000034,      # tCO2e/mile (DEFRA), per passenger
            'motorcycle': 0.000108,  # tCO2e/mile (DEFRA)
            'electric_vehicle': 0.000088  # tCO2e/mile (EPA), based on US average grid
        },
        
        # Hotel stays (tCO2e per room night)
        'hotel': {
            'USA': 0.0286,        # tCO2e/night (Cornell Hotel Sustainability Benchmarking)
            'UK': 0.0153,         # tCO2e/night (DEFRA)
            'EU average': 0.0182, # tCO2e/night (DEFRA/Green Tourism)
            'China': 0.0364,      # tCO2e/night (Cornell Hotel Sustainability Benchmarking)
            'Global average': 0.0252  # tCO2e/night (Cornell Hotel Sustainability Benchmarking)
        },
        
        # Spend-based factors for purchased goods (tCO2e per $)
        'spend': {
            'IT_equipment': 0.000465,     # tCO2e/$ (EEIO)
            'office_supplies': 0.000420,  # tCO2e/$ (EEIO)
            'furniture': 0.000480,        # tCO2e/$ (EEIO)
            'professional_services': 0.000170,  # tCO2e/$ (EEIO)
            'financial_services': 0.000075,     # tCO2e/$ (EEIO)
            'telecommunications': 0.000130,     # tCO2e/$ (EEIO)
            'food_catering': 0.000675,    # tCO2e/$ (EEIO)
            'hotels': 0.000280,           # tCO2e/$ (EEIO)
            'air_travel': 0.000900,       # tCO2e/$ (EEIO)
            'ground_transport': 0.000560  # tCO2e/$ (EEIO)
        },
        
        # Product-specific factors (tCO2e per unit)
        'products': {
            'paper': {
                'kg': 0.00175,     # tCO2e/kg (EPA)
                'ton': 1.75        # tCO2e/ton (EPA)
            },
            'plastic': {
                'kg': 0.00346,     # tCO2e/kg (EPA)
                'ton': 3.46        # tCO2e/ton (EPA)
            },
            'aluminum': {
                'kg': 0.00894,     # tCO2e/kg (EPA)
                'ton': 8.94        # tCO2e/ton (EPA)
            },
            'steel': {
                'kg': 0.00283,     # tCO2e/kg (EPA)
                'ton': 2.83        # tCO2e/ton (EPA)
            },
            'glass': {
                'kg': 0.00092,     # tCO2e/kg (EPA)
                'ton': 0.92        # tCO2e/ton (EPA)
            },
            'electronics': {
                'kg': 0.02500,     # tCO2e/kg (Apple/Dell sustainability reports, average)
                'unit': 0.14000    # tCO2e/unit (Apple/Dell sustainability reports, laptop average)
            }
        },
        
        # Water consumption (tCO2e per unit)
        'water': {
            'gallon': 0.0000035,   # tCO2e/gallon (Water Research Foundation)
            'liter': 0.0000009,    # tCO2e/liter (Water Research Foundation)
            'm3': 0.0009000,       # tCO2e/m3 (Water Research Foundation)
            'thousand_gallons': 0.0035000  # tCO2e/thousand gallons (Water Research Foundation)
        },
        
        # Purchased electricity conversion factors (for different units)
        'energy_conversion': {
            'kwh_to_mwh': 0.001,
            'mwh_to_kwh': 1000,
            'therm_to_kwh': 29.3001,
            'kwh_to_therm': 0.034129563,
            'mmbtu_to_kwh': 293.07107,
            'kwh_to_mmbtu': 0.003412142,
            'mwh_to_gj': 3.6,
            'gj_to_mwh': 0.27778
        },
        
        # Metadata about the factors
        'metadata': {
            'version': '1.2',
            'last_updated': '2023-12-15',
            'sources': [
                'EPA Emission Factors Hub (2023)',
                'IPCC AR5 (2014)',
                'DEFRA Conversion Factors (2023)',
                'IEA CO2 Emissions from Fuel Combustion (2022)',
                'EPA WARM Model Version 15',
                'Cornell Hotel Sustainability Benchmarking (2022)',
                'Water Research Foundation (2021)',
                'EEIO (Environmentally-Extended Input-Output) Model (2022)'
            ]
        }
    }

def get_emission_factor(category: str, subcategory: str = None, unit: str = None,
                      factors: Dict[str, Any] = None) -> float:
    """
    Get a specific emission factor.
    
    Args:
        category: Main category (e.g., 'electricity', 'natural_gas')
        subcategory: Optional subcategory (e.g., 'US average', 'gasoline')
        unit: Optional unit (e.g., 'kwh', 'gallons')
        factors: Optional custom factors dictionary
    
    Returns:
        Emission factor value (float)
    """
    try:
        # Get factors if not provided
        if factors is None:
            factors = get_emissions_factors()
        
        # Navigate to the right factor
        if category not in factors:
            logger.warning(f"Emission factor category not found: {category}")
            return 0.0
        
        category_factors = factors[category]
        
        # If no subcategory provided, check if this is a direct value
        if subcategory is None:
            if isinstance(category_factors, (int, float)):
                return float(category_factors)
            else:
                # Try to get a default or first value
                for key in ['default', 'average', 'US average', 'Global average']:
                    if key in category_factors:
                        return float(category_factors[key])
                
                # Fall back to first value if available
                if category_factors and isinstance(category_factors, dict):
                    first_key = next(iter(category_factors))
                    first_value = category_factors[first_key]
                    if isinstance(first_value, (int, float)):
                        return float(first_value)
                
                logger.warning(f"Could not find default value for category: {category}")
                return 0.0
        
        # With subcategory
        if subcategory not in category_factors:
            logger.warning(f"Emission factor subcategory not found: {category}.{subcategory}")
            return 0.0
        
        subcategory_factors = category_factors[subcategory]
        
        # If no unit provided or not a dict, return the value directly
        if unit is None or not isinstance(subcategory_factors, dict):
            if isinstance(subcategory_factors, (int, float)):
                return float(subcategory_factors)
            else:
                logger.warning(f"Invalid emission factor value type: {type(subcategory_factors)}")
                return 0.0
        
        # With unit
        if unit not in subcategory_factors:
            logger.warning(f"Emission factor unit not found: {category}.{subcategory}.{unit}")
            return 0.0
        
        return float(subcategory_factors[unit])
    
    except Exception as e:
        logger.error(f"Error getting emission factor: {e}")
        return 0.0

def update_emissions_factors(factors: Dict[str, Any], output_path: Optional[str] = None) -> bool:
    """
    Update emissions factors file.
    
    Args:
        factors: Updated emissions factors
        output_path: Path to save the updated factors (optional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Update metadata
        if 'metadata' not in factors:
            factors['metadata'] = {}
        
        factors['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        # Use provided path or default
        path = output_path or DEFAULT_FACTORS_PATH
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Write to file
        with open(path, 'w') as f:
            json.dump(factors, f, indent=4)
        
        logger.info(f"Updated emissions factors saved to {path}")
        return True
    
    except Exception as e:
        logger.error(f"Error updating emissions factors: {e}")
        return False

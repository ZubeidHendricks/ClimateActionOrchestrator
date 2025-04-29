"""
Simulation Models Utility for Climate Action Orchestrator

This module provides different modeling approaches for simulating
carbon emissions and business scenarios.
"""

import logging
from typing import Dict, Any, Callable
import numpy as np
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

def get_simulation_model(model_name: str, config: Dict[str, Any] = None) -> Callable:
    """
    Get a simulation model function based on the model name.
    
    Args:
        model_name: Name of the model to get
        config: Configuration parameters for the model
    
    Returns:
        Model function that can be called to run simulations
    """
    # Create a configuration dict if none provided
    if config is None:
        config = {}
    
    # Map model names to factory functions
    model_factories = {
        'linear': create_linear_model,
        'exponential': create_exponential_model,
        'logistic': create_logistic_model,
        'business_growth': create_business_growth_model,
        'carbon_intensity': create_carbon_intensity_model,
        'monte_carlo': create_monte_carlo_model
    }
    
    # Check if the requested model exists
    if model_name not in model_factories:
        logger.warning(f"Unknown model name: {model_name}, using linear as fallback")
        model_name = 'linear'
    
    # Create and return the model
    model_function = model_factories[model_name](config)
    logger.info(f"Created simulation model: {model_name}")
    
    return model_function

def create_linear_model(config: Dict[str, Any]) -> Callable:
    """
    Create a linear projection model.
    
    Args:
        config: Model configuration with parameters like slope and intercept
    
    Returns:
        Model function for linear projections
    """
    # Extract configuration
    slope = config.get('slope', 0.0)
    intercept = config.get('intercept', 0.0)
    
    def linear_model(x: float) -> float:
        """
        Apply a linear model: y = slope * x + intercept
        
        Args:
            x: Input value
        
        Returns:
            Projected value
        """
        return slope * x + intercept
    
    return linear_model

def create_exponential_model(config: Dict[str, Any]) -> Callable:
    """
    Create an exponential projection model.
    
    Args:
        config: Model configuration with parameters like rate
    
    Returns:
        Model function for exponential projections
    """
    # Extract configuration
    base_value = config.get('base_value', 1.0)
    rate = config.get('rate', 0.0)
    
    def exponential_model(x: float) -> float:
        """
        Apply an exponential model: y = base_value * (1 + rate)^x
        
        Args:
            x: Input value (usually time periods)
        
        Returns:
            Projected value
        """
        return base_value * ((1 + rate) ** x)
    
    return exponential_model

def create_logistic_model(config: Dict[str, Any]) -> Callable:
    """
    Create a logistic (S-curve) projection model.
    
    Args:
        config: Model configuration with parameters like L (curve maximum),
                k (steepness), and x0 (midpoint)
    
    Returns:
        Model function for logistic projections
    """
    # Extract configuration
    L = config.get('L', 1.0)  # Curve maximum
    k = config.get('k', 1.0)  # Steepness
    x0 = config.get('x0', 0.0)  # Midpoint
    
    def logistic_model(x: float) -> float:
        """
        Apply a logistic model: y = L / (1 + e^(-k * (x - x0)))
        
        Args:
            x: Input value (usually time periods)
        
        Returns:
            Projected value
        """
        return L / (1 + np.exp(-k * (x - x0)))
    
    return logistic_model

def create_business_growth_model(config: Dict[str, Any]) -> Callable:
    """
    Create a business growth model for simulating organization expansion.
    
    Args:
        config: Model configuration with parameters for growth trajectory
    
    Returns:
        Model function for business growth projections
    """
    # Extract configuration
    default_rate = config.get('default_rate', 0.03)  # 3% annual growth
    industry_rates = config.get('industry_rates', {
        'Technology': 0.08,
        'Manufacturing': 0.03,
        'Retail': 0.04,
        'Healthcare': 0.05,
        'Financial': 0.04
    })
    size_adjustments = config.get('size_adjustments', {
        'small': 0.02,    # < 100 employees
        'medium': 0.0,    # 100-1000 employees
        'large': -0.01    # > 1000 employees
    })
    
    def business_growth_model(years: int, industry: str = 'default', size: str = 'medium',
                             base_value: float = 1.0, custom_factors: Dict[str, float] = None) -> np.ndarray:
        """
        Project business growth over a period of years.
        
        Args:
            years: Number of years to project
            industry: Industry type for specific growth rates
            size: Organization size category
            base_value: Starting value
            custom_factors: Additional factors that modify growth
        
        Returns:
            Array of projected values for each year
        """
        # Get base growth rate from industry or default
        growth_rate = industry_rates.get(industry, default_rate)
        
        # Adjust for organization size
        growth_rate += size_adjustments.get(size, 0.0)
        
        # Apply custom factors if provided
        if custom_factors:
            for factor, value in custom_factors.items():
                growth_rate += value
        
        # Create year array (starting from year 0)
        year_array = np.arange(years + 1)
        
        # Calculate compound growth
        values = base_value * np.power(1 + growth_rate, year_array)
        
        return values
    
    return business_growth_model

def create_carbon_intensity_model(config: Dict[str, Any]) -> Callable:
    """
    Create a carbon intensity model for projecting emissions per unit of business activity.
    
    Args:
        config: Model configuration with parameters for carbon intensity trajectory
    
    Returns:
        Model function for carbon intensity projections
    """
    # Extract configuration
    default_rate = config.get('default_rate', -0.01)  # 1% annual efficiency improvement
    industry_rates = config.get('industry_rates', {
        'Technology': -0.02,
        'Manufacturing': -0.01,
        'Retail': -0.015,
        'Healthcare': -0.01,
        'Financial': -0.025
    })
    
    def carbon_intensity_model(years: int, industry: str = 'default', 
                              base_intensity: float = 1.0, 
                              initiatives: Dict[int, float] = None) -> np.ndarray:
        """
        Project carbon intensity over a period of years with potential initiatives.
        
        Args:
            years: Number of years to project
            industry: Industry type for specific rates
            base_intensity: Starting carbon intensity
            initiatives: Dict mapping year -> reduction factor for carbon initiatives
        
        Returns:
            Array of projected carbon intensity for each year
        """
        # Get base improvement rate from industry or default
        improvement_rate = industry_rates.get(industry, default_rate)
        
        # Create year array (starting from year 0)
        year_array = np.arange(years + 1)
        
        # Calculate baseline intensity improvement
        intensity = base_intensity * np.power(1 + improvement_rate, year_array)
        
        # Apply carbon initiatives if provided
        if initiatives:
            for year, reduction in initiatives.items():
                if year <= years:
                    # Apply one-time reduction in the specified year
                    intensity[year:] *= (1 - reduction)
        
        return intensity
    
    return carbon_intensity_model

def create_monte_carlo_model(config: Dict[str, Any]) -> Callable:
    """
    Create a Monte Carlo simulation model for risk analysis.
    
    Args:
        config: Model configuration with parameters for simulations
    
    Returns:
        Model function for Monte Carlo simulations
    """
    # Extract configuration
    num_simulations = config.get('num_simulations', 1000)
    confidence_interval = config.get('confidence_interval', 0.95)
    
    def monte_carlo_model(base_model: Callable, param_distributions: Dict[str, Any],
                         years: int = 10) -> Dict[str, Any]:
        """
        Run a Monte Carlo simulation over multiple parameter combinations.
        
        Args:
            base_model: Base model function to use in simulations
            param_distributions: Dictionary mapping parameters to their distributions
            years: Number of years to project
        
        Returns:
            Dictionary with simulation results including confidence intervals
        """
        # Initialize results array
        results = np.zeros((num_simulations, years + 1))
        
        # Run simulations
        for i in range(num_simulations):
            # Sample parameters from distributions
            params = {}
            for param_name, distribution in param_distributions.items():
                if distribution['type'] == 'normal':
                    params[param_name] = np.random.normal(
                        distribution['mean'], 
                        distribution['std']
                    )
                elif distribution['type'] == 'uniform':
                    params[param_name] = np.random.uniform(
                        distribution['min'], 
                        distribution['max']
                    )
                elif distribution['type'] == 'triangular':
                    params[param_name] = np.random.triangular(
                        distribution['min'], 
                        distribution['mode'], 
                        distribution['max']
                    )
                elif distribution['type'] == 'constant':
                    params[param_name] = distribution['value']
            
            # Run model with sampled parameters
            results[i, :] = base_model(years, **params)
        
        # Calculate statistics
        mean = np.mean(results, axis=0)
        median = np.median(results, axis=0)
        
        # Calculate confidence intervals
        alpha = (1 - confidence_interval) / 2
        lower_bound = np.percentile(results, alpha * 100, axis=0)
        upper_bound = np.percentile(results, (1 - alpha) * 100, axis=0)
        
        # Structure the results
        return {
            'mean': mean,
            'median': median,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'raw_simulations': results,
            'confidence_interval': confidence_interval,
            'num_simulations': num_simulations
        }
    
    return monte_carlo_model

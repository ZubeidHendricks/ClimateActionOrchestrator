"""
Carbon Calculation Agent for Climate Action Orchestrator

This agent processes operational data to calculate carbon footprint
using standards-based methodologies and emissions factors.
"""

import logging
from typing import Dict, List, Any
import pandas as pd
import numpy as np

# Import utility modules
from utils.azure_client import get_azure_client
from utils.emissions_factors import get_emissions_factors

logger = logging.getLogger(__name__)

class CarbonCalculationAgent:
    """Agent that calculates carbon footprint from operational data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the carbon calculation agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        self.config = config
        self.azure_client = get_azure_client(config.get("azure", {}))
        self.emissions_factors = get_emissions_factors()
        logger.info("Carbon Calculation Agent initialized")
    
    def calculate_emissions(self, operational_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate carbon emissions from operational data.
        
        Args:
            operational_data: Collected operational data for the organization
        
        Returns:
            Dictionary containing emissions calculations and breakdowns
        """
        logger.info("Calculating carbon emissions")
        
        # Calculate emissions for each scope and category
        scope1 = self._calculate_scope1(operational_data.get('scope1_data', {}))
        scope2 = self._calculate_scope2(operational_data.get('scope2_data', {}))
        scope3 = self._calculate_scope3(operational_data.get('scope3_data', {}))
        
        # Calculate total emissions
        total_emissions = sum([
            scope1.get('total', 0),
            scope2.get('total', 0),
            scope3.get('total', 0)
        ])
        
        # Calculate percentages for each scope
        if total_emissions > 0:
            scope1['percentage'] = (scope1.get('total', 0) / total_emissions) * 100
            scope2['percentage'] = (scope2.get('total', 0) / total_emissions) * 100
            scope3['percentage'] = (scope3.get('total', 0) / total_emissions) * 100
        
        # Prepare sources breakdown
        sources = {}
        
        # Add scope 1 categories
        for category, data in scope1.get('categories', {}).items():
            sources[category] = {
                'total': data.get('total', 0),
                'scope': 'scope1',
                'percentage': (data.get('total', 0) / total_emissions * 100) if total_emissions > 0 else 0
            }
        
        # Add scope 2 categories
        for category, data in scope2.get('categories', {}).items():
            sources[category] = {
                'total': data.get('total', 0),
                'scope': 'scope2',
                'percentage': (data.get('total', 0) / total_emissions * 100) if total_emissions > 0 else 0
            }
        
        # Add scope 3 categories
        for category, data in scope3.get('categories', {}).items():
            sources[category] = {
                'total': data.get('total', 0),
                'scope': 'scope3',
                'percentage': (data.get('total', 0) / total_emissions * 100) if total_emissions > 0 else 0
            }
        
        # Structure the response
        emissions_data = {
            'summary': {
                'total': total_emissions,
                'scope1': scope1.get('total', 0),
                'scope2': scope2.get('total', 0),
                'scope3': scope3.get('total', 0),
                'unit': 'tCO2e',
                'calculation_timestamp': pd.Timestamp.now().isoformat()
            },
            'scopes': {
                'scope1': scope1,
                'scope2': scope2,
                'scope3': scope3
            },
            'sources': sources,
            'methodology': {
                'standard': 'GHG Protocol',
                'emissions_factors': 'Various (EPA, IEA, DEFRA)',
                'assumptions': self._get_calculation_assumptions()
            }
        }
        
        logger.info(f"Completed emissions calculations: {total_emissions} tCO2e")
        return emissions_data
    
    def _calculate_scope1(self, scope1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Scope 1 (direct) emissions.
        
        Args:
            scope1_data: Operational data related to direct emissions
        
        Returns:
            Dictionary with Scope 1 emissions calculations
        """
        categories = {}
        total = 0
        
        # Stationary combustion (e.g., natural gas for heating)
        if 'stationary_combustion' in scope1_data:
            stationary = self._calculate_stationary_combustion(
                scope1_data['stationary_combustion']
            )
            categories['stationary_combustion'] = stationary
            total += stationary['total']
        
        # Mobile combustion (e.g., company vehicles)
        if 'mobile_combustion' in scope1_data:
            mobile = self._calculate_mobile_combustion(
                scope1_data['mobile_combustion']
            )
            categories['mobile_combustion'] = mobile
            total += mobile['total']
        
        # Fugitive emissions (e.g., refrigerant leaks)
        if 'fugitive_emissions' in scope1_data:
            fugitive = self._calculate_fugitive_emissions(
                scope1_data['fugitive_emissions']
            )
            categories['fugitive_emissions'] = fugitive
            total += fugitive['total']
        
        # Process emissions (e.g., manufacturing processes)
        if 'process_emissions' in scope1_data:
            process = self._calculate_process_emissions(
                scope1_data['process_emissions']
            )
            categories['process_emissions'] = process
            total += process['total']
        
        return {
            'total': total,
            'categories': categories
        }
    
    def _calculate_scope2(self, scope2_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Scope 2 (electricity) emissions.
        
        Args:
            scope2_data: Operational data related to purchased electricity
        
        Returns:
            Dictionary with Scope 2 emissions calculations
        """
        categories = {}
        total = 0
        
        # Electricity
        if 'electricity' in scope2_data:
            electricity = self._calculate_electricity_emissions(
                scope2_data['electricity']
            )
            categories['electricity'] = electricity
            total += electricity['total']
        
        # Steam
        if 'purchased_steam' in scope2_data:
            steam = self._calculate_steam_emissions(
                scope2_data['purchased_steam']
            )
            categories['purchased_steam'] = steam
            total += steam['total']
        
        # Heating/cooling
        if 'purchased_heating_cooling' in scope2_data:
            heating_cooling = self._calculate_heating_cooling_emissions(
                scope2_data['purchased_heating_cooling']
            )
            categories['purchased_heating_cooling'] = heating_cooling
            total += heating_cooling['total']
        
        return {
            'total': total,
            'categories': categories
        }
    
    def _calculate_scope3(self, scope3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Scope 3 (indirect) emissions.
        
        Args:
            scope3_data: Operational data related to value chain emissions
        
        Returns:
            Dictionary with Scope 3 emissions calculations
        """
        categories = {}
        total = 0
        
        # Purchased goods and services
        if 'purchased_goods' in scope3_data:
            purchased_goods = self._calculate_purchased_goods_emissions(
                scope3_data['purchased_goods']
            )
            categories['purchased_goods'] = purchased_goods
            total += purchased_goods['total']
        
        # Capital goods
        if 'capital_goods' in scope3_data:
            capital_goods = self._calculate_capital_goods_emissions(
                scope3_data['capital_goods']
            )
            categories['capital_goods'] = capital_goods
            total += capital_goods['total']
        
        # Fuel and energy-related activities
        if 'fuel_energy_related' in scope3_data:
            fuel_energy = self._calculate_fuel_energy_emissions(
                scope3_data['fuel_energy_related']
            )
            categories['fuel_energy_related'] = fuel_energy
            total += fuel_energy['total']
        
        # Upstream transportation
        if 'upstream_transportation' in scope3_data:
            upstream_transport = self._calculate_upstream_transportation_emissions(
                scope3_data['upstream_transportation']
            )
            categories['upstream_transportation'] = upstream_transport
            total += upstream_transport['total']
        
        # Waste
        if 'waste' in scope3_data:
            waste = self._calculate_waste_emissions(
                scope3_data['waste']
            )
            categories['waste'] = waste
            total += waste['total']
        
        # Business travel
        if 'business_travel' in scope3_data:
            business_travel = self._calculate_business_travel_emissions(
                scope3_data['business_travel']
            )
            categories['business_travel'] = business_travel
            total += business_travel['total']
        
        # Employee commuting
        if 'employee_commuting' in scope3_data:
            commuting = self._calculate_employee_commuting_emissions(
                scope3_data['employee_commuting']
            )
            categories['employee_commuting'] = commuting
            total += commuting['total']
        
        # Other categories would be included for a complete Scope 3 inventory
        
        return {
            'total': total,
            'categories': categories
        }
    
    def _calculate_stationary_combustion(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from stationary combustion (e.g., natural gas).
        
        Args:
            data: Consumption data for stationary combustion
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Example: Natural gas
        if 'natural_gas' in data:
            natural_gas = data['natural_gas']
            quantity = natural_gas.get('quantity', 0)
            unit = natural_gas.get('unit', 'therms')
            
            # Get appropriate emissions factor
            ef = self.emissions_factors.get('natural_gas', {}).get(unit, 0.005302)  # tCO2e/therm
            
            # Calculate emissions
            emissions = quantity * ef
            total += emissions
            
            details.append({
                'fuel_type': 'natural_gas',
                'quantity': quantity,
                'unit': unit,
                'emissions_factor': ef,
                'emissions': emissions
            })
        
        # Other fuels would be calculated similarly
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_mobile_combustion(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from mobile combustion (e.g., vehicle fleet).
        
        Args:
            data: Consumption data for mobile combustion
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Example: Vehicle fleet
        if 'vehicle_fleet' in data:
            for vehicle in data['vehicle_fleet']:
                fuel_type = vehicle.get('fuel_type', 'gasoline')
                quantity = vehicle.get('quantity', 0)
                unit = vehicle.get('unit', 'gallons')
                
                # Get appropriate emissions factor
                ef = self.emissions_factors.get('mobile', {}).get(fuel_type, {}).get(unit, 0.008887)  # tCO2e/gallon for gasoline
                
                # Calculate emissions
                emissions = quantity * ef
                total += emissions
                
                details.append({
                    'vehicle_type': vehicle.get('type', 'unknown'),
                    'fuel_type': fuel_type,
                    'quantity': quantity,
                    'unit': unit,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_fugitive_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from fugitive sources (e.g., refrigerant leaks).
        
        Args:
            data: Data on fugitive emissions
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Example: Refrigerants
        if 'refrigerants' in data:
            for refrigerant in data['refrigerants']:
                gas_type = refrigerant.get('type', 'R-410A')
                quantity = refrigerant.get('quantity', 0)
                unit = refrigerant.get('unit', 'kg')
                
                # Get appropriate GWP (Global Warming Potential)
                gwp = self.emissions_factors.get('refrigerants', {}).get(gas_type, 2088)  # GWP for R-410A
                
                # Calculate emissions (CO2 equivalent)
                emissions = quantity * gwp / 1000  # Convert to tCO2e
                total += emissions
                
                details.append({
                    'gas_type': gas_type,
                    'quantity': quantity,
                    'unit': unit,
                    'gwp': gwp,
                    'emissions': emissions
                })
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_process_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from industrial processes.
        
        Args:
            data: Data on process emissions
        
        Returns:
            Emissions calculation results
        """
        # This would be implemented for specific industrial processes
        # For this demo, we'll return a placeholder
        return {
            'total': 0,
            'details': []
        }
    
    def _calculate_electricity_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from electricity consumption.
        
        Args:
            data: Electricity consumption data
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Process each facility/location
        for location_name, location_data in data.items():
            quantity = location_data.get('quantity', 0)
            unit = location_data.get('unit', 'kWh')
            grid_region = location_data.get('grid_region', 'US average')
            
            # Get appropriate emissions factor based on grid region
            ef = self.emissions_factors.get('electricity', {}).get(grid_region, 0.000429)  # tCO2e/kWh US average
            
            # Calculate emissions
            emissions = quantity * ef
            total += emissions
            
            details.append({
                'location': location_name,
                'quantity': quantity,
                'unit': unit,
                'grid_region': grid_region,
                'emissions_factor': ef,
                'emissions': emissions
            })
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_steam_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from purchased steam."""
        # Implementation for steam emissions calculation
        return {
            'total': 0,
            'details': []
        }
    
    def _calculate_heating_cooling_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from purchased heating/cooling."""
        # Implementation for heating/cooling emissions calculation
        return {
            'total': 0,
            'details': []
        }
    
    def _calculate_purchased_goods_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from purchased goods and services.
        
        Args:
            data: Purchased goods data
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Calculate based on spend data (Economic Input-Output method)
        if 'spend_data' in data:
            for category, spend_info in data['spend_data'].items():
                amount = spend_info.get('amount', 0)
                currency = spend_info.get('currency', 'USD')
                
                # Get emissions factor for this spending category
                ef = self.emissions_factors.get('spend', {}).get(category, 0.0001)  # tCO2e/USD
                
                # Calculate emissions
                emissions = amount * ef
                total += emissions
                
                details.append({
                    'category': category,
                    'spend_amount': amount,
                    'currency': currency,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        # Calculate based on specific product data
        if 'product_data' in data:
            for product in data['product_data']:
                product_type = product.get('type', 'unknown')
                quantity = product.get('quantity', 0)
                unit = product.get('unit', 'kg')
                
                # Get appropriate emissions factor
                ef = self.emissions_factors.get('products', {}).get(product_type, {}).get(unit, 0)
                
                # Calculate emissions
                emissions = quantity * ef
                total += emissions
                
                details.append({
                    'product_type': product_type,
                    'quantity': quantity,
                    'unit': unit,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_capital_goods_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from capital goods."""
        # Implementation similar to purchased goods
        return {
            'total': 0,
            'details': []
        }
    
    def _calculate_fuel_energy_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from fuel and energy-related activities."""
        # Implementation for upstream fuel emissions
        return {
            'total': 0,
            'details': []
        }
    
    def _calculate_upstream_transportation_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from upstream transportation."""
        # Implementation for upstream transportation
        return {
            'total': 0,
            'details': []
        }
    
    def _calculate_waste_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from waste disposal.
        
        Args:
            data: Waste disposal data
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Process waste data
        if 'waste_streams' in data:
            for waste in data['waste_streams']:
                waste_type = waste.get('type', 'landfill')
                quantity = waste.get('quantity', 0)
                unit = waste.get('unit', 'tons')
                
                # Get appropriate emissions factor
                ef = self.emissions_factors.get('waste', {}).get(waste_type, {}).get(unit, 0.382)  # tCO2e/ton landfill waste
                
                # Calculate emissions
                emissions = quantity * ef
                total += emissions
                
                details.append({
                    'waste_type': waste_type,
                    'quantity': quantity,
                    'unit': unit,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_business_travel_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate emissions from business travel.
        
        Args:
            data: Business travel data
        
        Returns:
            Emissions calculation results
        """
        total = 0
        details = []
        
        # Air travel
        if 'air_travel' in data:
            for flight in data['air_travel']:
                distance = flight.get('distance', 0)
                distance_unit = flight.get('distance_unit', 'miles')
                flight_type = flight.get('type', 'economy')  # economy, business, first
                
                # Get appropriate emissions factor
                ef_key = f"{flight_type}_{self._categorize_flight_distance(distance)}"
                ef = self.emissions_factors.get('air_travel', {}).get(ef_key, 0.0002)  # tCO2e/mile economy short haul
                
                # Calculate emissions
                emissions = distance * ef
                total += emissions
                
                details.append({
                    'travel_mode': 'air',
                    'distance': distance,
                    'distance_unit': distance_unit,
                    'class': flight_type,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        # Ground travel
        if 'ground_travel' in data:
            for trip in data['ground_travel']:
                mode = trip.get('mode', 'car')
                distance = trip.get('distance', 0)
                distance_unit = trip.get('distance_unit', 'miles')
                
                # Get appropriate emissions factor
                ef = self.emissions_factors.get('ground_travel', {}).get(mode, 0.000403)  # tCO2e/mile car
                
                # Calculate emissions
                emissions = distance * ef
                total += emissions
                
                details.append({
                    'travel_mode': mode,
                    'distance': distance,
                    'distance_unit': distance_unit,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        # Hotel stays
        if 'hotel_stays' in data:
            for stay in data['hotel_stays']:
                nights = stay.get('nights', 0)
                country = stay.get('country', 'USA')
                
                # Get appropriate emissions factor
                ef = self.emissions_factors.get('hotel', {}).get(country, 0.0286)  # tCO2e/night USA
                
                # Calculate emissions
                emissions = nights * ef
                total += emissions
                
                details.append({
                    'stay_type': 'hotel',
                    'nights': nights,
                    'country': country,
                    'emissions_factor': ef,
                    'emissions': emissions
                })
        
        return {
            'total': total,
            'details': details
        }
    
    def _calculate_employee_commuting_emissions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from employee commuting."""
        # Implementation for employee commuting
        return {
            'total': 0,
            'details': []
        }
    
    def _categorize_flight_distance(self, distance: float) -> str:
        """
        Categorize flight distance as short, medium, or long haul.
        
        Args:
            distance: Flight distance
        
        Returns:
            Category of flight (short_haul, medium_haul, long_haul)
        """
        if distance < 300:
            return 'short_haul'
        elif distance < 2300:
            return 'medium_haul'
        else:
            return 'long_haul'
    
    def _get_calculation_assumptions(self) -> List[str]:
        """
        Get a list of assumptions made in emissions calculations.
        
        Returns:
            List of assumption descriptions
        """
        return [
            "Default emissions factors used where region-specific data is unavailable",
            "Economic Input-Output method used for purchased goods where product-specific data is unavailable",
            "Average occupancy assumed for business travel where specific data is unavailable",
            "Radiative forcing included in flight emissions calculations",
            "Grid average emissions factors used where specific utility emission factors are unavailable"
        ]

"""
Simulation Agent for Climate Action Orchestrator

This agent models different sustainability strategies to predict outcomes
and help organizations make data-driven decisions about emission reduction initiatives.
"""

import logging
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import utility modules
from utils.azure_client import get_azure_client
from utils.simulation_models import get_simulation_model

logger = logging.getLogger(__name__)

class SimulationAgent:
    """Agent that simulates sustainability scenarios and predicts outcomes."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the simulation agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        self.config = config
        self.azure_client = get_azure_client(config.get("azure", {}))
        self.models = {}
        
        # Initialize simulation models based on config
        if "models" in config:
            for model_name, model_config in config["models"].items():
                self.models[model_name] = get_simulation_model(
                    model_name, model_config
                )
        
        logger.info("Simulation Agent initialized")
    
    def simulate_scenarios(self, organization_data: Dict[str, Any], 
                         emissions_data: Dict[str, Any],
                         recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate different sustainability scenarios based on recommendations.
        
        Args:
            organization_data: Information about the organization
            emissions_data: Current carbon footprint data
            recommendations: Recommended sustainability initiatives
        
        Returns:
            Simulation results for different scenarios
        """
        logger.info(f"Simulating scenarios for {organization_data.get('name', 'unnamed organization')}")
        
        # Extract baseline emissions data
        baseline_emissions = emissions_data.get('summary', {}).get('total', 0)
        baseline_breakdown = emissions_data.get('sources', {})
        
        # Create business-as-usual (BAU) scenario
        bau_scenario = self._simulate_bau_scenario(
            organization_data, baseline_emissions, baseline_breakdown
        )
        
        # Create optimistic scenario (implement all recommendations)
        optimistic_scenario = self._simulate_optimistic_scenario(
            organization_data, baseline_emissions, baseline_breakdown, recommendations
        )
        
        # Create realistic scenario (implement high priority recommendations)
        realistic_scenario = self._simulate_realistic_scenario(
            organization_data, baseline_emissions, baseline_breakdown, recommendations
        )
        
        # Create minimal scenario (implement only quick wins)
        minimal_scenario = self._simulate_minimal_scenario(
            organization_data, baseline_emissions, baseline_breakdown, recommendations
        )
        
        # Calculate impact metrics
        impact_summary = self._calculate_impact_summary(
            bau_scenario, optimistic_scenario, realistic_scenario, minimal_scenario
        )
        
        # Structure the response
        simulation_results = {
            'scenarios': {
                'business_as_usual': bau_scenario,
                'optimistic': optimistic_scenario,
                'realistic': realistic_scenario,
                'minimal': minimal_scenario
            },
            'impact_summary': impact_summary,
            'meta': {
                'simulation_timestamp': pd.Timestamp.now().isoformat(),
                'simulation_period_years': 10,
                'confidence_level': 'medium'
            }
        }
        
        logger.info(f"Completed scenario simulations with {len(impact_summary)} impact metrics")
        return simulation_results
    
    def _simulate_bau_scenario(self, organization_data: Dict[str, Any],
                             baseline_emissions: float,
                             baseline_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate business-as-usual scenario (no new initiatives).
        
        Args:
            organization_data: Information about the organization
            baseline_emissions: Current total emissions
            baseline_breakdown: Current emissions breakdown by source
        
        Returns:
            Business-as-usual scenario projection
        """
        # Get growth factors based on industry and size
        industry = organization_data.get('industry', 'Technology')
        employees = organization_data.get('employees', 500)
        
        # Default annual growth rates by industry
        industry_growth_rates = {
            'Technology': 0.08,
            'Manufacturing': 0.03,
            'Retail': 0.04,
            'Healthcare': 0.05,
            'Financial': 0.04
        }
        
        # Get growth rate for this industry (default to 3% if unknown)
        annual_growth_rate = industry_growth_rates.get(industry, 0.03)
        
        # Adjust growth rate based on organization size
        if employees < 100:
            annual_growth_rate += 0.02  # Smaller companies tend to grow faster
        elif employees > 1000:
            annual_growth_rate -= 0.01  # Larger companies tend to grow slower
        
        # Project emissions for 10 years
        years = list(range(datetime.now().year, datetime.now().year + 11))
        projected_emissions = []
        
        # Assume efficiency improvements of 1% per year even in BAU
        efficiency_improvement = 0.01
        
        # Calculate projected emissions for each year
        current_emissions = baseline_emissions
        for year_idx, year in enumerate(years):
            if year_idx == 0:
                # First year is baseline
                projected_emissions.append({
                    'year': year,
                    'emissions': current_emissions,
                    'change_from_baseline': 0
                })
            else:
                # Project growth
                growth_factor = (1 + annual_growth_rate)
                # Apply efficiency improvement
                efficiency_factor = (1 - efficiency_improvement)
                # Calculate new emissions
                current_emissions = current_emissions * growth_factor * efficiency_factor
                
                projected_emissions.append({
                    'year': year,
                    'emissions': current_emissions,
                    'change_from_baseline': (current_emissions / baseline_emissions) - 1
                })
        
        # Create emissions breakdown projections
        breakdown_projections = {}
        for source, details in baseline_breakdown.items():
            if isinstance(details, dict) and 'total' in details:
                source_emissions = details['total']
                source_projections = []
                
                current_source_emissions = source_emissions
                for year_idx, year in enumerate(years):
                    if year_idx == 0:
                        # First year is baseline
                        source_projections.append({
                            'year': year,
                            'emissions': current_source_emissions
                        })
                    else:
                        # Project growth with source-specific factors
                        # This would be more sophisticated in a real implementation
                        growth_factor = (1 + annual_growth_rate)
                        efficiency_factor = (1 - efficiency_improvement)
                        current_source_emissions = current_source_emissions * growth_factor * efficiency_factor
                        
                        source_projections.append({
                            'year': year,
                            'emissions': current_source_emissions
                        })
                
                breakdown_projections[source] = source_projections
        
        # Calculate cumulative emissions
        cumulative_emissions = sum(year_data['emissions'] for year_data in projected_emissions)
        
        return {
            'name': 'Business as Usual',
            'description': 'Projection assuming no new sustainability initiatives beyond business as usual efficiency improvements.',
            'annual_projections': projected_emissions,
            'breakdown_projections': breakdown_projections,
            'cumulative_emissions': cumulative_emissions,
            'final_year_emissions': projected_emissions[-1]['emissions'],
            'final_year_change': projected_emissions[-1]['change_from_baseline'],
            'assumptions': [
                f"Annual growth rate: {annual_growth_rate:.1%}",
                f"Business-as-usual efficiency improvement: {efficiency_improvement:.1%} per year"
            ]
        }
    
    def _simulate_optimistic_scenario(self, organization_data: Dict[str, Any],
                                    baseline_emissions: float,
                                    baseline_breakdown: Dict[str, Any],
                                    recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate optimistic scenario (implement all recommendations).
        
        Args:
            organization_data: Information about the organization
            baseline_emissions: Current total emissions
            baseline_breakdown: Current emissions breakdown by source
            recommendations: Recommended sustainability initiatives
        
        Returns:
            Optimistic scenario projection
        """
        # Get all recommendations
        all_recommendations = []
        for rec_type in ['quick_wins', 'strategic_initiatives', 'industry_specific']:
            if rec_type in recommendations:
                all_recommendations.extend(recommendations[rec_type])
        
        # Start with BAU scenario as baseline
        bau_scenario = self._simulate_bau_scenario(
            organization_data, baseline_emissions, baseline_breakdown
        )
        
        # Get implementation timeline
        implementation_timeline = self._create_implementation_timeline(
            all_recommendations, aggressive=True
        )
        
        # Apply recommendations to BAU projections
        return self._apply_recommendations_to_scenario(
            bau_scenario, implementation_timeline, baseline_breakdown, 
            "Optimistic", 
            "Projection assuming implementation of all recommended initiatives with aggressive timeline."
        )
    
    def _simulate_realistic_scenario(self, organization_data: Dict[str, Any],
                                   baseline_emissions: float,
                                   baseline_breakdown: Dict[str, Any],
                                   recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate realistic scenario (implement high priority recommendations).
        
        Args:
            organization_data: Information about the organization
            baseline_emissions: Current total emissions
            baseline_breakdown: Current emissions breakdown by source
            recommendations: Recommended sustainability initiatives
        
        Returns:
            Realistic scenario projection
        """
        # Get prioritized recommendations
        prioritized_recs = recommendations.get('prioritized', [])
        
        # Select top ~60% of recommendations by priority score
        selected_recs = prioritized_recs[:int(len(prioritized_recs) * 0.6)]
        
        # Start with BAU scenario as baseline
        bau_scenario = self._simulate_bau_scenario(
            organization_data, baseline_emissions, baseline_breakdown
        )
        
        # Get implementation timeline
        implementation_timeline = self._create_implementation_timeline(
            selected_recs, aggressive=False
        )
        
        # Apply recommendations to BAU projections
        return self._apply_recommendations_to_scenario(
            bau_scenario, implementation_timeline, baseline_breakdown,
            "Realistic", 
            "Projection assuming implementation of high-priority initiatives with realistic timeline."
        )
    
    def _simulate_minimal_scenario(self, organization_data: Dict[str, Any],
                                 baseline_emissions: float,
                                 baseline_breakdown: Dict[str, Any],
                                 recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate minimal scenario (implement only quick wins).
        
        Args:
            organization_data: Information about the organization
            baseline_emissions: Current total emissions
            baseline_breakdown: Current emissions breakdown by source
            recommendations: Recommended sustainability initiatives
        
        Returns:
            Minimal scenario projection
        """
        # Get quick win recommendations
        quick_wins = recommendations.get('quick_wins', [])
        
        # Start with BAU scenario as baseline
        bau_scenario = self._simulate_bau_scenario(
            organization_data, baseline_emissions, baseline_breakdown
        )
        
        # Get implementation timeline
        implementation_timeline = self._create_implementation_timeline(
            quick_wins, aggressive=False
        )
        
        # Apply recommendations to BAU projections
        return self._apply_recommendations_to_scenario(
            bau_scenario, implementation_timeline, baseline_breakdown,
            "Minimal Effort", 
            "Projection assuming implementation of only quick win initiatives."
        )
    
    def _create_implementation_timeline(self, recommendations: List[Dict[str, Any]], 
                                      aggressive: bool = False) -> Dict[int, List[Dict[str, Any]]]:
        """
        Create timeline for implementing recommendations.
        
        Args:
            recommendations: List of recommendations to implement
            aggressive: Whether to use aggressive (faster) implementation timeline
        
        Returns:
            Dictionary mapping years to lists of recommendations implemented that year
        """
        implementation_timeline = {}
        current_year = datetime.now().year
        
        for rec in recommendations:
            # Determine implementation year based on effort level and aggressiveness
            effort_level = rec.get('effort_level', 'medium')
            
            if aggressive:
                # Aggressive timeline
                if effort_level == 'low':
                    impl_year = current_year  # Implement immediately
                elif effort_level == 'medium':
                    impl_year = current_year + 1  # Implement next year
                else:  # high
                    impl_year = current_year + 2  # Implement in 2 years
            else:
                # Conservative timeline
                if effort_level == 'low':
                    impl_year = current_year + 1  # Implement next year
                elif effort_level == 'medium':
                    impl_year = current_year + 2  # Implement in 2 years
                else:  # high
                    impl_year = current_year + 3  # Implement in 3 years
            
            # Add to timeline
            if impl_year not in implementation_timeline:
                implementation_timeline[impl_year] = []
            
            implementation_timeline[impl_year].append(rec)
        
        return implementation_timeline
    
    def _apply_recommendations_to_scenario(self, base_scenario: Dict[str, Any],
                                         implementation_timeline: Dict[int, List[Dict[str, Any]]],
                                         baseline_breakdown: Dict[str, Any],
                                         name: str,
                                         description: str) -> Dict[str, Any]:
        """
        Apply recommendations to modify a scenario.
        
        Args:
            base_scenario: Base scenario (usually BAU) to modify
            implementation_timeline: When recommendations will be implemented
            baseline_breakdown: Current emissions breakdown by source
            name: Name for the new scenario
            description: Description for the new scenario
        
        Returns:
            Modified scenario
        """
        # Create deep copy of base scenario projections
        annual_projections = [dict(proj) for proj in base_scenario['annual_projections']]
        breakdown_projections = {}
        for source, projections in base_scenario['breakdown_projections'].items():
            breakdown_projections[source] = [dict(proj) for proj in projections]
        
        # Track implemented recommendations
        implemented_recs = []
        
        # Apply recommendations according to timeline
        for year, recs in implementation_timeline.items():
            for rec in recs:
                # Find year index in projections
                year_idx = next((i for i, proj in enumerate(annual_projections) if proj['year'] == year), None)
                if year_idx is None:
                    continue  # Year not in projections
                
                # Get impact details
                absolute_reduction = rec.get('absolute_reduction', 0)
                emission_category = rec.get('emission_category', 'multiple')
                
                # Track implemented recommendation
                implemented_recs.append({
                    'title': rec.get('title', 'Unknown'),
                    'year_implemented': year,
                    'absolute_reduction': absolute_reduction
                })
                
                # Apply reduction to annual projections from this year forward
                for i in range(year_idx, len(annual_projections)):
                    # Reduce emissions proportionally (emissions may change year over year)
                    if i == year_idx:
                        # First year gets full reduction
                        reduction = absolute_reduction
                    else:
                        # Subsequent years' reduction scales with emissions growth
                        ratio = annual_projections[i]['emissions'] / annual_projections[year_idx]['emissions']
                        reduction = absolute_reduction * ratio
                    
                    # Apply reduction
                    annual_projections[i]['emissions'] -= reduction
                    
                    # Update change from baseline
                    baseline = annual_projections[0]['emissions']
                    annual_projections[i]['change_from_baseline'] = (annual_projections[i]['emissions'] / baseline) - 1
                
                # Apply reduction to breakdown projections if category-specific
                if emission_category != 'multiple' and emission_category in breakdown_projections:
                    for i in range(year_idx, len(breakdown_projections[emission_category])):
                        if i == year_idx:
                            # First year gets full reduction
                            breakdown_projections[emission_category][i]['emissions'] -= absolute_reduction
                        else:
                            # Subsequent years' reduction scales with emissions growth
                            ratio = breakdown_projections[emission_category][i]['emissions'] / breakdown_projections[emission_category][year_idx]['emissions']
                            breakdown_projections[emission_category][i]['emissions'] -= absolute_reduction * ratio
        
        # Calculate cumulative emissions
        cumulative_emissions = sum(year_data['emissions'] for year_data in annual_projections)
        
        # Create new scenario
        new_scenario = {
            'name': name,
            'description': description,
            'annual_projections': annual_projections,
            'breakdown_projections': breakdown_projections,
            'cumulative_emissions': cumulative_emissions,
            'final_year_emissions': annual_projections[-1]['emissions'],
            'final_year_change': annual_projections[-1]['change_from_baseline'],
            'implemented_recommendations': implemented_recs,
            'total_recommendations': len(implemented_recs),
            'assumptions': base_scenario['assumptions'] + [
                f"Implementation timeline: {'Aggressive' if any(year == datetime.now().year for year in implementation_timeline) else 'Conservative'}"
            ]
        }
        
        return new_scenario
    
    def _calculate_impact_summary(self, bau_scenario: Dict[str, Any],
                                optimistic_scenario: Dict[str, Any],
                                realistic_scenario: Dict[str, Any],
                                minimal_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate impact summary metrics across scenarios.
        
        Args:
            bau_scenario: Business-as-usual scenario
            optimistic_scenario: Optimistic scenario
            realistic_scenario: Realistic scenario
            minimal_scenario: Minimal effort scenario
        
        Returns:
            Impact summary metrics
        """
        # Get final year data
        final_year = bau_scenario['annual_projections'][-1]['year']
        bau_final = bau_scenario['final_year_emissions']
        optimistic_final = optimistic_scenario['final_year_emissions']
        realistic_final = realistic_scenario['final_year_emissions']
        minimal_final = minimal_scenario['final_year_emissions']
        
        # Get cumulative data
        bau_cumulative = bau_scenario['cumulative_emissions']
        optimistic_cumulative = optimistic_scenario['cumulative_emissions']
        realistic_cumulative = realistic_scenario['cumulative_emissions']
        minimal_cumulative = minimal_scenario['cumulative_emissions']
        
        # Calculate avoided emissions
        optimistic_avoided = bau_cumulative - optimistic_cumulative
        realistic_avoided = bau_cumulative - realistic_cumulative
        minimal_avoided = bau_cumulative - minimal_cumulative
        
        # Calculate final year reductions
        optimistic_reduction = 1 - (optimistic_final / bau_final)
        realistic_reduction = 1 - (realistic_final / bau_final)
        minimal_reduction = 1 - (minimal_final / bau_final)
        
        return {
            'final_year': final_year,
            'bau_final_emissions': bau_final,
            'optimistic_final_emissions': optimistic_final,
            'realistic_final_emissions': realistic_final,
            'minimal_final_emissions': minimal_final,
            
            'optimistic_final_reduction': optimistic_reduction,
            'realistic_final_reduction': realistic_reduction,
            'minimal_final_reduction': minimal_reduction,
            
            'bau_cumulative_emissions': bau_cumulative,
            'optimistic_cumulative_emissions': optimistic_cumulative,
            'realistic_cumulative_emissions': realistic_cumulative,
            'minimal_cumulative_emissions': minimal_cumulative,
            
            'optimistic_avoided_emissions': optimistic_avoided,
            'realistic_avoided_emissions': realistic_avoided,
            'minimal_avoided_emissions': minimal_avoided,
            
            'recommended_scenario': 'realistic',  # Default recommendation
            'key_insights': [
                f"The realistic scenario could reduce emissions by {realistic_reduction:.1%} by {final_year} compared to business as usual.",
                f"Implementing all recommendations could reduce emissions by {optimistic_reduction:.1%} by {final_year}.",
                f"Even minimal effort initiatives could reduce emissions by {minimal_reduction:.1%} by {final_year}.",
                f"The realistic scenario would avoid approximately {realistic_avoided:.1f} tCO2e over the next 10 years."
            ]
        }

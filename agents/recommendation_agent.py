"""
Recommendation Agent for Climate Action Orchestrator

This agent analyzes emissions data and organization characteristics
to generate prioritized sustainability recommendations.
"""

import logging
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Import utility modules
from utils.azure_client import get_azure_client
from utils.recommendation_templates import get_recommendation_templates

logger = logging.getLogger(__name__)

class RecommendationAgent:
    """Agent that generates sustainability recommendations based on emissions data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the recommendation agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        self.config = config
        self.azure_client = get_azure_client(config.get("azure", {}))
        self.recommendation_templates = get_recommendation_templates()
        self.industry_benchmarks = self._load_industry_benchmarks()
        logger.info("Recommendation Agent initialized")
    
    def _load_industry_benchmarks(self) -> Dict[str, Any]:
        """
        Load industry benchmarking data for comparative analysis.
        
        Returns:
            Dictionary of industry benchmarks
        """
        try:
            # In a real implementation, this would load from a database or API
            # For demo purposes, we'll return sample data
            return {
                "Technology": {
                    "average_emissions_per_employee": 3.5,
                    "best_in_class_emissions_per_employee": 1.8,
                    "common_initiatives": ["renewable_energy", "remote_work", "e_waste_management"]
                },
                "Manufacturing": {
                    "average_emissions_per_employee": 12.7,
                    "best_in_class_emissions_per_employee": 7.3,
                    "common_initiatives": ["process_efficiency", "material_substitution", "heat_recovery"]
                },
                "Retail": {
                    "average_emissions_per_employee": 5.2,
                    "best_in_class_emissions_per_employee": 3.0,
                    "common_initiatives": ["logistics_optimization", "refrigerant_management", "packaging_reduction"]
                }
                # Additional industries would be included here
            }
        except Exception as e:
            logger.error(f"Error loading industry benchmarks: {e}")
            return {}
    
    def generate_recommendations(self, organization_data: Dict[str, Any], 
                               emissions_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sustainability recommendations based on emissions data.
        
        Args:
            organization_data: Information about the organization
            emissions_data: Carbon footprint data for the organization
        
        Returns:
            Dictionary containing various recommendation categories and priorities
        """
        logger.info(f"Generating recommendations for {organization_data.get('name', 'unnamed organization')}")
        
        # Extract key information
        industry = organization_data.get('industry', 'Unknown')
        total_emissions = emissions_data.get('summary', {}).get('total', 0)
        emission_sources = emissions_data.get('sources', {})
        
        # Get industry benchmarks
        benchmarks = self.industry_benchmarks.get(industry, {})
        
        # Identify hotspots in emissions
        hotspots = self._identify_emission_hotspots(emission_sources)
        
        # Generate quick wins (low effort, medium impact)
        quick_wins = self._generate_quick_wins(hotspots, organization_data)
        
        # Generate strategic initiatives (higher effort, high impact)
        strategic_initiatives = self._generate_strategic_initiatives(emission_sources, benchmarks)
        
        # Generate industry-specific recommendations
        industry_specific = self._generate_industry_specific(industry, total_emissions)
        
        # Combine and prioritize recommendations
        all_recommendations = quick_wins + strategic_initiatives + industry_specific
        prioritized = self._prioritize_recommendations(all_recommendations, organization_data)
        
        # Structure the response
        recommendations = {
            "quick_wins": quick_wins,
            "strategic_initiatives": strategic_initiatives,
            "industry_specific": industry_specific,
            "prioritized": prioritized,
            "meta": {
                "total_recommendations": len(all_recommendations),
                "estimated_total_impact": self._estimate_total_impact(prioritized),
                "generation_timestamp": pd.Timestamp.now().isoformat()
            }
        }
        
        logger.info(f"Generated {len(all_recommendations)} recommendations")
        return recommendations
    
    def _identify_emission_hotspots(self, emission_sources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify the biggest contributors to emissions.
        
        Args:
            emission_sources: Breakdown of emissions by source
        
        Returns:
            List of emission hotspots with source and magnitude
        """
        # Convert to a list of sources with their emissions
        sources = []
        for category, details in emission_sources.items():
            if isinstance(details, dict) and 'total' in details:
                sources.append({
                    'category': category,
                    'emissions': details['total'],
                    'percentage': details.get('percentage', 0)
                })
            elif isinstance(details, (int, float)):
                sources.append({
                    'category': category,
                    'emissions': details,
                    'percentage': 0  # We would calculate this in a real implementation
                })
        
        # Sort by emissions (descending)
        sources.sort(key=lambda x: x['emissions'], reverse=True)
        
        # Return top sources (hotspots)
        return sources[:5]  # Top 5 emission sources
    
    def _generate_quick_wins(self, hotspots: List[Dict[str, Any]], 
                           organization_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate quick win recommendations based on emission hotspots.
        
        Args:
            hotspots: Biggest emission sources
            organization_data: Information about the organization
        
        Returns:
            List of quick win recommendations
        """
        quick_wins = []
        
        # Map emission categories to potential quick win recommendations
        category_to_recommendations = {
            'electricity': [
                {
                    'title': 'LED Lighting Upgrade',
                    'description': 'Replace conventional lighting with LED alternatives to reduce electricity consumption by up to 75%.',
                    'estimated_reduction': 0.05,  # 5% of electricity emissions
                    'implementation_cost': 'medium',
                    'effort_level': 'low',
                    'payback_period': '1-2 years'
                },
                {
                    'title': 'Smart Building Controls',
                    'description': 'Implement occupancy sensors and smart thermostats to optimize HVAC and lighting usage.',
                    'estimated_reduction': 0.08,  # 8% of electricity emissions
                    'implementation_cost': 'medium',
                    'effort_level': 'medium',
                    'payback_period': '2-3 years'
                }
            ],
            'transportation': [
                {
                    'title': 'Remote Work Policy',
                    'description': 'Implement or expand remote work options to reduce commuting emissions.',
                    'estimated_reduction': 0.15,  # 15% of transportation emissions
                    'implementation_cost': 'low',
                    'effort_level': 'medium',
                    'payback_period': 'immediate'
                },
                {
                    'title': 'Fleet Route Optimization',
                    'description': 'Optimize delivery routes and schedules to minimize fuel consumption.',
                    'estimated_reduction': 0.12,  # 12% of transportation emissions
                    'implementation_cost': 'low',
                    'effort_level': 'medium',
                    'payback_period': '<1 year'
                }
            ],
            # Other categories would be included here
        }
        
        # Generate recommendations based on hotspots
        for hotspot in hotspots:
            category = hotspot['category']
            if category in category_to_recommendations:
                # Add relevant recommendations for this category
                for recommendation in category_to_recommendations[category]:
                    # Calculate actual impact based on hotspot emissions
                    impact = hotspot['emissions'] * recommendation['estimated_reduction']
                    
                    # Add to quick wins list with the calculated impact
                    quick_wins.append({
                        **recommendation,
                        'emission_category': category,
                        'absolute_reduction': impact,
                        'recommendation_type': 'quick_win'
                    })
        
        return quick_wins
    
    def _generate_strategic_initiatives(self, emission_sources: Dict[str, Any], 
                                     benchmarks: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategic (longer-term) sustainability initiatives.
        
        Args:
            emission_sources: Breakdown of emissions by source
            benchmarks: Industry benchmarking data
        
        Returns:
            List of strategic initiative recommendations
        """
        # This would contain more complex logic in a real implementation
        # For this demo, we'll return some sample strategic initiatives
        strategic_initiatives = [
            {
                'title': 'Renewable Energy Procurement',
                'description': 'Enter into power purchase agreements (PPAs) for renewable energy to reduce Scope 2 emissions.',
                'estimated_reduction': 0.8 * emission_sources.get('electricity', {}).get('total', 0),
                'emission_category': 'electricity',
                'implementation_cost': 'high',
                'effort_level': 'high',
                'payback_period': '5-10 years',
                'recommendation_type': 'strategic'
            },
            {
                'title': 'Supply Chain Engagement Program',
                'description': 'Work with top suppliers to measure and reduce their emissions, impacting your Scope 3 footprint.',
                'estimated_reduction': 0.2 * emission_sources.get('purchased_goods', {}).get('total', 0),
                'emission_category': 'purchased_goods',
                'implementation_cost': 'medium',
                'effort_level': 'high',
                'payback_period': '3-5 years',
                'recommendation_type': 'strategic'
            }
        ]
        
        # Add benchmark-based recommendation if available
        if benchmarks and 'best_in_class_emissions_per_employee' in benchmarks:
            strategic_initiatives.append({
                'title': 'Best Practices Implementation Program',
                'description': f"Implement comprehensive sustainability program based on industry best practices to achieve best-in-class performance of {benchmarks['best_in_class_emissions_per_employee']} tCO2e per employee.",
                'estimated_reduction': 0.3 * sum(src.get('total', 0) for src in emission_sources.values() if isinstance(src, dict)),
                'emission_category': 'multiple',
                'implementation_cost': 'high',
                'effort_level': 'high',
                'payback_period': '3-7 years',
                'recommendation_type': 'strategic'
            })
        
        return strategic_initiatives
    
    def _generate_industry_specific(self, industry: str, 
                                  total_emissions: float) -> List[Dict[str, Any]]:
        """
        Generate industry-specific recommendations.
        
        Args:
            industry: Organization's industry
            total_emissions: Total carbon footprint
        
        Returns:
            List of industry-specific recommendations
        """
        industry_recommendations = {
            'Technology': [
                {
                    'title': 'Green Data Center Practices',
                    'description': 'Implement energy efficiency best practices for data centers, including optimized cooling, server virtualization, and power management.',
                    'estimated_reduction': 0.15 * total_emissions,
                    'implementation_cost': 'medium',
                    'effort_level': 'medium',
                    'payback_period': '2-4 years',
                    'recommendation_type': 'industry'
                }
            ],
            'Manufacturing': [
                {
                    'title': 'Process Heat Electrification',
                    'description': 'Convert fossil fuel-based process heating to electric alternatives powered by renewable energy.',
                    'estimated_reduction': 0.25 * total_emissions,
                    'implementation_cost': 'high',
                    'effort_level': 'high',
                    'payback_period': '5-8 years',
                    'recommendation_type': 'industry'
                }
            ],
            'Retail': [
                {
                    'title': 'Refrigeration System Upgrade',
                    'description': 'Replace HFC refrigerants with low-GWP alternatives and improve system efficiency.',
                    'estimated_reduction': 0.18 * total_emissions,
                    'implementation_cost': 'high',
                    'effort_level': 'medium',
                    'payback_period': '3-6 years',
                    'recommendation_type': 'industry'
                }
            ]
            # Other industries would be included here
        }
        
        return industry_recommendations.get(industry, [])
    
    def _prioritize_recommendations(self, recommendations: List[Dict[str, Any]], 
                                 organization_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prioritize recommendations based on impact, cost, and effort.
        
        Args:
            recommendations: List of all recommendations
            organization_data: Information about the organization
        
        Returns:
            Prioritized list of recommendations
        """
        # Calculate a priority score for each recommendation
        for recommendation in recommendations:
            # Convert categorical values to numerical scores
            cost_score = {'low': 3, 'medium': 2, 'high': 1}.get(recommendation.get('implementation_cost', 'medium'), 2)
            effort_score = {'low': 3, 'medium': 2, 'high': 1}.get(recommendation.get('effort_level', 'medium'), 2)
            
            # Impact score based on absolute reduction
            impact = recommendation.get('absolute_reduction', 0)
            impact_score = 1
            if impact > 10:  # Significant impact
                impact_score = 3
            elif impact > 5:  # Moderate impact
                impact_score = 2
            
            # Calculate overall priority score (higher is better)
            recommendation['priority_score'] = impact_score * 0.6 + cost_score * 0.2 + effort_score * 0.2
        
        # Sort by priority score (descending)
        prioritized = sorted(recommendations, key=lambda x: x.get('priority_score', 0), reverse=True)
        
        return prioritized
    
    def _estimate_total_impact(self, recommendations: List[Dict[str, Any]]) -> float:
        """
        Estimate the total potential impact of all recommendations.
        
        Args:
            recommendations: List of recommendations
        
        Returns:
            Total potential emissions reduction in tCO2e
        """
        # Sum up the absolute reduction from all recommendations
        # In a real implementation, we would account for overlapping effects
        return sum(rec.get('absolute_reduction', 0) for rec in recommendations)
    
    def refine_recommendations(self, existing_recommendations: Dict[str, Any], 
                             feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refine recommendations based on human feedback.
        
        Args:
            existing_recommendations: Previously generated recommendations
            feedback: Feedback from human experts
        
        Returns:
            Updated recommendations
        """
        logger.info("Refining recommendations based on human feedback")
        
        # Start with the existing recommendations
        refined = dict(existing_recommendations)
        
        # Extract the prioritized list
        prioritized = refined.get('prioritized', [])
        
        # Process rejections (remove rejected recommendations)
        rejected_ids = feedback.get('rejected', [])
        if rejected_ids:
            prioritized = [rec for rec in prioritized 
                          if rec.get('id', '') not in rejected_ids]
        
        # Process modifications (update recommendations)
        modifications = feedback.get('modifications', {})
        for rec_id, changes in modifications.items():
            for rec in prioritized:
                if rec.get('id', '') == rec_id:
                    # Update the recommendation with the changes
                    rec.update(changes)
                    break
        
        # Process new constraints
        constraints = feedback.get('constraints', {})
        if constraints:
            # Apply filters based on constraints
            # This would be more sophisticated in a real implementation
            if 'max_cost' in constraints:
                cost_map = {'low': 1, 'medium': 2, 'high': 3}
                prioritized = [rec for rec in prioritized 
                              if cost_map.get(rec.get('implementation_cost', 'medium'), 2) 
                              <= cost_map.get(constraints['max_cost'], 3)]
            
            if 'max_effort' in constraints:
                effort_map = {'low': 1, 'medium': 2, 'high': 3}
                prioritized = [rec for rec in prioritized 
                              if effort_map.get(rec.get('effort_level', 'medium'), 2) 
                              <= effort_map.get(constraints['max_effort'], 3)]
            
            if 'focus_categories' in constraints:
                prioritized = [rec for rec in prioritized 
                              if rec.get('emission_category', '') 
                              in constraints['focus_categories']]
        
        # Update meta information
        refined['meta'] = {
            **refined.get('meta', {}),
            'total_recommendations': len(prioritized),
            'estimated_total_impact': self._estimate_total_impact(prioritized),
            'refinement_timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Update the prioritized list
        refined['prioritized'] = prioritized
        
        logger.info(f"Refined to {len(prioritized)} recommendations based on feedback")
        return refined

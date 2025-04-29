"""
Reporting Agent for Climate Action Orchestrator

This agent generates standardized reports for various stakeholders
and regulatory frameworks based on the emissions analysis.
"""

import logging
from typing import Dict, List, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Import utility modules
from utils.azure_client import get_azure_client

logger = logging.getLogger(__name__)

class ReportingAgent:
    """Agent that generates standardized sustainability reports."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the reporting agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        self.config = config
        self.azure_client = get_azure_client(config.get("azure", {}))
        self.report_templates = self._load_report_templates()
        self.output_dir = config.get("output_dir", "reports")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info("Reporting Agent initialized")
    
    def generate_reports(self, 
                         organization_data: Dict[str, Any], 
                         emissions_data: Dict[str, Any],
                         recommendations: Dict[str, Any], 
                         simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate standardized reports based on emissions data and recommendations.
        
        Args:
            organization_data: Data about the organization
            emissions_data: Carbon footprint calculations
            recommendations: Recommended actions for reducing emissions
            simulation_results: Results of simulating different scenarios
        
        Returns:
            Dictionary containing report metadata and access URLs
        """
        logger.info("Generating sustainability reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        org_name = organization_data.get("name", "Organization").replace(" ", "_").lower()
        
        reports = {}
        report_urls = {}
        
        # Generate GHG Protocol report
        ghg_report = self._generate_ghg_protocol_report(
            organization_data, emissions_data, timestamp, org_name
        )
        reports["ghg_protocol"] = ghg_report
        report_urls["ghg_protocol"] = ghg_report.get("url")
        
        # Generate TCFD report
        tcfd_report = self._generate_tcfd_report(
            organization_data, emissions_data, recommendations, 
            simulation_results, timestamp, org_name
        )
        reports["tcfd"] = tcfd_report
        report_urls["tcfd"] = tcfd_report.get("url")
        
        # Generate CDP report
        cdp_report = self._generate_cdp_report(
            organization_data, emissions_data, recommendations,
            timestamp, org_name
        )
        reports["cdp"] = cdp_report
        report_urls["cdp"] = cdp_report.get("url")
        
        # Generate executive summary
        exec_summary = self._generate_executive_summary(
            organization_data, emissions_data, recommendations,
            simulation_results, timestamp, org_name
        )
        reports["executive_summary"] = exec_summary
        report_urls["executive_summary"] = exec_summary.get("url")
        
        # Generate technical appendix with data sources and methodologies
        technical_appendix = self._generate_technical_appendix(
            emissions_data, timestamp, org_name
        )
        reports["technical_appendix"] = technical_appendix
        report_urls["technical_appendix"] = technical_appendix.get("url")
        
        result = {
            "report_metadata": {
                "timestamp": timestamp,
                "organization": organization_data.get("name"),
                "report_count": len(reports)
            },
            "report_urls": report_urls,
            "reports": reports
        }
        
        logger.info(f"Generated {len(reports)} sustainability reports")
        return result
    
    def _load_report_templates(self) -> Dict[str, Any]:
        """
        Load report templates from storage.
        
        Returns:
            Dictionary of report templates
        """
        # In a real implementation, this would load templates from Azure storage
        # For this demo, we'll return placeholder templates
        return {
            "ghg_protocol": {
                "sections": [
                    "organizational_information",
                    "inventory_boundaries",
                    "emissions_summary",
                    "emissions_detail",
                    "methodologies",
                    "verification_statement"
                ]
            },
            "tcfd": {
                "sections": [
                    "governance",
                    "strategy",
                    "risk_management",
                    "metrics_and_targets"
                ]
            },
            "cdp": {
                "sections": [
                    "governance",
                    "risks_and_opportunities",
                    "business_strategy",
                    "targets_and_performance",
                    "emissions_methodology",
                    "emissions_data",
                    "energy",
                    "verification",
                    "carbon_pricing",
                    "engagement"
                ]
            },
            "executive_summary": {
                "sections": [
                    "key_findings",
                    "emissions_overview",
                    "top_recommendations",
                    "potential_impact",
                    "next_steps"
                ]
            }
        }
    
    def _generate_charts(self, emissions_data: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """
        Generate data visualization charts for reports.
        
        Args:
            emissions_data: Carbon footprint data
            output_dir: Directory to save charts
            
        Returns:
            Dictionary of chart file paths
        """
        charts = {}
        
        # Create emissions by scope pie chart
        scope_data = {
            'Scope 1': emissions_data['summary']['scope1'],
            'Scope 2': emissions_data['summary']['scope2'],
            'Scope 3': emissions_data['summary']['scope3']
        }
        
        plt.figure(figsize=(10, 6))
        plt.pie(
            scope_data.values(), 
            labels=scope_data.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=['#ff9999','#66b3ff','#99ff99']
        )
        plt.title('Emissions by Scope')
        scope_chart_path = f"{output_dir}/emissions_by_scope.png"
        plt.savefig(scope_chart_path)
        plt.close()
        charts['emissions_by_scope'] = scope_chart_path
        
        # Create emissions by source bar chart
        sources = emissions_data.get('sources', {})
        source_names = []
        source_values = []
        for source, data in sources.items():
            if data.get('total', 0) > 0:
                source_names.append(source.replace('_', ' ').title())
                source_values.append(data.get('total', 0))
        
        # Sort by emission value (descending)
        sorted_indices = sorted(range(len(source_values)), key=lambda k: source_values[k], reverse=True)
        sorted_names = [source_names[i] for i in sorted_indices]
        sorted_values = [source_values[i] for i in sorted_indices]
        
        # Limit to top 10 sources
        if len(sorted_names) > 10:
            sorted_names = sorted_names[:10]
            sorted_values = sorted_values[:10]
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x=sorted_values, y=sorted_names)
        plt.title('Top Emission Sources')
        plt.xlabel('Emissions (tCO2e)')
        plt.tight_layout()
        sources_chart_path = f"{output_dir}/emissions_by_source.png"
        plt.savefig(sources_chart_path)
        plt.close()
        charts['emissions_by_source'] = sources_chart_path
        
        return charts
    
    def _generate_ghg_protocol_report(self, 
                                     organization_data: Dict[str, Any],
                                     emissions_data: Dict[str, Any],
                                     timestamp: str,
                                     org_name: str) -> Dict[str, Any]:
        """
        Generate a report following the GHG Protocol standard.
        
        Args:
            organization_data: Data about the organization
            emissions_data: Carbon footprint calculations
            timestamp: Timestamp for the report
            org_name: Organization name (formatted)
            
        Returns:
            Report metadata including URL
        """
        report_dir = f"{self.output_dir}/{org_name}/ghg_protocol_{timestamp}"
        os.makedirs(report_dir, exist_ok=True)
        
        # Generate charts
        charts = self._generate_charts(emissions_data, report_dir)
        
        # In a real implementation, this would generate a formatted report document
        # For this demo, we'll create a simple JSON file with report data
        
        report_data = {
            "report_type": "GHG Protocol",
            "organization": organization_data.get("name"),
            "reporting_period": "January 2024 - December 2024",  # Example period
            "emissions_summary": emissions_data.get("summary", {}),
            "scopes": emissions_data.get("scopes", {}),
            "methodology": emissions_data.get("methodology", {}),
            "charts": charts
        }
        
        # Write report data to file
        report_file = f"{report_dir}/ghg_protocol_report.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(report_data, f, indent=2)
        
        # In a real implementation, this would be a URL to access the report
        report_url = f"file://{report_file}"
        
        return {
            "title": "GHG Protocol Emissions Inventory",
            "timestamp": timestamp,
            "file_path": report_file,
            "url": report_url,
            "standard": "GHG Protocol Corporate Standard"
        }
    
    def _generate_tcfd_report(self,
                             organization_data: Dict[str, Any],
                             emissions_data: Dict[str, Any],
                             recommendations: Dict[str, Any],
                             simulation_results: Dict[str, Any],
                             timestamp: str,
                             org_name: str) -> Dict[str, Any]:
        """
        Generate a report following the TCFD recommendations.
        
        Args:
            organization_data: Data about the organization
            emissions_data: Carbon footprint calculations
            recommendations: Recommended actions for reducing emissions
            simulation_results: Results of simulating different scenarios
            timestamp: Timestamp for the report
            org_name: Organization name (formatted)
            
        Returns:
            Report metadata including URL
        """
        report_dir = f"{self.output_dir}/{org_name}/tcfd_{timestamp}"
        os.makedirs(report_dir, exist_ok=True)
        
        # In a real implementation, this would generate a comprehensive TCFD report
        # For this demo, we'll create a simple JSON file with report data
        
        report_data = {
            "report_type": "TCFD",
            "organization": organization_data.get("name"),
            "governance": {
                "board_oversight": "Board receives quarterly updates on climate risks and strategy",
                "management_role": "Sustainability team reports to CFO, Climate Committee meets monthly"
            },
            "strategy": {
                "climate_risks": [
                    "Physical risks to facilities in coastal regions",
                    "Transition risks from carbon pricing mechanisms",
                    "Market shifts toward low-carbon alternatives"
                ],
                "climate_opportunities": [
                    "Development of low-carbon products and services",
                    "Energy efficiency improvements",
                    "Renewable energy adoption"
                ],
                "business_impacts": "Based on simulation results, climate risks could impact profitability by 2-5% by 2030 if unaddressed"
            },
            "risk_management": {
                "identification_process": "Annual climate risk assessment integrated with enterprise risk management",
                "management_process": "Climate risks incorporated into strategic planning and capital allocation",
                "integration": "Climate risk assessment informs business continuity planning and investment decisions"
            },
            "metrics_and_targets": {
                "emissions": emissions_data.get("summary", {}),
                "targets": "50% reduction in absolute emissions by 2030, net-zero by 2050",
                "performance": "Current emissions reduction trajectory: 5% annual reduction"
            }
        }
        
        # Write report data to file
        report_file = f"{report_dir}/tcfd_report.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(report_data, f, indent=2)
        
        # In a real implementation, this would be a URL to access the report
        report_url = f"file://{report_file}"
        
        return {
            "title": "TCFD Climate-Related Financial Disclosures",
            "timestamp": timestamp,
            "file_path": report_file,
            "url": report_url,
            "standard": "Task Force on Climate-Related Financial Disclosures"
        }
    
    def _generate_cdp_report(self,
                            organization_data: Dict[str, Any],
                            emissions_data: Dict[str, Any],
                            recommendations: Dict[str, Any],
                            timestamp: str,
                            org_name: str) -> Dict[str, Any]:
        """
        Generate a report following the CDP questionnaire format.
        
        Args:
            organization_data: Data about the organization
            emissions_data: Carbon footprint calculations
            recommendations: Recommended actions for reducing emissions
            timestamp: Timestamp for the report
            org_name: Organization name (formatted)
            
        Returns:
            Report metadata including URL
        """
        report_dir = f"{self.output_dir}/{org_name}/cdp_{timestamp}"
        os.makedirs(report_dir, exist_ok=True)
        
        # In a real implementation, this would generate CDP questionnaire responses
        # For this demo, we'll create a simple JSON file with sample responses
        
        report_data = {
            "report_type": "CDP",
            "organization": organization_data.get("name"),
            "cdp_section_c1": {
                "governance": {
                    "board_oversight": "Yes",
                    "management_responsibility": "Chief Sustainability Officer",
                    "incentives": "Executive compensation linked to emissions reductions"
                }
            },
            "cdp_section_c2": {
                "risks_and_opportunities": {
                    "identified_risks": [
                        "Increased carbon pricing",
                        "Changed customer behavior",
                        "Extreme weather events affecting operations"
                    ],
                    "identified_opportunities": [
                        "Resource efficiency",
                        "Development of low-carbon products",
                        "Access to new markets"
                    ]
                }
            },
            "cdp_section_c4": {
                "targets_and_performance": {
                    "emissions_targets": "Absolute target: 50% reduction by 2030 from 2020 baseline",
                    "progress": "On track - 15% reduction achieved to date"
                }
            },
            "cdp_section_c6": {
                "emissions_data": {
                    "scope_1": emissions_data['summary']['scope1'],
                    "scope_2": emissions_data['summary']['scope2'],
                    "scope_3": emissions_data['summary']['scope3'],
                    "verification": "Third-party verification conducted annually"
                }
            }
        }
        
        # Write report data to file
        report_file = f"{report_dir}/cdp_responses.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(report_data, f, indent=2)
        
        # In a real implementation, this would be a URL to access the report
        report_url = f"file://{report_file}"
        
        return {
            "title": "CDP Climate Change Questionnaire",
            "timestamp": timestamp,
            "file_path": report_file,
            "url": report_url,
            "standard": "CDP (formerly Carbon Disclosure Project)"
        }
    
    def _generate_executive_summary(self,
                                   organization_data: Dict[str, Any],
                                   emissions_data: Dict[str, Any],
                                   recommendations: Dict[str, Any],
                                   simulation_results: Dict[str, Any],
                                   timestamp: str,
                                   org_name: str) -> Dict[str, Any]:
        """
        Generate an executive summary report.
        
        Args:
            organization_data: Data about the organization
            emissions_data: Carbon footprint calculations
            recommendations: Recommended actions for reducing emissions
            simulation_results: Results of simulating different scenarios
            timestamp: Timestamp for the report
            org_name: Organization name (formatted)
            
        Returns:
            Report metadata including URL
        """
        report_dir = f"{self.output_dir}/{org_name}/executive_{timestamp}"
        os.makedirs(report_dir, exist_ok=True)
        
        # Generate charts
        charts = self._generate_charts(emissions_data, report_dir)
        
        # Extract top recommendations (assuming they're already prioritized)
        top_recommendations = recommendations.get("prioritized", [])[:5]
        
        # Extract impact summary
        impact_summary = simulation_results.get("impact_summary", {})
        
        # In a real implementation, this would generate a polished executive report
        # For this demo, we'll create a simple JSON file with report data
        
        report_data = {
            "report_type": "Executive Summary",
            "organization": organization_data.get("name"),
            "key_findings": {
                "total_emissions": f"{emissions_data['summary']['total']} tCO2e",
                "emissions_intensity": f"{emissions_data['summary']['total'] / organization_data.get('employees', 1):.2f} tCO2e per employee",
                "largest_sources": [
                    "Source 1", "Source 2", "Source 3"  # Would be populated with actual top sources
                ],
                "benchmark_comparison": "15% above industry average"  # Example benchmark
            },
            "emissions_summary": emissions_data.get("summary", {}),
            "top_recommendations": top_recommendations,
            "potential_impact": impact_summary,
            "next_steps": [
                "Review and approve recommended actions",
                "Set emissions reduction targets aligned with findings",
                "Implement prioritized recommendations",
                "Establish monitoring system for progress tracking"
            ],
            "charts": charts
        }
        
        # Write report data to file
        report_file = f"{report_dir}/executive_summary.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(report_data, f, indent=2)
        
        # In a real implementation, this would be a URL to access the report
        report_url = f"file://{report_file}"
        
        return {
            "title": "Carbon Footprint Executive Summary",
            "timestamp": timestamp,
            "file_path": report_file,
            "url": report_url
        }
    
    def _generate_technical_appendix(self,
                                    emissions_data: Dict[str, Any],
                                    timestamp: str,
                                    org_name: str) -> Dict[str, Any]:
        """
        Generate a technical appendix with detailed methodologies and data sources.
        
        Args:
            emissions_data: Carbon footprint calculations
            timestamp: Timestamp for the report
            org_name: Organization name (formatted)
            
        Returns:
            Report metadata including URL
        """
        report_dir = f"{self.output_dir}/{org_name}/technical_{timestamp}"
        os.makedirs(report_dir, exist_ok=True)
        
        # In a real implementation, this would generate a comprehensive technical document
        # For this demo, we'll create a simple JSON file with methodology information
        
        report_data = {
            "report_type": "Technical Appendix",
            "calculation_methodology": emissions_data.get("methodology", {}),
            "emissions_factors": {
                "source": "Combination of EPA, IEA, and DEFRA factors",
                "version": "2023 emissions factors",
                "specific_factors": {
                    "electricity": "EPA eGRID 2021 data",
                    "natural_gas": "EPA 2023 factors",
                    "business_travel": "DEFRA 2023 factors"
                }
            },
            "data_quality": {
                "assessment": "Primary data used for 75% of emissions calculations, secondary data for 25%",
                "limitations": [
                    "Limited primary data for some Scope 3 categories",
                    "Some emissions factors based on industry averages",
                    "Estimates used for some employee commuting patterns"
                ],
                "improvement_plan": "Implementing enhanced data collection for Scope 3 categories in next reporting cycle"
            },
            "calculation_details": {
                "scope1_methodology": "Direct measurement of fuel consumption with standard conversion factors",
                "scope2_methodology": "Location-based method using grid emissions factors",
                "scope3_methodology": "Combination of spend-based and activity-based methods depending on category"
            },
            "assumptions": emissions_data.get("methodology", {}).get("assumptions", [])
        }
        
        # Write report data to file
        report_file = f"{report_dir}/technical_appendix.json"
        with open(report_file, 'w') as f:
            import json
            json.dump(report_data, f, indent=2)
        
        # In a real implementation, this would be a URL to access the report
        report_url = f"file://{report_file}"
        
        return {
            "title": "Carbon Footprint Technical Appendix",
            "timestamp": timestamp,
            "file_path": report_file,
            "url": report_url
        }

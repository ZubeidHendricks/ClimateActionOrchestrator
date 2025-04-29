# Quick Start Tutorial for Climate Action Orchestrator

This tutorial will guide you through the basic usage of the Climate Action Orchestrator to analyze your organization's carbon footprint and generate sustainability recommendations.

## Prerequisites

Before beginning this tutorial, ensure you have:

- Completed the [Installation Guide](installation.md)
- Access to your organization's operational data (energy consumption, travel, etc.)
- Basic familiarity with carbon accounting concepts (GHG Protocol, scopes, etc.)

## 1. Prepare Your Data

The Climate Action Orchestrator can work with various data sources:

### CSV Files

Prepare CSV files with operational data in the following structure:

**Energy consumption (scope2_data.csv):**
```
facility_name,electricity_kwh,grid_region,month,year
Headquarters,50000,WECC,1,2023
Headquarters,48000,WECC,2,2023
...
```

**Business travel (scope3_travel.csv):**
```
trip_id,mode,distance_miles,employee_count,date
T001,air,2500,1,2023-01-15
T002,car,120,2,2023-01-20
...
```

Place your CSV files in the `data` directory or configure custom locations in the next step.

### Azure Blob Storage

If your data is in Azure Blob Storage, make note of the container names and blob paths.

### Other Data Sources

For API or database connections, prepare the necessary connection details and access credentials.

## 2. Configure Data Sources

Create a `config.json` file in the root directory with the following structure:

```json
{
  "organization": {
    "name": "Example Corp",
    "industry": "Technology",
    "employees": 500,
    "locations": [
      {"city": "Seattle", "country": "USA", "type": "headquarters"},
      {"city": "Austin", "country": "USA", "type": "office"}
    ]
  },
  "data_sources": {
    "energy": {
      "type": "csv",
      "config": {
        "files": ["data/scope2_data.csv"]
      }
    },
    "business_travel": {
      "type": "csv",
      "config": {
        "files": ["data/scope3_travel.csv"]
      }
    },
    "waste": {
      "type": "azure_blob",
      "config": {
        "container": "sustainability-data",
        "blob": "waste/2023_waste_data.csv",
        "format": "csv"
      }
    }
  }
}
```

## 3. Run the Emissions Analysis

Execute the following Python code to run an emissions analysis:

```python
from orchestrator import ClimateActionOrchestrator

# Initialize the orchestrator with your configuration
orchestrator = ClimateActionOrchestrator('config.json')

# Define your organization data
organization_data = {
    "name": "Example Corp",
    "industry": "Technology",
    "employees": 500,
    "locations": [
        {"city": "Seattle", "country": "USA", "type": "headquarters"},
        {"city": "Austin", "country": "USA", "type": "office"}
    ],
    "data_sources": {
        "energy": "csv",
        "transport": "csv",
        "waste": "azure_blob"
    }
}

# Run the analysis
results = orchestrator.start_emissions_analysis(organization_data)

# Print summary results
print(f"Analysis complete. Total emissions: {results['emissions_summary']['total']} tCO2e")
print(f"Top recommendation: {results['top_recommendations'][0]['title']}")

# Access detailed reports
for report_type, url in results['reports'].items():
    print(f"{report_type}: {url}")
```

## 4. Explore the Results

The analysis results include:

- **Emissions Summary**: Total carbon footprint broken down by scope and category
- **Top Recommendations**: Prioritized list of actions to reduce emissions
- **Potential Impact**: Estimated effect of implementing recommendations
- **Reports**: Links to detailed reports in various formats

## 5. Provide Feedback on Recommendations

You can provide feedback on the recommendations to refine the analysis:

```python
# Define your feedback
feedback = {
    "recommendation_adjustments": [
        {
            "id": "rec123",  # ID from the original recommendations
            "priority": "high",  # Adjust priority
            "notes": "This aligns with our sustainability goals"
        },
        {
            "id": "rec456",
            "exclude": True,  # Remove this recommendation
            "reason": "Not feasible in our current facilities"
        }
    ],
    "additional_constraints": {
        "budget_limit": 250000,
        "implementation_timeline": "18_months"
    }
}

# Process feedback and get updated results
updated_results = orchestrator.human_feedback_loop(feedback)

# Review updated recommendations
print(f"Updated top recommendation: {updated_results['updated_recommendations'][0]['title']}")
```

## 6. Access Generated Reports

The orchestrator generates several types of reports:

1. **GHG Protocol Report**: Standard emissions inventory
2. **TCFD Report**: Climate-related financial disclosures
3. **CDP Report**: Climate Change Questionnaire responses
4. **Executive Summary**: Overview for leadership
5. **Technical Appendix**: Detailed methodology documentation

Access these reports using the URLs provided in the results.

## 7. Schedule Regular Updates

For ongoing emissions tracking, set up a regular schedule to update your data and re-run the analysis. This can be done:

- Manually as new data becomes available
- Via automated scripts on a weekly/monthly basis
- Through integration with your existing data pipelines

## Next Steps

Now that you've completed the quick start tutorial, explore these advanced topics:

- [Custom Emissions Factors Guide](emissions_factors.md)
- [Advanced Scenario Modeling](scenario_modeling.md)
- [Integration with Existing Systems](integrations.md)
- [Regulatory Reporting Guide](regulatory_reporting.md)

For technical reference, see the [API Documentation](api_reference.md).

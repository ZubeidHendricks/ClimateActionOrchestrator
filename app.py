"""
Climate Action Orchestrator Dashboard
Flask-based web dashboard for the Climate Action Orchestrator
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import datetime
import random

app = Flask(__name__)

# Sample data for the dashboard
def load_sample_data():
    emissions_data = {
        'total': 1245.8,
        'scope1': 168.3,
        'scope2': 632.5,
        'scope3': 445.0,
        'by_facility': {
            'Headquarters': 845.2,
            'AustinOffice': 400.6
        },
        'by_category': {
            'electricity': 632.5,
            'business_travel': 318.7,
            'waste': 126.3,
            'fuel': 168.3
        },
        'trend': 3.2,  # Percentage change since last period
        'quarterly_data': [
            {'quarter': 'Q1 2023', 'scope1': 160.5, 'scope2': 610.2, 'scope3': 420.8, 'total': 1191.5},
            {'quarter': 'Q2 2023', 'scope1': 162.8, 'scope2': 618.4, 'scope3': 425.6, 'total': 1206.8},
            {'quarter': 'Q3 2023', 'scope1': 165.9, 'scope2': 625.1, 'scope3': 435.2, 'total': 1226.2},
            {'quarter': 'Q4 2023', 'scope1': 166.7, 'scope2': 629.3, 'scope3': 440.1, 'total': 1236.1},
            {'quarter': 'Q1 2024', 'scope1': 168.3, 'scope2': 632.5, 'scope3': 445.0, 'total': 1245.8}
        ]
    }
    
    recommendations = [
        {
            'id': 'rec123',
            'title': 'Switch to renewable energy provider',
            'description': 'Transition to a 100% renewable energy contract for all facilities',
            'potential_reduction': 450.2,
            'estimated_cost': 15000,
            'difficulty': 'medium',
            'timeframe': '3-6 months',
            'priority': 'high'
        },
        {
            'id': 'rec456',
            'title': 'Implement remote work policy',
            'description': 'Reduce business travel and commuting by 30% through expanded remote work',
            'potential_reduction': 95.6,
            'estimated_cost': 5000,
            'difficulty': 'low',
            'timeframe': '1-3 months',
            'priority': 'medium'
        },
        {
            'id': 'rec789',
            'title': 'Install LED lighting systems',
            'description': 'Replace all conventional lighting with LED systems',
            'potential_reduction': 85.3,
            'estimated_cost': 32000,
            'difficulty': 'medium',
            'timeframe': '2-4 months',
            'priority': 'medium'
        },
        {
            'id': 'rec101',
            'title': 'Optimize HVAC scheduling',
            'description': 'Implement smart controls and scheduling for heating and cooling systems',
            'potential_reduction': 75.2,
            'estimated_cost': 12000,
            'difficulty': 'medium',
            'timeframe': '2-3 months',
            'priority': 'medium'
        },
        {
            'id': 'rec102',
            'title': 'Switch to electric vehicle fleet',
            'description': 'Gradually replace company vehicles with electric alternatives',
            'potential_reduction': 120.5,
            'estimated_cost': 150000,
            'difficulty': 'high',
            'timeframe': '12-24 months',
            'priority': 'low'
        }
    ]
    
    agents = [
        {
            'name': 'Data Collection Agent',
            'status': 'Active',
            'last_activity': '2 minutes ago',
            'tasks_processed': 42,
            'description': 'Gathers operational data from various sources'
        },
        {
            'name': 'Carbon Calculation Agent',
            'status': 'Active',
            'last_activity': '5 minutes ago',
            'tasks_processed': 38,
            'description': 'Calculates carbon footprint using emissions factors'
        },
        {
            'name': 'Recommendation Agent',
            'status': 'Active',
            'last_activity': '8 minutes ago',
            'tasks_processed': 15,
            'description': 'Analyzes data to generate sustainability recommendations'
        },
        {
            'name': 'Simulation Agent',
            'status': 'Active',
            'last_activity': '15 minutes ago',
            'tasks_processed': 7,
            'description': 'Projects outcomes of different sustainability initiatives'
        },
        {
            'name': 'Reporting Agent',
            'status': 'Active',
            'last_activity': '12 minutes ago',
            'tasks_processed': 12,
            'description': 'Generates standardized documentation and reports'
        }
    ]
    
    return {
        'emissions': emissions_data,
        'recommendations': recommendations,
        'agents': agents,
        'organization': {
            'name': 'Example Corp',
            'industry': 'Technology',
            'employees': 500,
            'sustainability_score': 78
        }
    }

# Routes
@app.route('/')
def index():
    data = load_sample_data()
    return render_template('index.html', data=data)

@app.route('/agents')
def agents():
    data = load_sample_data()
    return render_template('agents.html', data=data)

@app.route('/recommendations')
def recommendations():
    data = load_sample_data()
    return render_template('recommendations.html', data=data)

@app.route('/data-sources')
def data_sources():
    return render_template('data_sources.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/api/agents/status')
def agent_status():
    """API endpoint to simulate real-time agent status updates"""
    data = load_sample_data()
    agents = data['agents']
    
    # Simulate some activity changes
    for agent in agents:
        # Randomly update last activity time
        time_options = ['just now', '1 minute ago', '2 minutes ago', '5 minutes ago', '10 minutes ago']
        agent['last_activity'] = random.choice(time_options)
        
        # Occasionally increment tasks processed
        if random.random() > 0.7:
            agent['tasks_processed'] += 1
    
    return jsonify(agents)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)

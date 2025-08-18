import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# Load and process the data
data = {
    'Employee': ['Arun Ghule', 'Ashlesha Nandankar', 'Harish Sahare', 'Irshaad Sheikh', 'Rishabh Dabruse'],
    'Comments': [232, 191, 238, 212, 217],
    'New_Applications': [0, 0, 1, 0, 0],
    'Stage_Changes': [0, 5, 3, 6, 9],
    'Cases_Closed_After_Offer': [0, 0, 13, 0, 0],
    'Deposits': [1, 1, 5, 3, 6],
    'Hold_by_University': [0, 0, 3, 1, 1],
    'Other': [46, 33, 37, 69, 20],
    'Rejected_by_University': [0, 0, 5, 0, 1],
    'Total_Actions': [296, 234, 362, 293, 255]
}

df = pd.DataFrame(data)

# Calculate performance metrics
df['Productivity_Score'] = df['Total_Actions']
df['Success_Rate'] = ((df['Cases_Closed_After_Offer'] + df['Deposits']) / df['Total_Actions'] * 100).round(2)
df['Efficiency_Score'] = (df['Comments'] / df['Total_Actions'] * 100).round(2)

# Performance Analysis
def analyze_performance():
    analysis = {
        'top_performer': {
            'name': df.loc[df['Total_Actions'].idxmax(), 'Employee'],
            'total_actions': int(df['Total_Actions'].max()),
            'reason': 'Highest total productivity'
        },
        'most_efficient': {
            'name': df.loc[df['Success_Rate'].idxmax(), 'Employee'],
            'success_rate': float(df['Success_Rate'].max()),
            'reason': 'Best success rate in closing deals'
        },
        'needs_improvement': {
            'name': df.loc[df['Total_Actions'].idxmin(), 'Employee'],
            'total_actions': int(df['Total_Actions'].min()),
            'reason': 'Lowest total productivity'
        },
        'insights': [
            f"Harish Sahare leads with {df.loc[df['Employee'] == 'Harish Sahare', 'Total_Actions'].iloc[0]} total actions",
            f"Average team productivity: {df['Total_Actions'].mean():.0f} actions per employee",
            f"Top success rate: {df['Success_Rate'].max():.1f}% (Cases closed + Deposits)",
            f"Total team output: {df['Total_Actions'].sum()} actions"
        ]
    }
    return analysis

# Generate visualizations
def create_dashboard():
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total Actions by Employee', 'Success Rate Analysis', 
                       'Comment Activity', 'Action Distribution'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}]]
    )
    
    # Total Actions Bar Chart
    fig.add_trace(
        go.Bar(x=df['Employee'], y=df['Total_Actions'], 
               name='Total Actions',
               marker_color='lightblue'),
        row=1, col=1
    )
    
    # Success Rate Bar Chart
    fig.add_trace(
        go.Bar(x=df['Employee'], y=df['Success_Rate'], 
               name='Success Rate (%)',
               marker_color='lightgreen'),
        row=1, col=2
    )
    
    # Comments Activity
    fig.add_trace(
        go.Bar(x=df['Employee'], y=df['Comments'], 
               name='Comments',
               marker_color='orange'),
        row=2, col=1
    )
    
    # Action Distribution Pie Chart
    action_totals = {
        'Comments': df['Comments'].sum(),
        'Stage Changes': df['Stage_Changes'].sum(),
        'Cases Closed': df['Cases_Closed_After_Offer'].sum(),
        'Deposits': df['Deposits'].sum(),
        'Other': df['Other'].sum()
    }
    
    fig.add_trace(
        go.Pie(labels=list(action_totals.keys()), 
               values=list(action_totals.values()),
               name="Action Distribution"),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text="Employee Performance Dashboard - Daily Work Report",
        title_x=0.5,
        showlegend=False,
        height=800
    )
    
    return fig

# Save analysis and dashboard data
analysis_results = analyze_performance()
dashboard_fig = create_dashboard()

# Export for web display
with open('/workspace/analysis_data.json', 'w') as f:
    json.dump({
        'employee_data': df.to_dict('records'),
        'analysis': analysis_results
    }, f, indent=2)

# Save HTML version of dashboard
dashboard_fig.write_html('/workspace/dashboard.html')

print("Dashboard and analysis generated successfully!")
print(f"Top Performer: {analysis_results['top_performer']['name']}")
print(f"Most Efficient: {analysis_results['most_efficient']['name']}")
print(f"Needs Improvement: {analysis_results['needs_improvement']['name']}")
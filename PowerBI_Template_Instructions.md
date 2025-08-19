# Power BI Dashboard Setup Instructions

## Data Import Steps

1. **Open Power BI Desktop**
2. **Import Data:**
   - Click "Get Data" > "Text/CSV"
   - Select the `employee_data.csv` file
   - Click "Load"

## Creating Visualizations

### 1. Total Actions Bar Chart
- **Visualization Type:** Clustered Column Chart
- **Axis:** Employee Names
- **Values:** Total Actions
- **Title:** "Total Actions by Employee"

### 2. Success Rate Analysis
- **Visualization Type:** Clustered Column Chart
- **Axis:** Employee Names
- **Values:** Success Rate (calculated field)
- **Formula:** `Success Rate = (Cases Closed After Offer + Deposits) / Total Actions * 100`

### 3. Comment Activity Chart
- **Visualization Type:** Bar Chart
- **Axis:** Employee Names
- **Values:** Comments
- **Title:** "Comment Activity by Employee"

### 4. Action Distribution Pie Chart
- **Visualization Type:** Pie Chart
- **Legend:** Action Types
- **Values:** Sum of each action type
- **Categories:** Comments, Stage Changes, Cases Closed, Deposits, Other

### 5. KPI Cards
Create individual card visualizations for:
- Total Team Actions
- Average Actions per Employee
- Total Deposits
- Total Cases Closed
- Success Rate Average

## Calculated Fields to Create

```DAX
Success Rate = 
DIVIDE(
    [Cases Closed After Offer] + [Deposits],
    [Total Actions]
) * 100

Team Average = 
AVERAGE([Total Actions])

Top Performer = 
TOPN(1, VALUES([Employee]), [Total Actions], DESC)

Productivity Score = 
RANKX(ALL([Employee]), [Total Actions], , DESC)
```

## Dashboard Layout Recommendations

1. **Top Section:** KPI cards showing key metrics
2. **Middle Section:** Bar charts for total actions and success rates
3. **Bottom Section:** Pie chart for action distribution and detailed table

## Color Scheme
- Primary: Blue (#4472C4)
- Secondary: Green (#70AD47)
- Accent: Orange (#FFC000)
- Warning: Red (#C5504B)

## Filters to Add
- Date Range Slicer
- Employee Multi-Select
- Department Filter (if applicable)

## Key Insights to Highlight
1. Harish Sahare is the top performer with 362 total actions
2. Team average is 288 actions per employee
3. Success rate varies significantly across team members
4. Comments represent the largest portion of daily activities

## Export Options
- Save as .pbix file for sharing
- Publish to Power BI Service for web access
- Export to PowerPoint for presentations
- Schedule data refresh if connecting to live data source
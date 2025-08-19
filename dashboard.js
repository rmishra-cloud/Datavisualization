// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Set current date
    document.getElementById('currentDate').textContent = new Date().toLocaleDateString();
    
    // Load analysis data (from analysis_report.js)
    const data = employeeData;
    const analysis = performanceAnalysis;
    
    // Update key metrics cards
    updateKeyMetrics(analysis);
    
    // Update team statistics
    updateTeamStats(analysis.teamStats);
    
    // Create charts
    createTotalActionsChart(data);
    createSuccessRateChart(data);
    createCommentsChart(data);
    createActionDistributionChart(data);
    
    // Update insights and recommendations
    updateInsights(analysis.insights);
    updateRecommendations(analysis.recommendations);
    
    // Update employee table
    updateEmployeeTable(data);
});

function updateKeyMetrics(analysis) {
    document.getElementById('topPerformer').textContent = analysis.topPerformer.employee.name;
    document.getElementById('topPerformerMetric').textContent = `${analysis.topPerformer.employee.totalActions} total actions`;
    
    document.getElementById('mostEfficient').textContent = analysis.mostEfficient.employee.name;
    document.getElementById('efficientMetric').textContent = `${analysis.mostEfficient.employee.successRate}% success rate`;
    
    document.getElementById('needsImprovement').textContent = analysis.needsImprovement.employee.name;
    document.getElementById('improvementMetric').textContent = `${analysis.needsImprovement.employee.totalActions} total actions`;
}

function updateTeamStats(stats) {
    document.getElementById('totalActions').textContent = stats.totalActions;
    document.getElementById('avgActions').textContent = stats.averageActions;
    document.getElementById('totalComments').textContent = stats.totalComments;
    document.getElementById('totalDeposits').textContent = stats.totalDeposits;
    document.getElementById('totalClosed').textContent = stats.totalCasesClosed;
}

function createTotalActionsChart(data) {
    const ctx = document.getElementById('totalActionsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(emp => emp.name),
            datasets: [{
                label: 'Total Actions',
                data: data.map(emp => emp.totalActions),
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createSuccessRateChart(data) {
    const ctx = document.getElementById('successRateChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(emp => emp.name),
            datasets: [{
                label: 'Success Rate (%)',
                data: data.map(emp => emp.successRate),
                backgroundColor: 'rgba(75, 192, 192, 0.8)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: Math.max(...data.map(emp => emp.successRate)) + 1
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createCommentsChart(data) {
    const ctx = document.getElementById('commentsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(emp => emp.name),
            datasets: [{
                label: 'Comments',
                data: data.map(emp => emp.comments),
                backgroundColor: 'rgba(153, 102, 255, 0.8)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createActionDistributionChart(data) {
    const ctx = document.getElementById('actionDistributionChart').getContext('2d');
    
    const totalComments = data.reduce((sum, emp) => sum + emp.comments, 0);
    const totalStageChanges = data.reduce((sum, emp) => sum + emp.stageChanges, 0);
    const totalCasesClosed = data.reduce((sum, emp) => sum + emp.casesClosedAfterOffer, 0);
    const totalDeposits = data.reduce((sum, emp) => sum + emp.deposits, 0);
    const totalOther = data.reduce((sum, emp) => sum + emp.other, 0);
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Comments', 'Stage Changes', 'Cases Closed', 'Deposits', 'Other'],
            datasets: [{
                data: [totalComments, totalStageChanges, totalCasesClosed, totalDeposits, totalOther],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateInsights(insights) {
    const insightsList = document.getElementById('insightsList');
    insightsList.innerHTML = '';
    
    insights.forEach(insight => {
        const li = document.createElement('li');
        li.className = 'flex items-start space-x-2 p-2 bg-yellow-50 rounded-lg';
        li.innerHTML = `
            <i class="fas fa-star text-yellow-500 mt-1"></i>
            <span class="text-gray-700">${insight}</span>
        `;
        insightsList.appendChild(li);
    });
}

function updateRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    
    recommendations.forEach(recommendation => {
        const li = document.createElement('li');
        li.className = 'flex items-start space-x-2 p-2 bg-teal-50 rounded-lg';
        li.innerHTML = `
            <i class="fas fa-arrow-right text-teal-500 mt-1"></i>
            <span class="text-gray-700">${recommendation}</span>
        `;
        recommendationsList.appendChild(li);
    });
}

function updateEmployeeTable(data) {
    const tableBody = document.getElementById('employeeTableBody');
    tableBody.innerHTML = '';
    
    data.forEach((emp, index) => {
        const row = document.createElement('tr');
        row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';
        
        row.innerHTML = `
            <td class="px-4 py-3 font-medium text-gray-900">${emp.name}</td>
            <td class="px-4 py-3 text-center text-gray-700">${emp.totalActions}</td>
            <td class="px-4 py-3 text-center text-gray-700">${emp.comments}</td>
            <td class="px-4 py-3 text-center">
                <span class="px-2 py-1 text-xs font-semibold rounded-full ${
                    emp.successRate >= 5 ? 'bg-green-100 text-green-800' : 
                    emp.successRate >= 2 ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-red-100 text-red-800'
                }">
                    ${emp.successRate}%
                </span>
            </td>
            <td class="px-4 py-3 text-center text-gray-700">${emp.deposits}</td>
            <td class="px-4 py-3 text-center text-gray-700">${emp.casesClosedAfterOffer}</td>
        `;
        
        tableBody.appendChild(row);
    });
}
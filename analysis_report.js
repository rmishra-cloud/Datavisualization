// Employee Performance Analysis Data
const employeeData = [
    {
        name: "Arun Ghule",
        comments: 232,
        newApplications: 0,
        stageChanges: 0,
        casesClosedAfterOffer: 0,
        deposits: 1,
        holdByUniversity: 0,
        other: 46,
        rejectedByUniversity: 0,
        totalActions: 296
    },
    {
        name: "Ashlesha Nandankar",
        comments: 191,
        newApplications: 0,
        stageChanges: 5,
        casesClosedAfterOffer: 0,
        deposits: 1,
        holdByUniversity: 0,
        other: 33,
        rejectedByUniversity: 0,
        totalActions: 234
    },
    {
        name: "Harish Sahare",
        comments: 238,
        newApplications: 1,
        stageChanges: 3,
        casesClosedAfterOffer: 13,
        deposits: 5,
        holdByUniversity: 3,
        other: 37,
        rejectedByUniversity: 5,
        totalActions: 362
    },
    {
        name: "Irshaad Sheikh",
        comments: 212,
        newApplications: 0,
        stageChanges: 6,
        casesClosedAfterOffer: 0,
        deposits: 3,
        holdByUniversity: 1,
        other: 69,
        rejectedByUniversity: 0,
        totalActions: 293
    },
    {
        name: "Rishabh Dabruse",
        comments: 217,
        newApplications: 0,
        stageChanges: 9,
        casesClosedAfterOffer: 0,
        deposits: 6,
        holdByUniversity: 1,
        other: 20,
        rejectedByUniversity: 1,
        totalActions: 255
    }
];

// Calculate performance metrics
const analysisResults = employeeData.map(emp => {
    const successfulActions = emp.casesClosedAfterOffer + emp.deposits;
    const successRate = emp.totalActions > 0 ? (successfulActions / emp.totalActions * 100).toFixed(2) : 0;
    const commentRatio = (emp.comments / emp.totalActions * 100).toFixed(2);
    
    return {
        ...emp,
        successfulActions,
        successRate: parseFloat(successRate),
        commentRatio: parseFloat(commentRatio)
    };
});

// Performance Analysis
const performanceAnalysis = {
    topPerformer: {
        employee: analysisResults.reduce((prev, current) => 
            prev.totalActions > current.totalActions ? prev : current
        ),
        metric: "Total Actions",
        reason: "Highest overall productivity with comprehensive task completion"
    },
    
    mostEfficient: {
        employee: analysisResults.reduce((prev, current) => 
            prev.successRate > current.successRate ? prev : current
        ),
        metric: "Success Rate",
        reason: "Best conversion rate for closing deals and securing deposits"
    },
    
    needsImprovement: {
        employee: analysisResults.reduce((prev, current) => 
            prev.totalActions < current.totalActions ? prev : current
        ),
        metric: "Total Actions",
        reason: "Lowest overall productivity, needs support and guidance"
    },
    
    teamStats: {
        totalActions: analysisResults.reduce((sum, emp) => sum + emp.totalActions, 0),
        averageActions: (analysisResults.reduce((sum, emp) => sum + emp.totalActions, 0) / analysisResults.length).toFixed(0),
        totalComments: analysisResults.reduce((sum, emp) => sum + emp.comments, 0),
        totalDeposits: analysisResults.reduce((sum, emp) => sum + emp.deposits, 0),
        totalCasesClosed: analysisResults.reduce((sum, emp) => sum + emp.casesClosedAfterOffer, 0)
    },
    
    insights: [
        `🏆 Harish Sahare leads the team with ${analysisResults.find(e => e.name === "Harish Sahare").totalActions} total actions`,
        `📈 Harish Sahare has the highest success rate at ${analysisResults.find(e => e.name === "Harish Sahare").successRate}%`,
        `💼 Team processed ${analysisResults.reduce((sum, emp) => sum + emp.totalActions, 0)} total actions today`,
        `🎯 Average team productivity: ${(analysisResults.reduce((sum, emp) => sum + emp.totalActions, 0) / analysisResults.length).toFixed(0)} actions per employee`,
        `✅ Total successful outcomes: ${analysisResults.reduce((sum, emp) => sum + emp.deposits + emp.casesClosedAfterOffer, 0)} (deposits + closed cases)`
    ],
    
    recommendations: [
        "Harish Sahare should mentor other team members on efficient case closure techniques",
        "Ashlesha Nandankar shows potential with good stage management - focus on conversion",
        "Irshaad Sheikh handles high 'Other' category volume - review task categorization",
        "Team should focus on improving deposit conversion rates",
        "Consider implementing Harish's successful strategies across the team"
    ]
};

// Export data for dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { employeeData: analysisResults, performanceAnalysis };
}
/**
 * Initiative List Charts Module
 * Adds dynamic data visualization to the initiatives list page
 */

class InitiativeCharts {
    constructor() {
        this.categoryChart = null;
        this.statusChart = null;
        this.impactChart = null;
        this.chartsInitialized = false;
    }

    initialize() {
        if (this.chartsInitialized) return;
        
        this.initCategoryDistribution();
        this.initStatusDistribution();
        this.initImpactComparison();
        
        this.chartsInitialized = true;
        
        // Update charts when window resizes
        window.addEventListener('resize', this.handleResize.bind(this));
    }
    
    handleResize() {
        if (this.categoryChart) this.categoryChart.resize();
        if (this.statusChart) this.statusChart.resize();
        if (this.impactChart) this.impactChart.resize();
    }
    
    // Category distribution chart
    initCategoryDistribution() {
        const ctx = document.getElementById('categoryDistributionChart');
        if (!ctx) return;
        
        // Extract data from the page
        const categories = {};
        document.querySelectorAll('.category-badge').forEach(badge => {
            const category = badge.textContent.trim();
            categories[category] = (categories[category] || 0) + 1;
        });
        
        const labels = Object.keys(categories);
        const data = Object.values(categories);
        const backgroundColors = this.getCategoryColors(labels);
        
        this.categoryChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            font: {
                                size: 12
                            },
                            boxWidth: 15,
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%',
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
    
    // Status distribution chart
    initStatusDistribution() {
        const ctx = document.getElementById('statusDistributionChart');
        if (!ctx) return;
          // Extract data from the page
        const statuses = {};
        document.querySelectorAll('.status-tags .badge').forEach(status => {
            const statusText = status.textContent.trim();
            if (statusText !== '' && !statusText.includes('map-marker')) {  // Filter out location badges
                statuses[statusText] = (statuses[statusText] || 0) + 1;
            }
        });
        
        const labels = Object.keys(statuses);
        const data = Object.values(statuses);
        const backgroundColors = this.getStatusColors(labels);
        
        this.statusChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 12
                            },
                            boxWidth: 15,
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
    
    // Impact comparison chart
    initImpactComparison() {
        const ctx = document.getElementById('impactComparisonChart');
        if (!ctx) return;
        
        // Extract impact data
        const impactData = {
            carbon: [],
            energy: [],
            water: []
        };
        
        const initiatives = [];
        
        document.querySelectorAll('.initiative-card').forEach(card => {
            const title = card.querySelector('.initiative-title').textContent.trim();
            const detailsSection = card.querySelector('.initiative-details');
            
            if (detailsSection) {
                const impactStats = detailsSection.querySelectorAll('.impact-stat');
                
                impactStats.forEach((stat, index) => {
                    const value = stat.querySelector('.impact-value') ? 
                        parseFloat(stat.querySelector('.impact-value').textContent.replace(/,/g, '')) : 0;
                    
                    if (index === 0) impactData.carbon.push(value);
                    if (index === 1) impactData.energy.push(value);
                    if (index === 2) impactData.water.push(value);
                });
                
                initiatives.push(title);
            }
        });
        
        // Only show top 5 initiatives for readability
        if (initiatives.length > 5) {
            initiatives.length = 5;
            impactData.carbon.length = 5;
            impactData.energy.length = 5;
            impactData.water.length = 5;
        }
        
        this.impactChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: initiatives,
                datasets: [
                    {
                        label: 'Carbon Impact',
                        data: impactData.carbon,
                        backgroundColor: 'rgba(37, 162, 68, 0.7)',
                        borderColor: 'rgba(37, 162, 68, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Energy Impact',
                        data: impactData.energy,
                        backgroundColor: 'rgba(255, 193, 7, 0.7)',
                        borderColor: 'rgba(255, 193, 7, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Water Impact',
                        data: impactData.water,
                        backgroundColor: 'rgba(13, 110, 253, 0.7)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                }
            }
        });
    }
    
    getCategoryColors(categories) {
        const colorMap = {
            'Renewable Energy': '#22c55e',
            'Recycling': '#3b82f6',
            'Emission Control': '#f59e0b',
            'Water Conservation': '#06b6d4',
            'Reforestation': '#16a34a',
            'Sustainable Agriculture': '#65a30d',
            'Clean Transportation': '#8b5cf6',
            'Waste Management': '#ef4444',
            'Green Technology': '#0ea5e9',
            'Ocean Conservation': '#0284c7'
        };
        
        return categories.map(category => colorMap[category] || '#6b7280');
    }
    
    getStatusColors(statuses) {
        const colorMap = {
            'Active': '#3b82f6',
            'Completed': '#22c55e',
            'Funded': '#0ea5e9',
            'Draft': '#94a3b8',
            'Cancelled': '#f97316'
        };
        
        return statuses.map(status => colorMap[status] || '#6b7280');
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const chartsTrigger = document.getElementById('showChartsBtn');
    const charts = new InitiativeCharts();
    
    if (chartsTrigger) {
        chartsTrigger.addEventListener('click', function() {
            charts.initialize();
        });
    }
});

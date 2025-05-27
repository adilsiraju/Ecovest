/**
 * Mobile responsiveness utility functions for Dashboard page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // Auto-collapse some sections after a delay to improve initial loading experience
        setTimeout(() => {
            const sections = ['portfolioInsights', 'investmentDistribution', 'recommendedInitiatives'];
            sections.forEach(sectionId => {
                const section = document.getElementById(sectionId);
                if (section) {
                    const collapse = bootstrap.Collapse.getInstance(section) || 
                                    new bootstrap.Collapse(section, {toggle: false});
                    collapse.hide();
                    
                    // Update toggle icon
                    const toggleButton = document.querySelector(`[data-bs-target="#${sectionId}"]`);
                    if (toggleButton) {
                        const icon = toggleButton.querySelector('.fa-chevron-down');
                        if (icon) {
                            icon.style.transform = 'rotate(-90deg)';
                        }
                    }
                }
            });
        }, 1000);
        
        // Make tables more mobile-friendly
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            // Add horizontal scroll wrapper if not already present
            if (!table.parentElement.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
            
            // Make the table more compact
            table.classList.add('table-sm');
            
            // If it's a holdings or transactions table, add special mobile formatting
            if (table.classList.contains('holdings-table') || table.classList.contains('transactions-table')) {
                // Add data-labels for responsive tables
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
                
                // Add data attributes to cells for mobile labels
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    cells.forEach((cell, i) => {
                        if (headers[i]) {
                            cell.setAttribute('data-label', headers[i]);
                        }
                    });
                });
                
                // Add special class for stacked mobile view
                table.classList.add('table-mobile-stacked');
            }
        });
        
        // Optimize charts for mobile
        const chartCanvases = document.querySelectorAll('canvas');
        chartCanvases.forEach(canvas => {
            // Set max height for charts
            canvas.style.maxHeight = '250px';
            
            // Get chart instance
            const chartInstance = Chart.getChart(canvas);
            if (chartInstance) {
                // Optimize chart options for mobile
                if (chartInstance.config.type === 'pie' || chartInstance.config.type === 'doughnut') {
                    // For pie/doughnut charts
                    if (chartInstance.options.plugins && chartInstance.options.plugins.legend) {
                        chartInstance.options.plugins.legend.position = 'bottom';
                        
                        if (chartInstance.options.plugins.legend.labels) {
                            chartInstance.options.plugins.legend.labels.boxWidth = 10;
                            chartInstance.options.plugins.legend.labels.padding = 8;
                            chartInstance.options.plugins.legend.labels.font = { size: 10 };
                        }
                    }
                } else if (chartInstance.config.type === 'line' || chartInstance.config.type === 'bar') {
                    // For line/bar charts
                    if (chartInstance.options.scales && chartInstance.options.scales.x) {
                        // Limit x-axis ticks for cleaner display
                        chartInstance.options.scales.x.ticks = {
                            maxRotation: 0,
                            autoSkip: true,
                            maxTicksLimit: 5,
                            font: { size: 9 }
                        };
                    }
                    
                    if (chartInstance.options.scales && chartInstance.options.scales.y) {
                        // Optimize y-axis
                        chartInstance.options.scales.y.ticks = {
                            font: { size: 9 },
                            padding: 4
                        };
                    }
                }
                
                // Update the chart
                chartInstance.update();
            }
        });
        
        // Add swipe gestures for holdings section if touch is supported
        if ('ontouchstart' in window) {
            const holdingsSection = document.querySelector('.holdings-section');
            if (holdingsSection) {
                let startX, startY, distX, distY;
                let threshold = 100; // Minimum distance for swipe
                let restraint = 100; // Maximum perpendicular distance allowed
                let allowedTime = 300; // Maximum time allowed for the swipe
                let startTime;
                
                holdingsSection.addEventListener('touchstart', function(e) {
                    const touchObj = e.changedTouches[0];
                    startX = touchObj.pageX;
                    startY = touchObj.pageY;
                    startTime = new Date().getTime();
                    e.preventDefault();
                }, false);
                
                holdingsSection.addEventListener('touchend', function(e) {
                    const touchObj = e.changedTouches[0];
                    distX = touchObj.pageX - startX;
                    distY = touchObj.pageY - startY;
                    const elapsedTime = new Date().getTime() - startTime;
                    
                    // Check if time and distance requirements are met
                    if (elapsedTime <= allowedTime) {
                        if (Math.abs(distX) >= threshold && Math.abs(distY) <= restraint) {
                            // Horizontal swipe detected
                            const direction = distX > 0 ? 'right' : 'left';
                            
                            // Handle swipe direction
                            if (direction === 'left') {
                                // Show more details or next page
                                const detailsToggle = holdingsSection.querySelector('.details-toggle');
                                if (detailsToggle) detailsToggle.click();
                            } else if (direction === 'right') {
                                // Go back or hide details
                                const backButton = holdingsSection.querySelector('.back-button');
                                if (backButton) backButton.click();
                            }
                        }
                    }
                }, false);
            }
        }
        
        // Add refresh pull-down functionality
        function addPullToRefresh() {
            let touchStartY = 0;
            let touchEndY = 0;
            const minDistance = 100; // Minimum pull distance to trigger refresh
            const refreshThreshold = 150; // Distance at which refresh is triggered
            let refreshing = false;
            let startScrollTop = 0;
            
            // Create refresh indicator
            const refreshIndicator = document.createElement('div');
            refreshIndicator.className = 'pull-to-refresh-indicator';
            refreshIndicator.innerHTML = '<i class="fas fa-sync-alt"></i>';
            refreshIndicator.style.cssText = `
                position: absolute;
                top: -50px;
                left: 50%;
                transform: translateX(-50%);
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #28a745;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: top 0.3s ease;
                z-index: 1000;
            `;
            document.body.appendChild(refreshIndicator);
            
            document.addEventListener('touchstart', function(e) {
                if (window.scrollY === 0 && !refreshing) {
                    touchStartY = e.touches[0].clientY;
                    startScrollTop = window.scrollY;
                }
            }, { passive: true });
            
            document.addEventListener('touchmove', function(e) {
                if (touchStartY > 0 && window.scrollY <= 0 && !refreshing) {
                    touchEndY = e.touches[0].clientY;
                    const distance = touchEndY - touchStartY;
                    
                    if (distance > 0) {
                        // Show pull indicator
                        refreshIndicator.style.top = `${Math.min(distance/2 - 50, 10)}px`;
                        
                        // Rotate the icon based on pull distance
                        const icon = refreshIndicator.querySelector('i');
                        const rotation = Math.min(distance / refreshThreshold * 360, 360);
                        icon.style.transform = `rotate(${rotation}deg)`;
                    }
                }
            }, { passive: true });
            
            document.addEventListener('touchend', function() {
                if (touchStartY > 0 && !refreshing) {
                    const distance = touchEndY - touchStartY;
                    
                    if (distance > minDistance) {
                        // Trigger refresh
                        refreshing = true;
                        refreshIndicator.style.top = '10px';
                        refreshIndicator.querySelector('i').classList.add('fa-spin');
                        
                        // Simulate refresh after 1.5 seconds
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    } else {
                        // Reset indicator
                        refreshIndicator.style.top = '-50px';
                    }
                    
                    // Reset values
                    touchStartY = 0;
                    touchEndY = 0;
                }
            }, { passive: true });
        }
        
        // Add quick filters for dashboard metrics
        function addQuickFilters() {
            const filterOptions = ['All Time', 'This Year', 'This Month', 'This Week'];
            const metricsContainers = document.querySelectorAll('.metrics-container, .portfolio-metrics');
            
            metricsContainers.forEach(container => {
                // Create filter buttons container
                const filterContainer = document.createElement('div');
                filterContainer.className = 'mobile-filters mb-2 d-flex overflow-auto pb-1';
                filterContainer.style.cssText = `
                    scrollbar-width: none;
                    -ms-overflow-style: none;
                `;
                
                // Add filter options
                filterOptions.forEach((option, index) => {
                    const filterBtn = document.createElement('button');
                    filterBtn.className = 'btn btn-sm ' + (index === 0 ? 'btn-primary' : 'btn-outline-primary');
                    filterBtn.textContent = option;
                    filterBtn.style.marginRight = '8px';
                    filterBtn.style.whiteSpace = 'nowrap';
                    filterContainer.appendChild(filterBtn);
                    
                    // Add click event
                    filterBtn.addEventListener('click', function() {
                        // Update active button
                        filterContainer.querySelectorAll('.btn').forEach(btn => {
                            btn.classList.remove('btn-primary');
                            btn.classList.add('btn-outline-primary');
                        });
                        this.classList.remove('btn-outline-primary');
                        this.classList.add('btn-primary');
                        
                        // Simulate filter change (in a real app, this would update the data)
                        const metrics = container.querySelectorAll('.metric-value');
                        metrics.forEach(metric => {
                            // Add loading effect
                            metric.style.opacity = '0.5';
                            setTimeout(() => {
                                metric.style.opacity = '1';
                            }, 500);
                        });
                    });
                });
                
                // Hide filter container's scrollbar
                filterContainer.innerHTML += `
                    <style>
                        .mobile-filters::-webkit-scrollbar {
                            display: none;
                        }
                    </style>
                `;
                
                // Add to the container before the metrics
                container.insertBefore(filterContainer, container.firstChild);
            });
        }
        
        // Initialize additional mobile features
        addPullToRefresh();
        addQuickFilters();
    }
});

/**
 * Dashboard Mobile Optimizations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on mobile
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // Add mobile-specific class
        document.body.classList.add('dashboard-mobile');
        
        // Auto-collapse some sections after a delay to improve initial loading experience
        setTimeout(() => {
            const sections = ['portfolioInsights', 'investmentDistribution'];
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
        
        // Toggle icon rotation on collapse toggle
        document.querySelectorAll('.section-toggle').forEach(toggle => {
            toggle.addEventListener('click', function() {
                const icon = this.querySelector('.fa-chevron-down');
                if (icon) {
                    if (this.getAttribute('aria-expanded') === 'true') {
                        icon.style.transform = 'rotate(0)';
                    } else {
                        icon.style.transform = 'rotate(-90deg)';
                    }
                }
            });
        });
        
        // Make investment cards more compact
        document.querySelectorAll('.investment-card').forEach(card => {
            card.classList.add('investment-card-mobile');
        });
        
        // Add touch-friendly styles to charts
        document.querySelectorAll('.chart-container').forEach(container => {
            container.style.height = '250px';
        });
        
        // Add max height to tables for scrolling
        document.querySelectorAll('table').forEach(table => {
            const wrapper = document.createElement('div');
            wrapper.classList.add('table-responsive');
            wrapper.style.maxHeight = '300px';
            
            // Only wrap if not already wrapped
            if (!table.parentElement.classList.contains('table-responsive')) {
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        const wasMobile = document.body.classList.contains('dashboard-mobile');
        const isMobileNow = window.innerWidth < 768;
        
        if (wasMobile !== isMobileNow) {
            // Refresh page when transitioning between mobile and desktop
            // to ensure proper layout
            location.reload();
        }
    });
});

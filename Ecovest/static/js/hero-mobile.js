/**
 * Mobile hero section collapsible fun                heroStats.forEach(stat => {
                    compactStatsContainer.innerHTML += `
                        <div class="compact-stat">
                            <i class="${stat.icon}"></i>
                            <h5>${stat.value}</h5>
                            <small>${stat.label}</small>
                        </div>
                    `;
                });y
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // Get all hero sections
        const heroSections = document.querySelectorAll('.hero');
        
        heroSections.forEach(hero => {
            // Create toggle button
            const toggleButton = document.createElement('button');
            toggleButton.className = 'hero-toggle';
            toggleButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
            toggleButton.setAttribute('aria-label', 'Toggle hero section');
            hero.appendChild(toggleButton);
            
            // Set initial state (not collapsed)
            let isCollapsed = false;
            
            // Create hero stats object for compact display
            const heroStats = [];
            
            // Collect stats from stat cards
            const statCards = hero.querySelectorAll('.stat-card');
            statCards.forEach(card => {
                const icon = card.querySelector('i')?.className;
                const value = card.querySelector('h3')?.textContent || card.querySelector('h4')?.textContent;
                const label = card.querySelector('p')?.textContent;
                
                if (icon && value && label) {
                    heroStats.push({ icon, value, label });
                }
            });
            
            // Add compact stats container for collapsed view
            if (heroStats.length > 0) {
                const compactStatsContainer = document.createElement('div');
                compactStatsContainer.className = 'compact-stats';
                
                heroStats.forEach(stat => {
                    compactStatsContainer.innerHTML += `
                        <div class="compact-stat">
                            <i class="${stat.icon}"></i>
                            <h5>${stat.value}</h5>
                            <small>${stat.label}</small>
                        </div>
                    `;
                });
                
                // Insert compact stats after hero title
                const heroTitle = hero.querySelector('.hero-title, h1');
                if (heroTitle) {
                    // Hide compact stats initially
                    compactStatsContainer.style.display = 'none';
                    
                    // Insert after the subtitle if it exists, otherwise after the title
                    const heroSubtitle = hero.querySelector('.hero-subtitle, p');
                    if (heroSubtitle) {
                        heroSubtitle.parentNode.insertBefore(compactStatsContainer, heroSubtitle.nextSibling);
                    } else {
                        heroTitle.parentNode.insertBefore(compactStatsContainer, heroTitle.nextSibling);
                    }
                }
            }
            
            // Store a reference to the compact stats container
            const compactStats = hero.querySelector('.compact-stats');
            
            // Toggle function
            function toggleHero() {
                isCollapsed = !isCollapsed;
                
                if (isCollapsed) {
                    // Collapse
                    hero.classList.add('hero-collapsed');
                    
                    // Hide stat cards
                    statCards.forEach(card => {
                        card.style.display = 'none';
                    });
                    
                    // Show compact stats
                    if (compactStats) {
                        compactStats.style.display = 'flex';
                    }
                    
                    // Hide any buttons or additional content
                    const buttons = hero.querySelectorAll('.btn:not(.hero-toggle)');
                    buttons.forEach(btn => {
                        btn.style.display = 'none';
                    });
                    
                    // Hide subtitle if screen is very small
                    if (window.innerWidth < 400) {
                        const subtitle = hero.querySelector('.hero-subtitle, p');
                        if (subtitle) {
                            subtitle.style.display = 'none';
                        }
                    }
                } else {
                    // Expand
                    hero.classList.remove('hero-collapsed');
                    
                    // Show stat cards with delay
                    setTimeout(() => {
                        statCards.forEach(card => {
                            card.style.display = '';
                        });
                    }, 300);
                    
                    // Hide compact stats
                    if (compactStats) {
                        compactStats.style.display = 'none';
                    }
                    
                    // Show any buttons or additional content
                    const buttons = hero.querySelectorAll('.btn:not(.hero-toggle)');
                    buttons.forEach(btn => {
                        btn.style.display = '';
                    });
                    
                    // Show subtitle
                    const subtitle = hero.querySelector('.hero-subtitle, p');
                    if (subtitle) {
                        subtitle.style.display = '';
                    }
                }
            }
            
            // Add click event to toggle button
            toggleButton.addEventListener('click', toggleHero);
            
            // Automatically collapse hero sections on dashboard and initiative list pages after page load
            setTimeout(() => {
                // Identify page type
                const isDashboard = document.querySelector('.dashboard-card');
                const isInitiativeList = document.querySelector('.filter-section');
                
                // Auto-collapse on appropriate pages
                if (isDashboard || isInitiativeList) {
                    toggleHero();
                }
            }, 1500);
        });
        
        // Listen for page orientation changes
        window.addEventListener('orientationchange', function() {
            setTimeout(() => {
                const heroes = document.querySelectorAll('.hero');
                heroes.forEach(hero => {
                    // If we're in portrait mode, make sure the heroes are collapsed
                    if (window.orientation === 0) { // Portrait mode
                        if (!hero.classList.contains('hero-collapsed')) {
                            hero.querySelector('.hero-toggle')?.click();
                        }
                    }
                });
            }, 500);
        });
    }
});

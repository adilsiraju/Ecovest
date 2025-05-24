/**
 * Page-specific mobile optimizations for Ecovest
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detect current page
    const currentPath = window.location.pathname;
    
    // Apply optimizations based on the current page
    if (currentPath.includes('/initiatives/')) {
        optimizeInitiativesPage();
    } else if (currentPath.includes('/dashboard/')) {
        optimizeDashboardPage();
    } else if (currentPath.includes('/profile/')) {
        optimizeProfilePage();
    } else if (currentPath === '/' || currentPath.includes('/landing/')) {
        optimizeLandingPage();
    } else if (currentPath.includes('/invest/')) {
        optimizeInvestmentPage();
    }
    
    // Initiative list and detail pages
    function optimizeInitiativesPage() {
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Make initiative cards more compact
            const cards = document.querySelectorAll('.initiative-card');
            cards.forEach(card => {
                card.classList.add('mb-3');
            });
            
            // Add truncate class to long descriptions
            const descriptions = document.querySelectorAll('.initiative-description');
            descriptions.forEach(desc => {
                desc.classList.add('truncate-mobile');
            });
            
            // Optimize impact charts
            const chartContainers = document.querySelectorAll('.chart-container');
            chartContainers.forEach(container => {
                container.style.height = '250px';
            });
        }
    }
    
    // Dashboard page
    function optimizeDashboardPage() {
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Simplify dashboard layout
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach(card => {
                card.classList.add('mb-3');
            });
            
            // Make charts responsive
            const chartContainers = document.querySelectorAll('.chart-container');
            chartContainers.forEach(container => {
                container.style.height = '250px';
            });
            
            // Add responsiveness to dashboard cards
            const dashboardCards = document.querySelectorAll('.dashboard-card');
            dashboardCards.forEach(card => {
                card.style.padding = '1.25rem';
            });
        }
    }
    
    // Profile page
    function optimizeProfilePage() {
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Center profile image
            const profileImg = document.querySelector('.profile-img');
            if (profileImg) {
                profileImg.style.margin = '0 auto 20px auto';
                profileImg.style.display = 'block';
            }
            
            // Make form elements more mobile friendly
            const formGroups = document.querySelectorAll('.form-group');
            formGroups.forEach(group => {
                group.style.marginBottom = '1rem';
            });
        }
    }
    
    // Landing page
    function optimizeLandingPage() {
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Adjust hero section
            const hero = document.querySelector('.hero');
            if (hero) {
                hero.style.padding = '3rem 0';
            }
            
            // Make feature cards more compact
            const featureCards = document.querySelectorAll('.feature-card');
            featureCards.forEach(card => {
                card.classList.add('mb-3');
            });
        }
    }
    
    // Investment page
    function optimizeInvestmentPage() {
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Simplify investment form
            const formGroups = document.querySelectorAll('.form-group');
            formGroups.forEach(group => {
                group.style.marginBottom = '1rem';
            });
            
            // Make impact previews more compact
            const impactCards = document.querySelectorAll('.impact-preview-card');
            impactCards.forEach(card => {
                card.style.padding = '1rem';
            });
        }
    }
});

/**
 * Mobile responsiveness utility functions for Profile page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;
    
    // Function to make profile sections collapsible on mobile
    function makeProfileSectionsCollapsible() {
        if (isMobile) {
            // Get all the profile sections with the class 'profile-section'
            const profileSections = document.querySelectorAll('.profile-section');
            
            profileSections.forEach((section, index) => {
                // Get the section title
                const title = section.querySelector('h3, h4, .section-title');
                if (!title) return;
                
                // Skip the first section (profile info), keep it expanded
                if (index === 0) return;
                
                // Create wrapper for collapsible content
                const wrapper = document.createElement('div');
                wrapper.className = 'mobile-profile-section';
                section.parentNode.insertBefore(wrapper, section);
                
                // Create header
                const header = document.createElement('div');
                header.className = 'mobile-profile-header';
                if (index > 1) header.classList.add('collapsed'); // Only first section expanded
                header.innerHTML = `
                    <span>${title.textContent}</span>
                    <i class="fas fa-chevron-down"></i>
                `;
                wrapper.appendChild(header);
                
                // Create collapsible body
                const body = document.createElement('div');
                body.className = 'collapse';
                if (index === 1) body.classList.add('show'); // Only first section expanded
                body.id = `profileSection${index}`;
                wrapper.appendChild(body);
                
                // Move section into body
                body.appendChild(section);
                
                // Initialize collapse behavior
                header.addEventListener('click', function() {
                    const isOpen = body.classList.contains('show');
                    
                    if (isOpen) {
                        body.classList.remove('show');
                        header.classList.add('collapsed');
                    } else {
                        body.classList.add('show');
                        header.classList.remove('collapsed');
                    }
                    
                    // Toggle the chevron icon
                    const icon = header.querySelector('i');
                    if (icon) {
                        icon.style.transform = isOpen ? 'rotate(-90deg)' : 'rotate(0deg)';
                    }
                });
            });
        }
    }
    
    // Function to optimize profile tabs for mobile
    function optimizeProfileTabs() {
        if (isMobile) {
            // Make sure tabs are scrollable horizontally
            const tabContainer = document.querySelector('.nav-tabs');
            if (tabContainer) {
                tabContainer.classList.add('profile-tabs');
                
                // Highlight active tab more prominently
                const activeTab = tabContainer.querySelector('.nav-link.active');
                if (activeTab) {
                    activeTab.style.fontWeight = '600';
                }
                
                // Make tabs more touch-friendly
                const tabs = tabContainer.querySelectorAll('.nav-link');
                tabs.forEach(tab => {
                    tab.style.padding = '0.6rem 1rem';
                });
            }
        }
    }
    
    // Function to make forms more mobile-friendly
    function optimizeProfileForms() {
        if (isMobile) {
            // Get all forms
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.classList.add('profile-form');
                
                // Make buttons full width
                const buttons = form.querySelectorAll('.btn');
                buttons.forEach(button => {
                    button.classList.add('w-100');
                    button.classList.add('mb-2');
                });
                
                // Add more spacing between form groups
                const formGroups = form.querySelectorAll('.form-group, .mb-3');
                formGroups.forEach(group => {
                    group.classList.add('mb-3');
                });
            });
        }
    }
    
    // Call all the functions
    makeProfileSectionsCollapsible();
    optimizeProfileTabs();
    optimizeProfileForms();
});

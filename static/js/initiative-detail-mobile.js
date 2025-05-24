/**
 * Mobile responsiveness utility functions for Initiative Detail page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;
    
    // Function to make detail sections collapsible on mobile
    function makeDetailSectionsCollapsible() {
        if (isMobile) {
            // Get all the detail sections
            const detailSections = document.querySelectorAll('.detail-section');
            
            detailSections.forEach((section, index) => {
                // Get the section title
                const title = section.querySelector('h3');
                if (!title) return;
                
                // Skip the first section, keep it expanded
                if (index === 0) return;
                
                // Create wrapper for collapsible content
                const wrapper = document.createElement('div');
                wrapper.className = 'mobile-collapsible';
                section.parentNode.insertBefore(wrapper, section);
                
                // Create header
                const header = document.createElement('div');
                header.className = 'mobile-collapsible-header';
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
                body.id = `section${index}`;
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
    
    // Function to add quick action buttons on mobile
    function addQuickActionButtons() {
        if (isMobile) {
            // Create container for quick actions
            const quickActions = document.createElement('div');
            quickActions.className = 'quick-action-buttons';
            
            // Add invest button
            const investButton = document.createElement('a');
            investButton.className = 'quick-action invest-button';
            investButton.href = document.querySelector('a[href*="invest_initiative"]')?.href || '#';
            investButton.innerHTML = '<i class="fas fa-wallet"></i>';
            investButton.title = 'Invest Now';
            quickActions.appendChild(investButton);
            
            // Add share button
            const shareButton = document.createElement('a');
            shareButton.className = 'quick-action share-button';
            shareButton.href = '#';
            shareButton.setAttribute('data-bs-toggle', 'modal');
            shareButton.setAttribute('data-bs-target', '#shareModal');
            shareButton.innerHTML = '<i class="fas fa-share-alt"></i>';
            shareButton.title = 'Share';
            quickActions.appendChild(shareButton);
            
            // Add to the page
            document.body.appendChild(quickActions);
        }
    }
    
    // Function to optimize the sidebar for mobile
    function optimizeSidebar() {
        if (isMobile) {
            // Move the "Important Information" card to the top of the sidebar
            const sidebar = document.querySelector('.sticky-sidebar');
            if (!sidebar) return;
            
            const importantInfoCard = sidebar.querySelector('.card:has(.info-list)');
            if (importantInfoCard && sidebar.firstChild !== importantInfoCard) {
                sidebar.insertBefore(importantInfoCard, sidebar.firstChild);
            }
            
            // Make the other sidebar cards collapsible
            const otherCards = sidebar.querySelectorAll('.card:not(:first-child)');
            otherCards.forEach((card, index) => {
                const title = card.querySelector('.card-title');
                if (!title) return;
                
                // Save original title text
                const titleText = title.textContent;
                
                // Create toggle button
                title.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center w-100">
                        <span>${titleText}</span>
                        <i class="fas fa-chevron-down"></i>
                    </div>
                `;
                title.style.cursor = 'pointer';
                
                // Create collapsible body
                const cardBody = card.querySelector('.card-body');
                const cardContent = cardBody.innerHTML;
                
                // Remove existing content except title
                Array.from(cardBody.children).forEach(child => {
                    if (child !== title) {
                        child.remove();
                    }
                });
                
                // Create collapsible div
                const collapsible = document.createElement('div');
                collapsible.className = 'collapse';
                collapsible.id = `sidebar-section-${index}`;
                collapsible.innerHTML = cardContent;
                
                // Remove the title from what we just copied
                const titleInCollapsible = collapsible.querySelector('.card-title');
                if (titleInCollapsible) {
                    titleInCollapsible.remove();
                }
                
                cardBody.appendChild(collapsible);
                
                // Set up toggle behavior
                title.addEventListener('click', function() {
                    const isOpen = collapsible.classList.contains('show');
                    
                    if (isOpen) {
                        collapsible.classList.remove('show');
                        title.querySelector('i').style.transform = 'rotate(-90deg)';
                    } else {
                        collapsible.classList.add('show');
                        title.querySelector('i').style.transform = 'rotate(0deg)';
                    }
                });
                
                // Start with it collapsed
                title.querySelector('i').style.transform = 'rotate(-90deg)';
            });
        }
    }
    
    // Call all the functions
    makeDetailSectionsCollapsible();
    addQuickActionButtons();
    optimizeSidebar();
    
    // Handle window resize events
    window.addEventListener('resize', function() {
        const wasMobile = document.body.classList.contains('is-mobile');
        const isMobileNow = window.innerWidth < 768;
        
        if (wasMobile !== isMobileNow) {
            // Reload the page if going between mobile and desktop
            // to reset the layout modifications
            window.location.reload();
        }
    });
});

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
            
            // Add toast notification container
            const toastContainer = document.createElement('div');
            toastContainer.className = 'mobile-toast';
            toastContainer.id = 'mobileToast';
            document.body.appendChild(toastContainer);
            
            // Add click event to show toast when share button is clicked (if no modal exists)
            shareButton.addEventListener('click', function(e) {
                const shareModal = document.querySelector('#shareModal');
                if (!shareModal) {
                    e.preventDefault();
                    showToast('Sharing options opened');
                    
                    // Try to use the Web Share API if available
                    if (navigator.share) {
                        const initiativeTitle = document.querySelector('h1')?.textContent || 'Check out this sustainable initiative';
                        const url = window.location.href;
                        
                        navigator.share({
                            title: initiativeTitle,
                            url: url
                        }).catch(console.error);
                    }
                }
            });
        }
    }
    
    // Function to show a toast notification
    function showToast(message, duration = 2000) {
        const toast = document.getElementById('mobileToast');
        if (toast) {
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, duration);
        }
    }
    
    // Function to optimize the sidebar for mobile
    function optimizeSidebarForMobile() {
        if (isMobile) {
            const sidebar = document.querySelector('.sticky-sidebar');
            if (sidebar) {
                // Create a mobile-friendly version of the sidebar
                const investButton = sidebar.querySelector('a.btn-primary');
                if (investButton) {
                    // Make it more prominent
                    investButton.classList.add('btn-lg', 'w-100', 'mb-3');
                }
                
                // Make cards collapsible if needed
                const cards = sidebar.querySelectorAll('.card');
                cards.forEach((card, index) => {
                    if (index > 0) { // Skip the first card
                        const cardTitle = card.querySelector('.card-title');
                        const cardBody = card.querySelector('.card-body');
                        
                        if (cardTitle && cardBody) {
                            // Create collapsible header
                            const header = document.createElement('div');
                            header.className = 'card-header d-flex justify-content-between align-items-center cursor-pointer';
                            header.innerHTML = `
                                <h5 class="mb-0">${cardTitle.textContent}</h5>
                                <i class="fas fa-chevron-down"></i>
                            `;
                            card.insertBefore(header, cardBody);
                            
                            // Remove the original title
                            cardTitle.remove();
                            
                            // Initialize collapse behavior
                            const collapse = new bootstrap.Collapse(cardBody, {
                                toggle: false
                            });
                            
                            // Collapse by default
                            collapse.hide();
                            
                            header.addEventListener('click', function() {
                                collapse.toggle();
                                this.querySelector('i').style.transform = 
                                    cardBody.classList.contains('show') ? 'rotate(0deg)' : 'rotate(-90deg)';
                            });
                        }
                    }
                });
            }
        }
    }
    
    // Function to optimize image gallery for mobile
    function optimizeGalleryForMobile() {
        if (isMobile) {
            const galleryContainer = document.querySelector('.initiative-images');
            if (galleryContainer) {
                // Create a scrollable gallery
                const gallery = document.createElement('div');
                gallery.className = 'initiative-gallery';
                
                // Get all images
                const images = galleryContainer.querySelectorAll('img');
                
                images.forEach(img => {
                    // Create gallery item
                    const item = document.createElement('div');
                    item.className = 'gallery-item';
                    
                    // Clone the image
                    const clonedImg = img.cloneNode(true);
                    item.appendChild(clonedImg);
                    
                    // Add to gallery
                    gallery.appendChild(item);
                    
                    // Add lightbox functionality
                    item.addEventListener('click', function() {
                        const src = clonedImg.src;
                        showImageLightbox(src);
                    });
                });
                
                // Replace the original container with the gallery
                galleryContainer.parentNode.replaceChild(gallery, galleryContainer);
            }
        }
    }
    
    // Function to show image lightbox
    function showImageLightbox(src) {
        // Create lightbox
        const lightbox = document.createElement('div');
        lightbox.className = 'mobile-lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-content">
                <img src="${src}" alt="Enlarged view">
                <button class="close-lightbox"><i class="fas fa-times"></i></button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(lightbox);
        
        // Prevent scrolling
        document.body.style.overflow = 'hidden';
        
        // Add close event
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox || e.target.closest('.close-lightbox')) {
                document.body.removeChild(lightbox);
                document.body.style.overflow = '';
            }
        });
    }
    
    // Initialize mobile optimizations
    if (isMobile) {
        makeDetailSectionsCollapsible();
        addQuickActionButtons();
        optimizeSidebarForMobile();
        optimizeGalleryForMobile();
        
        // Add swipe navigation between tabs if tabs exist
        const tabs = document.querySelectorAll('.nav-tabs .nav-link');
        if (tabs.length > 0) {
            let startX, endX;
            const tabsContainer = document.querySelector('.tab-content');
            
            if (tabsContainer) {
                tabsContainer.addEventListener('touchstart', function(e) {
                    startX = e.touches[0].clientX;
                });
                
                tabsContainer.addEventListener('touchend', function(e) {
                    endX = e.changedTouches[0].clientX;
                    
                    const diff = startX - endX;
                    const activeTabIndex = Array.from(tabs).findIndex(tab => 
                        tab.classList.contains('active'));
                    
                    // Swipe left to right (previous tab)
                    if (diff < -50 && activeTabIndex > 0) {
                        tabs[activeTabIndex - 1].click();
                    }
                    // Swipe right to left (next tab)
                    else if (diff > 50 && activeTabIndex < tabs.length - 1) {
                        tabs[activeTabIndex + 1].click();
                    }
                });
            }
        }
    }
});

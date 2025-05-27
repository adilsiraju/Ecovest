/**
 * Enhanced Initiative List page functionality
 * Part of the Ecovest 10x UX improvements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Enhanced details toggle functionality with animations
    const detailsToggles = document.querySelectorAll('.details-toggle');
    detailsToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const initiativeId = this.dataset.initiative;
            const detailsEl = document.getElementById(`details-${initiativeId}`);
            const toggleText = this.querySelector('.toggle-text');
            const toggleIcon = this.querySelector('i');
            
            detailsEl.classList.toggle('show');
            
            if (detailsEl.classList.contains('show')) {
                toggleText.textContent = 'Hide details';
                toggleIcon.classList.replace('fa-chevron-down', 'fa-chevron-up');
            } else {
                toggleText.textContent = 'Show details';
                toggleIcon.classList.replace('fa-chevron-up', 'fa-chevron-down');
            }
        });
    });
    
    // View toggle functionality with smooth transitions
    const viewToggles = document.querySelectorAll('.view-toggle-btn');
    const initiativesContainer = document.getElementById('initiatives-container');
      // Apply saved view preference if exists
    const savedView = localStorage.getItem('initiativeViewPreference');
    if (savedView) {
        if (savedView === 'compact') {
            initiativesContainer.classList.add('compact-view');
            document.querySelectorAll('.initiative-item').forEach(item => {
                // Force full width in compact view
                item.classList.remove('col-lg-3', 'col-md-4', 'col-sm-6');
                item.classList.add('col-12');
            });
            viewToggles.forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.view === 'compact') {
                    btn.classList.add('active');
                }
            });
        }
    }
    
    viewToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            // Update active state
            viewToggles.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Change view with animation
            const viewType = this.dataset.view;
            if (viewType === 'compact') {
                initiativesContainer.classList.add('compact-view');
                localStorage.setItem('initiativeViewPreference', 'compact');
            } else {
                initiativesContainer.classList.remove('compact-view');
                localStorage.setItem('initiativeViewPreference', 'grid');
            }
        });
    });
      // Quick View Modal functionality
    const quickViewBtns = document.querySelectorAll('.quick-view-btn');
    const quickViewModal = new bootstrap.Modal(document.getElementById('quickViewModal'), {});
    
    quickViewBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const initiativeId = this.dataset.initiative;
            const card = this.closest('.initiative-card');
            
            // Extract data from the card to populate the modal
            const title = card.querySelector('.initiative-title').textContent;
            const image = card.querySelector('.initiative-image').src;
            const description = card.querySelector('.initiative-description').textContent;
            const currentAmount = card.querySelector('.funding-amount').textContent;
            const goalAmount = card.querySelector('.funding-goal').textContent;
            const progressPercent = card.querySelector('.progress-bar').style.width;
            const progressText = card.querySelector('.d-flex.justify-content-between.text-muted.small span:last-child').textContent;
            
            // Set data in the modal
            document.getElementById('quickViewTitle').textContent = title;
            document.getElementById('quickViewImage').src = image;
            document.getElementById('quickViewDescription').textContent = description;
            document.getElementById('quickViewCurrentAmount').textContent = currentAmount;
            document.getElementById('quickViewGoalAmount').textContent = goalAmount;
            document.getElementById('quickViewProgressBar').style.width = progressPercent;
            document.getElementById('quickViewProgressPercent').textContent = progressText;    viewToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            // Update active state
            viewToggles.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Change view with animation
            const viewType = this.dataset.view;
            if (viewType === 'compact') {
                initiativesContainer.classList.add('compact-view');
                localStorage.setItem('initiativeViewPreference', 'compact');
            } else {
                initiativesContainer.classList.remove('compact-view');
                localStorage.setItem('initiativeViewPreference', 'grid');
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
            const detailsSection = card.querySelector('.initiative-details');
            if (detailsSection) {
                const impactStats = detailsSection.querySelectorAll('.impact-stat');
                impactStats.forEach(stat => {
                    const icon = stat.querySelector('i').className;
                    const value = stat.querySelector('.impact-value') ? 
                        stat.querySelector('.impact-value').textContent : 
                        stat.textContent.trim();
                    const title = stat.getAttribute('title');
                    
                    impactData.push(`
                        <div class="col-4">
                            <div class="text-center p-2 bg-light rounded">
                                <i class="${icon} text-success"></i>
                                <div class="fw-bold">${value}</div>
                                <div class="small text-muted">${title}</div>
                            </div>
                        </div>
                    `);
                });
            }
            
            // Add any additional metadata from details section
            if (detailsSection) {
                const detailsRow = detailsSection.querySelector('.row.g-2');
                if (detailsRow) {
                    const detailCols = detailsRow.querySelectorAll('.col-6');
                    detailCols.forEach(col => {
                        const label = col.querySelector('.text-muted').textContent.trim();
                        const value = col.querySelector('.fw-bold').textContent.trim();
                        metadata.push(`
                            <div class="col-6 mb-2">
                                <div class="text-muted small">${label}</div>
                                <div class="fw-bold">${value}</div>
                            </div>
                        `);
                    });
                }
            }
            
            document.getElementById('quickViewMetadata').innerHTML = metadata.join('');
            document.getElementById('quickViewImpact').innerHTML = impactData.length > 0 ? 
                `<h6 class="fw-bold mb-2">Impact per ₹1,000</h6><div class="row gx-2">${impactData.join('')}</div>` : '';
            
            // Set the learn more link
            document.getElementById('quickViewLearnMore').href = `/initiatives/${initiativeId}/`;
            
            // Show the modal
            const quickViewModal = new bootstrap.Modal(document.getElementById('quickViewModal'));
            quickViewModal.show();
        });
    });
    
    // Lazy load images for better performance
    if ('IntersectionObserver' in window) {
        const imgOptions = {
            threshold: 0.1,
            rootMargin: "0px 0px 200px 0px"
        };
        
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.classList.add('fade-in');
                    }
                    observer.unobserve(img);
                }
            });
        }, imgOptions);
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            imgObserver.observe(img);
        });
    }
    
    // Animation on scroll for initiative cards
    if ('IntersectionObserver' in window) {
        const animOptions = {
            threshold: 0.15,
            rootMargin: "0px 0px -50px 0px"
        };
        
        const animObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const card = entry.target;
                    setTimeout(() => {
                        card.classList.add('fade-in-up', 'visible');
                    }, 100);
                    observer.unobserve(card);
                }
            });
        }, animOptions);
        
        const cards = document.querySelectorAll('.initiative-item:not(.fade-in-up)');
        cards.forEach(card => {
            card.style.opacity = '0';
            animObserver.observe(card);
        });
    }
    
    // Skeleton loader functionality for better perceived performance
    function showSkeletonLoaders() {
        const container = document.getElementById('initiatives-container');
        container.innerHTML = '';
        
        for (let i = 0; i < 6; i++) {
            const skeletonHTML = `
                <div class="col-lg-4 col-md-6">
                    <div class="skeleton-card">
                        <div class="skeleton skeleton-img"></div>
                        <div style="padding: 1.5rem;">
                            <div class="skeleton skeleton-title"></div>
                            <div class="skeleton skeleton-text sm"></div>
                            <div class="skeleton skeleton-text lg"></div>
                            <div class="skeleton skeleton-text md"></div>
                            <div style="margin: 1rem 0;"></div>
                            <div class="skeleton skeleton-text lg"></div>
                            <div class="skeleton" style="height: 8px; margin: 0.5rem 0;"></div>
                            <div class="d-flex justify-content-between">
                                <div class="skeleton skeleton-text sm"></div>
                                <div class="skeleton skeleton-text sm"></div>
                            </div>
                            <div style="margin: 1rem 0;"></div>
                            <div class="skeleton" style="height: 40px; border-radius: 12px;"></div>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += skeletonHTML;
        }
    }
    
    // Filter form submission loading effect
    const filterFormEl = document.querySelector('.filter-section form');
    if (filterFormEl) {
        filterFormEl.addEventListener('submit', function(e) {
            showSkeletonLoaders();
        });
    }
    
    // Smooth scroll to top for pagination
    const paginationLinks = document.querySelectorAll('.pagination .page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show skeleton loaders first
            showSkeletonLoaders();
            
            // Smooth scroll to top of initiatives
            const filterSection = document.querySelector('.filter-section');
            filterSection.scrollIntoView({ behavior: 'smooth' });
            
            // Then navigate after a short delay
            setTimeout(() => {
                window.location.href = this.getAttribute('href');
            }, 500);
        });
    });
    
    // Interactive hover effects for better engagement
    const initiativeCards = document.querySelectorAll('.initiative-card');
    initiativeCards.forEach(card => {
        const image = card.querySelector('.initiative-image');
        const titleArea = card.querySelector('.initiative-title-area');
        
        // Subtle parallax on mouse move
        card.addEventListener('mousemove', function(e) {
            if (window.innerWidth < 992) return; // Skip on smaller screens
            
            const cardRect = card.getBoundingClientRect();
            const cardCenterX = cardRect.left + cardRect.width / 2;
            const cardCenterY = cardRect.top + cardRect.height / 2;
            
            const mouseX = e.clientX - cardCenterX;
            const mouseY = e.clientY - cardCenterY;
            
            const moveX = (mouseX / cardRect.width) * 10;
            const moveY = (mouseY / cardRect.height) * 10;
            
            if (image) {
                image.style.transform = `translate(${moveX * -0.5}px, ${moveY * -0.5}px) scale(1.05)`;
            }
            
            if (titleArea) {
                titleArea.style.transform = `translate(${moveX * 0.2}px, ${moveY * 0.2}px)`;
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (image) {
                image.style.transform = '';
            }
            
            if (titleArea) {
                titleArea.style.transform = '';
            }
        });
    });
    
    // Highlight active filters and sort selections
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('category') || urlParams.has('status') || urlParams.has('sort')) {
        const formSelects = document.querySelectorAll('.filter-form-container select');
        formSelects.forEach(select => {
            const paramValue = urlParams.get(select.name);
            if (paramValue) {
                select.closest('.form-group').classList.add('has-value');
                const label = select.previousElementSibling;
                if (label) {
                    label.classList.add('text-success');
                }
            }
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Category color mapping utility
function getCategoryColorClass(category) {
    const categoryMap = {
        'Renewable Energy': 'renewable-energy',
        'Recycling': 'recycling',
        'Emission Control': 'emission-control',
        'Water Conservation': 'water-conservation',
        'Reforestation': 'reforestation',
        'Sustainable Agriculture': 'sustainable-agriculture',
        'Clean Transportation': 'clean-transportation',
        'Waste Management': 'waste-management',
        'Green Technology': 'green-technology',
        'Ocean Conservation': 'ocean-conservation'
    };
    
    return categoryMap[category] || 'default';
}

// Progress bar animation
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

// Initialize progress bar animations
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(animateProgressBars, 500);
});

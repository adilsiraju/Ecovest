/**
 * Main mobile utilities for Ecovest platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;
    
    // Add mobile-specific class to body
    if (isMobile) {
        document.body.classList.add('is-mobile');
    }
    
    // Add page loader for better mobile experience
    function addPageLoader() {
        // Create loader element
        const loader = document.createElement('div');
        loader.className = 'page-loader';
        loader.innerHTML = `
            <div class="loader-content">
                <i class="fas fa-leaf fa-spin"></i>
                <p>Loading Ecovest...</p>
            </div>
        `;
        
        // Add to body
        document.body.appendChild(loader);
        
        // Hide loader after page is fully loaded
        window.addEventListener('load', function() {
            setTimeout(() => {
                loader.classList.add('page-loader-fade');
                setTimeout(() => {
                    loader.remove();
                }, 500);
            }, 300);
        });
    }
    
    // Call the loader function
    addPageLoader();
    
    // Function to limit paragraph length on mobile
    function truncateTextOnMobile() {
        if (isMobile) {
            const longDescriptions = document.querySelectorAll('.truncate-mobile');
            longDescriptions.forEach(element => {
                const text = element.textContent;
                if (text.length > 120) {
                    const truncated = text.substring(0, 120) + '...';
                    element.textContent = truncated;
                    
                    // Add "Read more" button
                    const readMore = document.createElement('a');
                    readMore.textContent = 'Read more';
                    readMore.href = '#';
                    readMore.classList.add('btn-link', 'mt-2', 'd-block');
                    readMore.addEventListener('click', function(e) {
                        e.preventDefault();
                        element.textContent = text;
                        this.style.display = 'none';
                    });
                    
                    element.parentNode.appendChild(readMore);
                }
            });
        }
    }
    
    // Optimize image loading on mobile
    function optimizeImages() {
        if (isMobile) {
            const images = document.querySelectorAll('img[data-mobile-src]');
            images.forEach(img => {
                if (img.getAttribute('data-mobile-src')) {
                    img.src = img.getAttribute('data-mobile-src');
                }
            });
        }
    }
    
    // Adjust table layouts on mobile
    function makeTables() {
        if (isMobile) {
            const tables = document.querySelectorAll('table:not(.table-responsive)');
            tables.forEach(table => {
                const wrapper = document.createElement('div');
                wrapper.classList.add('table-responsive');
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            });
        }
    }
    
    // Add back-to-top button for long pages
    function addBackToTop() {
        const footer = document.querySelector('footer');
        if (!footer) return;
        
        const backToTop = document.createElement('button');
        backToTop.classList.add('back-to-top');
        backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
        backToTop.style.display = 'none';
        document.body.appendChild(backToTop);
        
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.style.display = 'block';
            } else {
                backToTop.style.display = 'none';
            }
        });
    }
    
    // Enhanced mobile navbar functionality
    function enhanceMobileNavbar() {
        const navbar = document.querySelector('.navbar-custom');
        const navbarCollapse = document.getElementById('navbarNav');
        const navbarToggler = document.querySelector('.navbar-toggler');
        
        if (navbar && navbarCollapse) {
            // Create backdrop for closing navbar when clicking outside
            const backdrop = document.createElement('div');
            backdrop.className = 'navbar-collapse-backdrop';
            document.body.appendChild(backdrop);
            
            // Close navbar when clicking on backdrop
            backdrop.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    // Use Bootstrap's collapse API to properly close the navbar
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            });
            
            // Show/hide backdrop when navbar is toggled
            navbarCollapse.addEventListener('show.bs.collapse', function() {
                backdrop.classList.add('show');
                document.body.style.overflow = 'hidden'; // Prevent scrolling
            });
            
            navbarCollapse.addEventListener('hide.bs.collapse', function() {
                backdrop.classList.remove('show');
                document.body.style.overflow = ''; // Enable scrolling
            });
            
            // Close navbar when a nav-link is clicked
            const navLinks = navbar.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    if (navbarCollapse.classList.contains('show') && window.innerWidth < 992) {
                        const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                        bsCollapse.hide();
                    }
                });
            });
            
            // Close navbar when ESC key is pressed
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            });
            
            // Fix issue with navbar toggler animation
            if (navbarToggler) {
                navbarToggler.addEventListener('click', function() {
                    // Toggle animation will be handled by aria-expanded state via CSS
                });
            }
        }
    }
    
    // Back to Top button functionality
    const backToTopBtn = document.getElementById('backToTopBtn');
    
    if (backToTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        // Scroll to top when clicked
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Improve form elements for touch devices
    if ('ontouchstart' in document.documentElement) {
        // Increase clickable area for checkboxes and radio buttons
        document.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(input => {
            const label = input.closest('label') || input.parentElement.querySelector('label[for="' + input.id + '"]');
            if (label) {
                label.style.padding = '10px 0';
                label.style.display = 'inline-block';
            }
        });
        
        // Add touch feedback to buttons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('touchstart', function() {
                this.classList.add('btn-touch');
            });
            btn.addEventListener('touchend', function() {
                this.classList.remove('btn-touch');
            });
        });
    }
    
    // Add page transition effect
    const content = document.querySelector('#main-content') || document.querySelector('main') || document.body;
    if (content) {
        // Add fade-in effect
        content.style.opacity = '0';
        content.style.transition = 'opacity 0.3s ease';
        
        // Fade in content after a slight delay
        setTimeout(() => {
            content.style.opacity = '1';
        }, 50);
    }
    
    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        // Refresh charts if they exist
        if (typeof Chart !== 'undefined') {
            document.querySelectorAll('canvas').forEach(canvas => {
                const chart = Chart.getChart(canvas);
                if (chart) {
                    setTimeout(() => {
                        chart.resize();
                    }, 300);
                }
            });
        }
    });
    
    // Apply all mobile optimizations
    truncateTextOnMobile();
    optimizeImages();
    makeTables();
    addBackToTop();
    enhanceMobileNavbar();
    
    // Handle window resize events
    window.addEventListener('resize', function() {
        const wasMobile = document.body.classList.contains('is-mobile');
        const isMobileNow = window.innerWidth < 768;
        
        if (wasMobile !== isMobileNow) {
            if (isMobileNow) {
                document.body.classList.add('is-mobile');
            } else {
                document.body.classList.remove('is-mobile');
                // Reload the page to reset desktop view
                // Uncomment if needed:
                // window.location.reload();
            }
        }
    });
});

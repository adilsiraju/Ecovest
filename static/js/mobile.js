/**
 * Mobile responsiveness utility functions for Ecovest
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
    
    // Apply all mobile optimizations
    truncateTextOnMobile();
    optimizeImages();
    makeTables();
    addBackToTop();
    
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

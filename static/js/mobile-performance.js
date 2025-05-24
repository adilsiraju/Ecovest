/**
 * Performance optimizations for mobile devices
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // Lazy load images
        function lazyLoadImages() {
            const images = document.querySelectorAll('img:not([loading="lazy"])');
            images.forEach(img => {
                if (!img.hasAttribute('loading')) {
                    img.setAttribute('loading', 'lazy');
                }
            });
        }
        
        // Defer non-critical JavaScript
        function deferNonCriticalJS() {
            const scripts = document.querySelectorAll('script[data-defer="true"]');
            scripts.forEach(script => {
                script.setAttribute('defer', '');
            });
        }
        
        // Optimize font loading
        function optimizeFontLoading() {
            // Add font-display: swap to improve font loading behavior
            const style = document.createElement('style');
            style.textContent = `
                @font-face {
                    font-display: swap !important;
                }
            `;
            document.head.appendChild(style);
        }
        
        // Optimize scrolling performance
        function optimizeScrolling() {
            // Add passive event listeners for touch events
            document.addEventListener('touchstart', function() {}, { passive: true });
            document.addEventListener('touchmove', function() {}, { passive: true });
            
            // Disable heavy animations while scrolling
            let scrollTimeout;
            let isScrolling = false;
            
            window.addEventListener('scroll', function() {
                if (!isScrolling) {
                    document.body.classList.add('is-scrolling');
                    isScrolling = true;
                }
                
                clearTimeout(scrollTimeout);
                
                scrollTimeout = setTimeout(function() {
                    document.body.classList.remove('is-scrolling');
                    isScrolling = false;
                }, 200);
            }, { passive: true });
        }
        
        // Initialize performance optimizations
        lazyLoadImages();
        deferNonCriticalJS();
        optimizeFontLoading();
        optimizeScrolling();
    }
});

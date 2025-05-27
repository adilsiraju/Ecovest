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
        
        // Optimize images specifically
        function optimizeImageSizes() {
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                // Set sizes attribute for responsive images
                if (img.hasAttribute('srcset') && !img.hasAttribute('sizes')) {
                    img.setAttribute('sizes', '(max-width: 576px) 100vw, (max-width: 768px) 50vw, 33vw');
                }
                
                // Ensure all images have alt text for accessibility
                if (!img.hasAttribute('alt')) {
                    img.setAttribute('alt', '');
                }
            });
        }
        
        // Pre-connect to third-party domains
        function addPreconnect() {
            const domains = [
                'https://cdn.jsdelivr.net',
                'https://cdnjs.cloudflare.com'
            ];
            
            domains.forEach(domain => {
                const link = document.createElement('link');
                link.rel = 'preconnect';
                link.href = domain;
                document.head.appendChild(link);
                
                const dnsLink = document.createElement('link');
                dnsLink.rel = 'dns-prefetch';
                dnsLink.href = domain;
                document.head.appendChild(dnsLink);
            });
        }
        
        // Reduce DOM size by removing comments
        function cleanDOMComments() {
            const commentNodes = [];
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_COMMENT,
                null,
                false
            );
            
            while (walker.nextNode()) {
                commentNodes.push(walker.currentNode);
            }
            
            commentNodes.forEach(node => {
                node.parentNode.removeChild(node);
            });
        }
        
        // Initialize performance optimizations
        lazyLoadImages();
        deferNonCriticalJS();
        optimizeFontLoading();
        optimizeScrolling();
        optimizeImageSizes();
        addPreconnect();
        cleanDOMComments();
        
        // Add a page loading indicator
        const pageLoader = document.createElement('div');
        pageLoader.className = 'page-loader';
        pageLoader.innerHTML = `
            <div class="loader-content">
                <i class="fas fa-leaf"></i>
                <p>Loading Ecovest...</p>
            </div>
        `;
        document.body.appendChild(pageLoader);
        
        // Remove loader after page is fully loaded
        window.addEventListener('load', function() {
            pageLoader.classList.add('page-loader-fade');
            setTimeout(() => {
                pageLoader.remove();
            }, 500);
        });
    }
});

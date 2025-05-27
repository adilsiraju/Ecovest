/**
 * Mobile accessibility enhancements for Ecovest
 */

document.addEventListener('DOMContentLoaded', function() {
    // Only run on mobile devices
    if (window.innerWidth < 768) {
        // Improve touch target sizes
        function improveTouchTargets() {
            // Links that are too small
            const smallLinks = Array.from(document.querySelectorAll('a')).filter(link => {
                const rect = link.getBoundingClientRect();
                return (rect.width < 44 || rect.height < 44) && 
                       !link.querySelector('img') && // Exclude image links
                       link.textContent.trim() !== ''; // Exclude empty links
            });
            
            smallLinks.forEach(link => {
                // Add padding to increase touch target
                link.style.padding = '10px';
                link.style.display = 'inline-block';
            });
            
            // Small buttons
            const smallButtons = Array.from(document.querySelectorAll('button')).filter(button => {
                const rect = button.getBoundingClientRect();
                return (rect.width < 44 || rect.height < 44);
            });
            
            smallButtons.forEach(button => {
                button.style.minWidth = '44px';
                button.style.minHeight = '44px';
            });
            
            // Form controls
            document.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(input => {
                const label = input.closest('label') || document.querySelector(`label[for="${input.id}"]`);
                if (label) {
                    label.style.minHeight = '44px';
                    label.style.display = 'flex';
                    label.style.alignItems = 'center';
                }
            });
        }
        
        // Fix font sizes for readability
        function fixFontSizes() {
            // Ensure minimum font size for readability
            const minBodyFontSize = 16; // pixels
            const bodyFontSize = parseFloat(window.getComputedStyle(document.body).fontSize);
            
            if (bodyFontSize < minBodyFontSize) {
                document.body.style.fontSize = minBodyFontSize + 'px';
            }
            
            // Find and fix small text
            document.querySelectorAll('p, span, li, td, th, button, a, label, input, select').forEach(el => {
                const fontSize = parseFloat(window.getComputedStyle(el).fontSize);
                if (fontSize < 14) {
                    el.style.fontSize = '14px';
                }
            });
        }
        
        // Improve contrast for accessibility
        function improveContrast() {
            // Add a slight text shadow to text on image backgrounds
            document.querySelectorAll('.hero, .image-bg, .banner, [class*="bg-"]').forEach(el => {
                const textElements = el.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, button');
                textElements.forEach(text => {
                    // Only add if not already styled
                    if (!text.style.textShadow) {
                        text.style.textShadow = '0 1px 2px rgba(0,0,0,0.4)';
                    }
                });
            });
        }
        
        // Add focus indicators for keyboard navigation
        function enhanceFocusIndicators() {
            // Create a style element for focus styles
            const style = document.createElement('style');
            style.textContent = `
                a:focus, button:focus, input:focus, select:focus, textarea:focus, [tabindex]:focus {
                    outline: 3px solid #4c9e62 !important;
                    outline-offset: 2px !important;
                }
            `;
            document.head.appendChild(style);
        }
        
        // Simplify page for better performance on low-end devices
        function simplifyForPerformance() {
            // Disable complex animations
            document.querySelectorAll('.animate, [data-animation], .animated').forEach(el => {
                el.style.animation = 'none';
                el.style.transition = 'none';
            });
            
            // Simplify gradients and shadows on low-end devices
            if (navigator.deviceMemory && navigator.deviceMemory < 4) {
                document.querySelectorAll('[class*="shadow"], [style*="box-shadow"]').forEach(el => {
                    el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                });
                
                document.querySelectorAll('[style*="gradient"]').forEach(el => {
                    // Simplify to solid color where possible
                    el.style.background = '#28a745';
                });
            }
        }
        
        // Initialize accessibility improvements
        improveTouchTargets();
        fixFontSizes();
        improveContrast();
        enhanceFocusIndicators();
        
        // Only apply performance simplifications on lower-end devices
        if (navigator.deviceMemory && navigator.deviceMemory < 4 || 
            navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
            simplifyForPerformance();
        }
        
        // Listen for orientation changes and re-apply
        window.addEventListener('orientationchange', function() {
            setTimeout(() => {
                improveTouchTargets();
            }, 300);
        });
    }
});

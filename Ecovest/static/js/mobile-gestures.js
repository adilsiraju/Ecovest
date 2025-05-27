/**
 * Mobile gesture navigation for Ecovest
 */

document.addEventListener('DOMContentLoaded', function() {
    // Only apply on mobile devices
    if (window.innerWidth < 768) {
        // Back navigation with edge swipe (right to left)
        let touchStartX = 0;
        let touchEndX = 0;
        const swipeThreshold = 100; // Minimum distance for a swipe
        const edgeThreshold = 30; // Maximum distance from edge to start swipe
        
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        document.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            
            // Check if it's a right-to-left swipe from the edge
            if (touchStartX < edgeThreshold && touchEndX - touchStartX > swipeThreshold) {
                // Show back navigation hint
                showNavigationHint('right');
                
                // Go back in history
                if (window.history.length > 1) {
                    window.history.back();
                }
            }
            
            // Check if it's a left-to-right swipe from the edge
            if (touchStartX > window.innerWidth - edgeThreshold && touchStartX - touchEndX > swipeThreshold) {
                // Show forward navigation hint
                showNavigationHint('left');
                
                // Go forward in history
                window.history.forward();
            }
        }, { passive: true });
        
        // Function to show navigation hint
        function showNavigationHint(direction) {
            // Create hint element if it doesn't exist
            let hint = document.getElementById('nav-hint');
            if (!hint) {
                hint = document.createElement('div');
                hint.id = 'nav-hint';
                hint.style.cssText = `
                    position: fixed;
                    top: 50%;
                    transform: translateY(-50%);
                    background: rgba(0, 0, 0, 0.7);
                    color: white;
                    padding: 10px 15px;
                    border-radius: 30px;
                    z-index: 10000;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    pointer-events: none;
                    font-size: 14px;
                `;
                document.body.appendChild(hint);
            }
            
            // Set position and text based on direction
            if (direction === 'right') {
                hint.style.left = '20px';
                hint.style.right = 'auto';
                hint.innerHTML = '<i class="fas fa-arrow-left mr-2"></i> Back';
            } else {
                hint.style.right = '20px';
                hint.style.left = 'auto';
                hint.innerHTML = 'Forward <i class="fas fa-arrow-right ml-2"></i>';
            }
            
            // Show and hide the hint
            hint.style.opacity = '1';
            setTimeout(() => {
                hint.style.opacity = '0';
            }, 1000);
        }
        
        // Add pull-to-refresh on specific pages
        const refreshablePaths = ['/dashboard/', '/initiatives/', '/profile/'];
        const currentPath = window.location.pathname;
        
        if (refreshablePaths.includes(currentPath)) {
            let pullStartY = 0;
            let pullMoveY = 0;
            let pullRefreshThreshold = 150;
            let pullRefreshElement;
            let isPulling = false;
            
            // Create pull-to-refresh element
            pullRefreshElement = document.createElement('div');
            pullRefreshElement.className = 'pull-refresh-element';
            pullRefreshElement.innerHTML = '<i class="fas fa-sync-alt"></i><span>Pull to refresh</span>';
            pullRefreshElement.style.cssText = `
                position: fixed;
                top: -60px;
                left: 0;
                right: 0;
                height: 60px;
                background: #28a745;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s ease;
                z-index: 9999;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                transform: translateY(-100%);
            `;
            document.body.appendChild(pullRefreshElement);
            
            // Touch events for pull-to-refresh
            document.addEventListener('touchstart', function(e) {
                // Only if we're at the top of the page
                if (window.scrollY === 0) {
                    pullStartY = e.touches[0].clientY;
                    isPulling = true;
                }
            }, { passive: true });
            
            document.addEventListener('touchmove', function(e) {
                if (!isPulling) return;
                
                pullMoveY = e.touches[0].clientY;
                let pullDistance = pullMoveY - pullStartY;
                
                // If pulling down
                if (pullDistance > 0) {
                    // Restrict pull distance with diminishing returns
                    let pullOffset = Math.min(pullDistance * 0.5, pullRefreshThreshold);
                    
                    // Update pull indicator
                    pullRefreshElement.style.transform = `translateY(${pullOffset}px)`;
                    
                    // Update text based on threshold
                    if (pullOffset >= pullRefreshThreshold) {
                        pullRefreshElement.querySelector('span').textContent = 'Release to refresh';
                    } else {
                        pullRefreshElement.querySelector('span').textContent = 'Pull to refresh';
                    }
                    
                    // Rotate icon based on pull distance
                    const rotation = Math.min(pullOffset / pullRefreshThreshold * 360, 360);
                    pullRefreshElement.querySelector('i').style.transform = `rotate(${rotation}deg)`;
                }
            }, { passive: true });
            
            document.addEventListener('touchend', function() {
                if (!isPulling) return;
                
                const pullDistance = pullMoveY - pullStartY;
                
                // If pulled past threshold, refresh the page
                if (pullDistance > pullRefreshThreshold) {
                    // Show loading animation
                    pullRefreshElement.querySelector('span').textContent = 'Refreshing...';
                    pullRefreshElement.querySelector('i').classList.add('fa-spin');
                    
                    // Reload after animation
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Reset the pull indicator
                    pullRefreshElement.style.transform = 'translateY(-100%)';
                }
                
                // Reset pull state
                isPulling = false;
                pullStartY = 0;
                pullMoveY = 0;
            }, { passive: true });
        }
    }
});

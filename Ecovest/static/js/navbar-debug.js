// Debug script for navbar responsiveness
document.addEventListener('DOMContentLoaded', function() {
    function logNavbarState() {
        const navbarButtons = document.querySelector('.navbar-buttons');
        const windowWidth = window.innerWidth;
        
        if (navbarButtons) {
            const computedStyle = window.getComputedStyle(navbarButtons);
            const flexDirection = computedStyle.flexDirection;
            
            console.log('=== Navbar Debug ===');
            console.log('Window width:', windowWidth);
            console.log('Flex direction:', flexDirection);
            console.log('Should be:', windowWidth >= 992 ? 'row (desktop)' : 'column (mobile)');
            
            const buttons = navbarButtons.querySelectorAll('.btn');
            buttons.forEach((btn, index) => {
                const btnStyle = window.getComputedStyle(btn);
                console.log(`Button ${index + 1}:`, {
                    width: btnStyle.width,
                    marginBottom: btnStyle.marginBottom,
                    padding: btnStyle.padding
                });
            });
            console.log('==================');
        }
    }
    
    // Log initial state
    logNavbarState();
    
    // Log on resize
    window.addEventListener('resize', function() {
        setTimeout(logNavbarState, 100);
    });
});

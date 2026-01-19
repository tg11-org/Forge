// TG11 Forge - Theme and Accessibility JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Theme Picker Functionality
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            // Cycle through themes: light -> dark -> high-contrast -> light
            if (body.classList.contains('dark-theme')) {
                body.classList.remove('dark-theme');
                body.classList.add('high-contrast-theme');
                localStorage.setItem('theme', 'high-contrast-theme');
            } else if (body.classList.contains('high-contrast-theme')) {
                body.classList.remove('high-contrast-theme');
                localStorage.setItem('theme', '');
            } else {
                body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark-theme');
            }
        });
    }
    
    // Dyslexia Toggle Functionality
    const dyslexiaToggle = document.getElementById('dyslexia-toggle');
    
    // Load saved dyslexia preference
    const savedDyslexiaMode = localStorage.getItem('dyslexiaMode');
    if (savedDyslexiaMode === 'true') {
        body.classList.add('dyslexia-mode');
    }
    
    if (dyslexiaToggle) {
        dyslexiaToggle.addEventListener('click', function() {
            body.classList.toggle('dyslexia-mode');
            const isDyslexiaMode = body.classList.contains('dyslexia-mode');
            localStorage.setItem('dyslexiaMode', isDyslexiaMode);
        });
    }
});

// Theme configuration
const themes = {
    ocean: {
        primary: '#2176FF',
        primaryDark: '#1557CC',
        gradient: 'linear-gradient(135deg, #2176FF 0%, #1557CC 100%)',
        name: 'Ocean Blue'
    },
    midnight: {
        primary: '#1A1A1A',
        primaryDark: '#000000',
        gradient: 'linear-gradient(135deg, #1A1A1A 0%, #000000 100%)',
        name: 'Midnight'
    },
    emerald: {
        primary: '#10B981',
        primaryDark: '#059669',
        gradient: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
        name: 'Emerald'
    },
    royal: {
        primary: '#8B5CF6',
        primaryDark: '#6D28D9',
        gradient: 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)',
        name: 'Royal Purple'
    },
    sunset: {
        primary: '#F97316',
        primaryDark: '#EA580C',
        gradient: 'linear-gradient(135deg, #F97316 0%, #EA580C 100%)',
        name: 'Sunset'
    }
};

// Change theme function
function changeTheme(themeName) {
    const theme = themes[themeName];
    if (!theme) return;

    // Update CSS variables
    document.documentElement.style.setProperty('--primary-color', theme.primary);
    document.documentElement.style.setProperty('--primary-dark', theme.primaryDark);
    document.documentElement.style.setProperty('--primary-gradient', theme.gradient);

    // Save to localStorage
    localStorage.setItem('selectedTheme', themeName);

    // Update active state
    document.querySelectorAll('.theme-option').forEach(option => {
        option.classList.remove('active');
    });
    document.querySelector(`[data-theme="${themeName}"]`).classList.add('active');

    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('themeModal'));
    if (modal) {
        modal.hide();
    }

    // Show success message
    showThemeChangeMessage(theme.name);
}

// Show theme change message
function showThemeChangeMessage(themeName) {
    const message = document.createElement('div');
    message.className = 'theme-change-toast';
    message.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        Theme changed to ${themeName}
    `;
    document.body.appendChild(message);

    setTimeout(() => {
        message.classList.add('show');
    }, 100);

    setTimeout(() => {
        message.classList.remove('show');
        setTimeout(() => message.remove(), 300);
    }, 2000);
}

// Load saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('selectedTheme') || 'ocean';
    changeTheme(savedTheme);
});

expandButtons = [...document.querySelectorAll('[id*="expand-reply"]')];
expandButtons.push(document.querySelector('[for*="expand"]'));

expandButtons.forEach(btn => {
    if (!userIsAuthenticated) { 
        btn.onclick = null;
    }
    btn.addEventListener("click", (e) => {
        if (!userIsAuthenticated) {
            e.preventDefault();
            showNotification('login-required');
        }
    });
});
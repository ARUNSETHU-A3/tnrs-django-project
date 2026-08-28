document.addEventListener('DOMContentLoaded', function() {
    console.log('TNRS - Application Started');
    
 
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navLinks.classList.toggle('hidden');
        });
        
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.navbar-left') && !e.target.closest('.nav-links')) {
                navLinks.classList.add('hidden');
            }
        });
    }
    
   
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            const cards = document.querySelectorAll('.app-card');
            
            cards.forEach(card => {
                const text = card.innerText.toLowerCase();
                card.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
    
   
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const card = this.closest('.app-card');
            const title = card ? card.querySelector('.card-title').innerText : 'item';
            
            if (!confirm(`Add "${title}" to cart?`)) {
                e.preventDefault();
            }
        });
    });
    
  
    document.querySelectorAll('.remove-from-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const card = this.closest('.app-card');
            const title = card ? card.querySelector('.card-title').innerText : 'item';
            
            if (!confirm(`Remove "${title}" from cart?`)) {
                e.preventDefault();
            }
        });
    });
    
   
    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            if (!confirm('Logout from TNRS?')) {
                e.preventDefault();
            }
        });
    }
    
    console.log('✓ TNRS Interface Ready');
});
document.addEventListener("DOMContentLoaded", function() {
    // Handle buy buttons from cart page
    const buyLinks = document.querySelectorAll(".app-card .app-buy-btn");

    buyLinks.forEach(link => {
        if (link.tagName === 'A') {
            link.addEventListener("click", function(e) {
                if (!window.confirm("Proceed to place your order?")) {
                    e.preventDefault();
                }
            });
        }
    });
});
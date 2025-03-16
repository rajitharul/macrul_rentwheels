// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize date pickers
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.min = new Date().toISOString().split('T')[0];
    });
});

// Handle rental form submission
document.addEventListener('DOMContentLoaded', function() {
    const rentalForm = document.getElementById('rental-form');
    if (rentalForm) {
        rentalForm.addEventListener('submit', function(e) {
            const startDate = new Date(document.getElementById('start_date').value);
            const endDate = new Date(document.getElementById('end_date').value);
            
            if (endDate <= startDate) {
                e.preventDefault();
                alert('End date must be after start date');
            }
        });
    }
});

// Dynamic price calculation
function updateTotalPrice() {
    const startDate = new Date(document.getElementById('start_date').value);
    const endDate = new Date(document.getElementById('end_date').value);
    const dailyRate = parseFloat(document.getElementById('daily_rate').value);
    
    if (!isNaN(dailyRate) && startDate && endDate && endDate > startDate) {
        const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
        const total = days * dailyRate;
        document.getElementById('total_cost').textContent = total.toFixed(2);
    }
}

// Vehicle filter functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('vehicle-filter-form');
    if (filterForm) {
        filterForm.addEventListener('change', function() {
            this.submit();
        });
    }
});

// Review star rating
function setRating(rating) {
    document.getElementById('rating').value = rating;
    const stars = document.querySelectorAll('.rating-star');
    stars.forEach((star, index) => {
        star.classList.toggle('active', index < rating);
    });
}

// Confirmation dialogs
function confirmCancellation(rentalId) {
    return confirm('Are you sure you want to cancel this rental?');
}

// Image preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('image-preview').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Show/hide password
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.querySelector(`[data-password-toggle="${inputId}"]`);
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// Responsive navigation
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }
}); 
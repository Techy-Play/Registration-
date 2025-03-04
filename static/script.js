// Form validation
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    })
})()

// Profile photo preview
document.addEventListener('DOMContentLoaded', function() {
    const profilePhotoInput = document.getElementById('profile_photo');
    if (profilePhotoInput) {
        profilePhotoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = this.parentElement.parentElement.querySelector('.profile-photo');
                    if (img) {
                        img.src = e.target.result;
                    }
                }.bind(this);
                reader.readAsDataURL(file);
            }
        });
    }
});

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Mobile number validation
document.addEventListener('DOMContentLoaded', function() {
    const mobileInputs = document.querySelectorAll('input[type="tel"]');
    mobileInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });
    });
});

// Password strength indicator
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    if (passwordInput && window.location.pathname === '/') { // Only on registration page
        const feedback = document.createElement('div');
        feedback.className = 'password-strength mt-1';
        passwordInput.parentElement.appendChild(feedback);

        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            let message = '';

            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;

            switch (strength) {
                case 0:
                case 1:
                    message = '<span class="text-danger">Very weak</span>';
                    break;
                case 2:
                    message = '<span class="text-warning">Weak</span>';
                    break;
                case 3:
                    message = '<span class="text-info">Medium</span>';
                    break;
                case 4:
                    message = '<span class="text-primary">Strong</span>';
                    break;
                case 5:
                    message = '<span class="text-success">Very strong</span>';
                    break;
            }

            feedback.innerHTML = message;
        });
    }
});

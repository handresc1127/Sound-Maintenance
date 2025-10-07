/* ==========================================================================
   Soundlab - La Casa del DJ - JavaScript Functions
   ========================================================================== */

$(document).ready(function() {
    
    // Initialize all components
    initializeComponents();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Add fade-in animation to cards
    $('.card').addClass('fade-in-up');
    
});

/**
 * Initialize all JavaScript components
 */
function initializeComponents() {
    initializeTooltips();
    initializePopovers();
    initializeDataTables();
    initializeFormValidation();
    initializeImagePreviews();
    initializeStatusUpdates();
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initializePopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Initialize DataTables for better table functionality
 */
function initializeDataTables() {
    if ($.fn.DataTable) {
        $('.datatable').DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
            },
            pageLength: 10,
            dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip',
            columnDefs: [
                { orderable: false, targets: 'no-sort' }
            ]
        });
    }
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    // Bootstrap validation
    (function() {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();
    
    // Custom validations
    validateCustomerForm();
    validateServiceForm();
    validateInventoryForm();
}

/**
 * Customer form validation
 */
function validateCustomerForm() {
    $('#customer-form').on('submit', function(e) {
        var isValid = true;
        
        // Validate name
        var name = $('#name').val().trim();
        if (name.length < 2) {
            showFieldError('#name', 'El nombre debe tener al menos 2 caracteres');
            isValid = false;
        }
        
        // Validate email if provided
        var email = $('#email').val().trim();
        if (email && !isValidEmail(email)) {
            showFieldError('#email', 'Ingrese un email válido');
            isValid = false;
        }
        
        // Validate phone if provided
        var phone = $('#phone').val().trim();
        if (phone && !isValidPhone(phone)) {
            showFieldError('#phone', 'Ingrese un teléfono válido');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
}

/**
 * Service form validation
 */
function validateServiceForm() {
    $('#service-form').on('submit', function(e) {
        var isValid = true;
        
        // Validate customer selection
        if (!$('#customer_id').val()) {
            showFieldError('#customer_id', 'Debe seleccionar un cliente');
            isValid = false;
        }
        
        // Validate equipment selection
        if (!$('#equipment_id').val()) {
            showFieldError('#equipment_id', 'Debe seleccionar un equipo');
            isValid = false;
        }
        
        // Validate description
        var description = $('#description').val().trim();
        if (description.length < 10) {
            showFieldError('#description', 'La descripción debe tener al menos 10 caracteres');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
}

/**
 * Inventory form validation
 */
function validateInventoryForm() {
    $('#inventory-form').on('submit', function(e) {
        var isValid = true;
        
        // Validate stock
        var stock = parseInt($('#stock').val());
        if (isNaN(stock) || stock < 0) {
            showFieldError('#stock', 'El stock debe ser un número positivo');
            isValid = false;
        }
        
        // Validate min_stock
        var minStock = parseInt($('#min_stock').val());
        if (isNaN(minStock) || minStock < 0) {
            showFieldError('#min_stock', 'El stock mínimo debe ser un número positivo');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
}

/**
 * Initialize image previews for evidence uploads
 */
function initializeImagePreviews() {
    $('input[type="file"]').on('change', function(e) {
        var file = e.target.files[0];
        var preview = $(this).closest('.form-group').find('.image-preview');
        
        if (file && file.type.startsWith('image/')) {
            var reader = new FileReader();
            reader.onload = function(e) {
                preview.html('<img src="' + e.target.result + '" class="img-thumbnail" style="max-width: 200px;">');
            };
            reader.readAsDataURL(file);
        } else {
            preview.empty();
        }
    });
}

/**
 * Initialize status update functionality
 */
function initializeStatusUpdates() {
    $('.status-select').on('change', function() {
        var serviceId = $(this).data('service-id');
        var newStatus = $(this).val();
        
        if (serviceId && newStatus) {
            updateServiceStatus(serviceId, newStatus);
        }
    });
}

/**
 * Update service status via AJAX
 */
function updateServiceStatus(serviceId, status) {
    $.ajax({
        url: '/api/services/' + serviceId + '/status',
        method: 'POST',
        data: {
            status: status
        },
        success: function(response) {
            showAlert('success', 'Estado actualizado correctamente');
            // Update status indicator
            updateStatusIndicator(serviceId, status);
        },
        error: function() {
            showAlert('danger', 'Error al actualizar el estado');
        }
    });
}

/**
 * Update status indicator visual
 */
function updateStatusIndicator(serviceId, status) {
    var indicator = $('.service-row[data-service-id="' + serviceId + '"] .status-indicator');
    indicator.removeClass('status-recibido status-proceso status-completado status-entregado');
    
    switch(status.toLowerCase()) {
        case 'recibido':
            indicator.addClass('status-recibido');
            break;
        case 'en proceso':
            indicator.addClass('status-proceso');
            break;
        case 'completado':
            indicator.addClass('status-completado');
            break;
        case 'entregado':
            indicator.addClass('status-entregado');
            break;
    }
}

/**
 * Customer search functionality
 */
function searchCustomers(query) {
    return $.ajax({
        url: '/api/customers/search',
        method: 'GET',
        data: { q: query }
    });
}

/**
 * Equipment search functionality
 */
function searchEquipment(query, customerId) {
    return $.ajax({
        url: '/api/equipment/search',
        method: 'GET',
        data: { 
            q: query,
            customer_id: customerId 
        }
    });
}

/**
 * Inventory search functionality
 */
function searchInventory(query) {
    return $.ajax({
        url: '/api/inventory/search',
        method: 'GET',
        data: { q: query }
    });
}

/**
 * Utility Functions
 */

/**
 * Show field validation error
 */
function showFieldError(fieldSelector, message) {
    var field = $(fieldSelector);
    field.addClass('is-invalid');
    
    var feedback = field.next('.invalid-feedback');
    if (feedback.length === 0) {
        field.after('<div class="invalid-feedback">' + message + '</div>');
    } else {
        feedback.text(message);
    }
}

/**
 * Clear field validation error
 */
function clearFieldError(fieldSelector) {
    var field = $(fieldSelector);
    field.removeClass('is-invalid');
    field.next('.invalid-feedback').remove();
}

/**
 * Show alert message
 */
function showAlert(type, message) {
    var alertHtml = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
                    '<i class="fas fa-' + getAlertIcon(type) + ' me-2"></i>' + message +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                    '</div>';
    
    $('.main-content').prepend(alertHtml);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert:first').fadeOut('slow');
    }, 5000);
}

/**
 * Get appropriate icon for alert type
 */
function getAlertIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'danger': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        case 'info': return 'info-circle';
        default: return 'info-circle';
    }
}

/**
 * Email validation
 */
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Phone validation (Colombian format)
 */
function isValidPhone(phone) {
    var phoneRegex = /^(\+57|0057|57)?[\s\-]?[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/\s+/g, ''));
}

/**
 * Format currency (Colombian Pesos)
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
    }).format(amount);
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    if (!dateString) return '';
    
    var date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Confirm deletion dialog
 */
function confirmDelete(message, callback) {
    if (confirm(message || '¿Está seguro de que desea eliminar este elemento?')) {
        if (typeof callback === 'function') {
            callback();
        }
    }
}

/**
 * Equipment category icon mapping
 */
function getEquipmentIcon(category) {
    var icons = {
        'consola': 'fas fa-music',
        'controlador': 'fas fa-sliders-h',
        'luces': 'fas fa-lightbulb',
        'sonido': 'fas fa-volume-up',
        'humo': 'fas fa-cloud',
        'otros': 'fas fa-tools'
    };
    
    return icons[category.toLowerCase()] || icons['otros'];
}

/**
 * Print functionality
 */
function printElement(elementSelector) {
    var printContents = $(elementSelector).html();
    var originalContents = document.body.innerHTML;
    
    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
    
    // Reload to restore functionality
    location.reload();
}
// Main JavaScript for HealthHub

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // CSRF Token for AJAX
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                      document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    // Add CSRF token to all AJAX requests
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.getElementById('toast-container') || 
                          document.body.appendChild(document.createElement('div'));
    toastContainer.id = 'toast-container';
    toastContainer.innerHTML = toastHTML;
    
    const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
    toast.show();
}

// Confirmation dialog
function confirm(message, callback) {
    if (window.confirm(message)) {
        callback();
    }
}

// Add to cart functionality
function addToCart(medicineId) {
    $.post(`/pharmacy/add-to-cart/${medicineId}/`, function(data) {
        showToast('Added to cart successfully!', 'success');
    }).fail(function() {
        showToast('Error adding to cart', 'danger');
    });
}

// Remove from cart
function removeFromCart(medicineId) {
    if (window.confirm('Remove this item from cart?')) {
        window.location.href = `/pharmacy/remove-from-cart/${medicineId}/`;
    }
}

// Rating system
function setRating(value) {
    const stars = document.querySelectorAll('.rating-star');
    stars.forEach((star, index) => {
        if (index < value) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
    document.getElementById('rating-input').value = value;
}

// Print functionality
function printDocument(elementId) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '', 'height=800,width=800');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link rel="stylesheet" href="/static/css/style.css">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// Download PDF
function downloadPDF(elementId, filename) {
    const element = document.getElementById(elementId);
    const opt = {
        margin: 10,
        filename: filename,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' }
    };
    html2pdf().set(opt).from(element).save();
}

// Real-time search
let searchTimeout;
function liveSearch(inputId, resultsId, url) {
    const input = document.getElementById(inputId);
    const results = document.getElementById(resultsId);
    
    input.addEventListener('keyup', function() {
        clearTimeout(searchTimeout);
        const query = this.value;
        
        if (query.length < 2) {
            results.innerHTML = '';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            $.get(url, { q: query }, function(data) {
                results.innerHTML = data;
            });
        }, 300);
    });
}

// Validate form
function validateForm(formId) {
    const form = document.getElementById(formId);
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    let csv = [];
    
    for (let row of table.rows) {
        let rowData = [];
        for (let cell of row.cells) {
            rowData.push('"' + cell.innerText + '"');
        }
        csv.push(rowData.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// WebSocket for chat
function initializeChat(roomId) {
    const chatSocket = new WebSocket(
        `ws://${window.location.host}/ws/chat/${roomId}/`
    );

    chatSocket.onopen = function(e) {
        console.log('Chat connection established');
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message received';
        messageDiv.innerHTML = `
            <strong>${data.username}</strong><br>
            ${data.message}<br>
            <small>${data.timestamp}</small>
        `;
        document.getElementById('chat-messages').appendChild(messageDiv);
        document.getElementById('chat-messages').scrollTop = 
            document.getElementById('chat-messages').scrollHeight;
    };

    chatSocket.onclose = function(e) {
        console.log('Chat connection closed');
    };

    document.getElementById('chat-form')?.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = document.getElementById('chat-input').value;
        chatSocket.send(JSON.stringify({ message: message }));
        document.getElementById('chat-input').value = '';
    });
}

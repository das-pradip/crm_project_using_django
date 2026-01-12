


 const leadStatusLabels = JSON.parse(
        document.getElementById('lead-labels').textContent
    );

    const leadStatusData = JSON.parse(
        document.getElementById('lead-data').textContent
    );

// PIE CHART
new Chart(document.getElementById('statusChart'), {
    type: 'pie',
    data: {
        labels: leadStatusLabels,
        datasets: [{
            data: leadStatusData,
            backgroundColor: [
                '#0d6efd', // New
                '#ffc107', // Contacted
                '#0dcaf0', // Qualified
                '#198754', // Converted
                '#dc3545'  // Lost
            ]
        }]
    }
});

// BAR CHART
new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: leadStatusLabels,
        datasets: [{
            label: 'Lead Count',
            data: leadStatusData,
            backgroundColor: [
                '#0d6efd', // New
                '#ffc107', // Contacted
                '#0dcaf0', // Qualified
                '#198754', // Converted
                '#dc3545'  // Lost
            ]
        }]
    }
});
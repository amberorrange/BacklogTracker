"use strict";

const ctx = document.getElementById('hoursByGenreChart').getContext('2d');
const hoursByGenreChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Hours Played',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});
   
const ctx2 = document.getElementById('genrePercentagesChart').getContext('2d');
const genrePercentagesChart = new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: [],
        datasets: [{
            label: 'Percent Played By Each Genre',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

$.get("/get_hours_by_genre.json", (response) => {
    hoursByGenreChart.data.labels = response.labels;
    hoursByGenreChart.data.datasets[0].data = response.data.quantity;
    hoursByGenreChart.update();

    let totalHours = 0;
    const percentagesArry = [];

    for (const hours of response.data.quantity) {
        totalHours += hours;
      }
    
    for (const hours of response.data.quantity) {
        percentagesArry.push(((hours / totalHours) * 100).toFixed(2))
    }

    genrePercentagesChart.data.labels = response.labels;
    genrePercentagesChart.data.datasets[0].data = percentagesArry;
    genrePercentagesChart.update();
});


const ctx3 = document.getElementById('hoursByPlatformChart').getContext('2d');
const hoursByPlatformChart = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Hours Played',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});
   
const ctx4 = document.getElementById('platformPercentagesChart').getContext('2d');
const platformPercentagesChart = new Chart(ctx4, {
    type: 'pie',
    data: {
        labels: [],
        datasets: [{
            label: 'Percent Played By Each Platform',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

$.get("/get_hours_by_platform.json", (response) => {
    console.log(response)
    hoursByPlatformChart.data.labels = response.labels;
    hoursByPlatformChart.data.datasets[0].data = response.data.quantity;
    hoursByPlatformChart.update();

    let totalHours = 0;
    const percentagesArry = [];

    for (const hours of response.data.quantity) {
        totalHours += hours;
      }
    
    for (const hours of response.data.quantity) {
        percentagesArry.push(((hours / totalHours) * 100).toFixed(2))
    }

    platformPercentagesChart.data.labels = response.labels;
    platformPercentagesChart.data.datasets[0].data = percentagesArry;
    platformPercentagesChart.update();
});





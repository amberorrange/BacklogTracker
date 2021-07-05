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
                'rgba(255,83,235, .2)',
                'rgba(252,241,108, .2)',
                'rgba(70, 200, 243, .2)',
                'rgba(90,44,143, .2)',
                'rgba(248,167,21, .2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                 'rgba(255,83,235, 1)',
                'rgba(252,241,108, 1)',
                'rgba(70, 200, 243, 1)',
                'rgba(90,44,143, 1)',
                'rgba(248,167,21, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1,
            datalabels: {
                color: 'white',
                anchor: 'end',
                align: 'top',
                offset: 5,
                font: {
                    family: 'montserrat',
                    size: 14
                }
            }
        }]
    },
    plugins: [ChartDataLabels],  
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Hours Played',
                    font: {
                        size: 20,
                        family:  'montserrat'
                    },
                    color: 'white',
                    padding: 22
                },
                ticks: {
                    color: 'white',
                    font:{
                        family: 'montserrat',
                        size: 12
                    }
                },
                grid: {
                    borderColor: 'white'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Genre',
                    font: {
                        size: 20,
                        family:  'montserrat',
                    },
                    color: 'white',
                    padding: 22
                },
                ticks: {
                    color: 'white',
                    font: {
                        family: 'montserrat',
                        size: 16
                    }
                },
                grid: {
                    borderColor: 'white'
                }
            }   
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Hours Played by Genre',
                padding: {
                    top: 20,
                    bottom: 30,
                },
                font: {
                    size: 30,
                    family:  'montserrat'
                },
                color:'white'
            },
            legend: {
                display: false  
            },
        }
    },
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
                'rgba(255,83,235, .2)',
                'rgba(252,241,108, .2)',
                'rgba(70, 200, 243, .2)',
                'rgba(90,44,143, .2)',
                'rgba(248,167,21, .2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor:  [
                'rgba(255,83,235, 1)',
               'rgba(252,241,108, 1)',
               'rgba(70, 200, 243, 1)',
               'rgba(90,44,143, 1)',
               'rgba(248,167,21, 1)',
               'rgba(255, 99, 132, 1)',
               'rgba(54, 162, 235, 1)',
               'rgba(75, 192, 192, 1)',
               'rgba(153, 102, 255, 1)',
               'rgba(255, 159, 64, 1)'
           ],
            hoverOffset: 4,
            datalabels: {
                color: 'white',
                font: {
                    family: 'montserrat',
                    size: 18
                },
                display: true,
                clip: false,
                anchor: 'end',
                offset: '5',
                align: 'end',
            formatter: (value) => {
                        return value + '%';
                    }                
            }
        }]
    },
    plugins: [ChartDataLabels],
    options: {
        layout: {
            padding: {
                bottom: 30
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Percentage of Hours Played by Genre',
                padding: {
                    top: 30,
                    bottom: 50
                },
                font: {
                    size: 30,
                    family: 'montserrat'
                },
                color: 'white'
            },
            legend: {
                position: 'right',
                labels: {
                    color: 'white',
                    font: {
                        family: 'montserrat',
                        size: 20
                    }
                } 
            }
        }
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
        percentagesArry.push(Math.round(((hours / totalHours) * 100)))
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
                'rgba(255,83,235, .2)',
                'rgba(252,241,108, .2)',
                'rgba(70, 200, 243, .2)',
                'rgba(90,44,143, .2)',
                'rgba(248,167,21, .2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,83,235, 1)',
               'rgba(252,241,108, 1)',
               'rgba(70, 200, 243, 1)',
               'rgba(90,44,143, 1)',
               'rgba(248,167,21, 1)',
               'rgba(255, 99, 132, 1)',
               'rgba(54, 162, 235, 1)',
               'rgba(75, 192, 192, 1)',
               'rgba(153, 102, 255, 1)',
               'rgba(255, 159, 64, 1)'
           ],
            borderWidth: 1,
            datalabels: {
                color: 'white',
                anchor: 'end',
                align: 'top',
                offset: 5,
                font: { 
                    family: 'montserrat',
                    size: 14
                }
            }
        }]
    },
    plugins: [ChartDataLabels], 
    options: {
        scales: {
            y: {  
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Hours Played',
                    font: {
                        size: 20,
                        family: 'montserrat'
                    },
                    color: 'white',
                    padding: 22
                },
                ticks: {
                    color: 'white',
                    font: {
                        family: 'montserrat',
                        size: 12
                    }
                },
                grid: {
                    borderColor: 'white'
                }              
            },
            x: {
                title: {
                    display: true,
                    text: 'Platform',
                    font: {
                        size: 20,
                        family: 'montserrat'
                    },
                    color: 'white',
                    padding: 22
                },
                ticks: {
                    color: 'white',
                    font: {
                        family: 'montserrat',
                        size: 16
                    }
                },
                grid: {
                    borderColor: 'white'
                }
            }  
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Hours Played by Platform',
                padding: {
                    top: 40,
                    bottom: 30
                },
                font: {
                    size: 30,
                    family: 'montserrat'
                },
                color: 'white'
            },
            legend: {
                display: false
            }

        }   
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
                'rgba(255,83,235, .2)',
                'rgba(252,241,108, .2)',
                'rgba(70, 200, 243, .2)',
                'rgba(90,44,143, .2)',
                'rgba(248,167,21, .2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor:  [
                'rgba(255,83,235, 1)',
               'rgba(252,241,108, 1)',
               'rgba(70, 200, 243, 1)',
               'rgba(90,44,143, 1)',
               'rgba(248,167,21, 1)',
               'rgba(255, 99, 132, 1)',
               'rgba(54, 162, 235, 1)',
               'rgba(75, 192, 192, 1)',
               'rgba(153, 102, 255, 1)',
               'rgba(255, 159, 64, 1)'
           ],
            hoverOffset: 4,
            datalabels: {
                color: 'white',
                font: {
                    family: 'montserrat',
                    size: 18
                },
                display: true,
                clip: false,
                anchor: 'end',
                offset: '5',
                align: 'end',
            formatter: (value) => {
                        return value + '%';
                    }                
            }
        }]
    },
    plugins: [ChartDataLabels],
    options: {
        layout: {
            padding: {
                bottom: 30
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Percentage of Hours Played by Platform',
                padding: {
                    top: 20,
                    bottom: 50
                },
                font: {
                    size: 30,
                    family: 'montserrat'
                },
                color: 'white'
            },
            legend: {
                position: 'right',
                labels: {
                    color: 'white',
                    font: {
                        family: 'montserrat',
                        size: 20
                    }
                }
            }
        }
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
        percentagesArry.push(Math.round(((hours / totalHours) * 100)))
    }

    platformPercentagesChart.data.labels = response.labels;
    platformPercentagesChart.data.datasets[0].data = percentagesArry;
    platformPercentagesChart.update();
});






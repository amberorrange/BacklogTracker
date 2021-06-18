"use strict";


// $.get('//get_chart_info.json', (res) => { // ajax request to get info from flask
//     const data = [];
//     // for (const dailyTotal of res.data) {
//     //   data.push({x: dailyTotal.date, y: dailyTotal.melons_sold});
//     }


$(window).on("load", function() {
    $.get("/get_chart_info.json"), {}, (res) => {
     console.log(res)
  }
  });

const ctx = document.getElementById('hoursByGenreChart');
const hours_by_genre = new Chart(ctx, {
type: 'bar',
data: {
    labels: ['Action', 'RPG', 'Shooter', 'Adventure', 'Puzzle', 'Simulation'], // genres go here-rf
    datasets: [{
        label: 'Hours Played',
        data: [33, 19, 3, 100, 70, 3], //hours played for each genre,
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
    }
}
});
// Gráfico de Temperatura
const temperatureCtx = document.getElementById('temperatureChart').getContext('2d');
new Chart(temperatureCtx, {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'Temperatura Sensor (°C)',
                data: sensorData.map(item => ({
                    x: new Date(item.timestamp),
                    y: item.temperature
                })),
                borderColor: '#FF6384',
                fill: false
            },
            {
                label: 'Temperatura OpenWeatherMap (°C)',
                data: weatherData.map(item => ({
                    x: new Date(item.timestamp),
                    y: item.temperature
                })),
                borderColor: '#36A2EB',
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'minute'
                },
                title: {
                    display: true,
                    text: 'Fecha y Hora'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Temperatura (°C)'
                }
            }
        }
    }
});

// Gráfico de Humedad
const humidityCtx = document.getElementById('humidityChart').getContext('2d');
new Chart(humidityCtx, {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'Humedad Sensor (%)',
                data: sensorData.map(item => ({
                    x: new Date(item.timestamp),
                    y: item.humidity
                })),
                borderColor: '#4BC0C0',
                fill: false
            },
            {
                label: 'Humedad OpenWeatherMap (%)',
                data: weatherData.map(item => ({
                    x: new Date(item.timestamp),
                    y: item.humidity
                })),
                borderColor: '#FFCE56',
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'minute'
                },
                title: {
                    display: true,
                    text: 'Fecha y Hora'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Humedad (%)'
                }
            }
        }
    }
});




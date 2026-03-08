// Gráficos de progreso usando Chart.js

class ProgressCharts {
    constructor() {
        this.charts = {};
        this.init();
    }
    
    init() {
        // Cargar Chart.js desde CDN si no está disponible
        if (typeof Chart === 'undefined') {
            this.loadChartJS();
        } else {
            this.createCharts();
        }
    }
    
    loadChartJS() {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => this.createCharts();
        document.head.appendChild(script);
    }
    
    createCharts() {
        this.createProgressChart();
        this.createDifficultyChart();
        this.createActivityChart();
    }
    
    createProgressChart() {
        const ctx = document.getElementById('progress-chart')?.getContext('2d');
        if (!ctx) return;
        
        // Obtener datos del atributo data
        const chartData = ctx.canvas.dataset;
        const completed = parseInt(chartData.completed) || 0;
        const total = parseInt(chartData.total) || 100;
        const remaining = total - completed;
        
        this.charts.progress = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completados', 'Pendientes'],
                datasets: [{
                    data: [completed, remaining],
                    backgroundColor: ['#1cc88a', '#e74a3b'],
                    hoverBackgroundColor: ['#17a673', '#be3e31'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    createDifficultyChart() {
        const ctx = document.getElementById('difficulty-chart')?.getContext('2d');
        if (!ctx) return;
        
        const chartData = ctx.canvas.dataset;
        const easy = parseInt(chartData.easy) || 0;
        const medium = parseInt(chartData.medium) || 0;
        const hard = parseInt(chartData.hard) || 0;
        
        this.charts.difficulty = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Fácil', 'Medio', 'Difícil'],
                datasets: [{
                    label: 'Ejercicios por nivel',
                    data: [easy, medium, hard],
                    backgroundColor: ['#1cc88a', '#f6c23e', '#e74a3b'],
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    createActivityChart() {
        const ctx = document.getElementById('activity-chart')?.getContext('2d');
        if (!ctx) return;
        
        const chartData = ctx.canvas.dataset;
        const days = JSON.parse(chartData.days || '[]');
        const activities = JSON.parse(chartData.activities || '[]');
        
        this.charts.activity = new Chart(ctx, {
            type: 'line',
            data: {
                labels: days,
                datasets: [{
                    label: 'Ejercicios realizados',
                    data: activities,
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.05)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    updateData(chartName, newData) {
        if (this.charts[chartName]) {
            this.charts[chartName].data = newData;
            this.charts[chartName].update();
        }
    }
    
    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            chart.resize();
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.progressCharts = new ProgressCharts();
    
    // Redimensionar gráficos cuando cambie el tamaño de la ventana
    window.addEventListener('resize', () => {
        if (window.progressCharts) {
            window.progressCharts.resizeCharts();
        }
    });
});

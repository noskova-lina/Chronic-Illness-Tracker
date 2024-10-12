import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';

function TriggerImpact({ trigger, period }) {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        fetch(`/api/trigger_impact?trigger=${trigger}&period=${period}`)
            .then(response => response.json())
            .then(data => setChartData(data));
    }, [trigger, period]);

    return (
        <div>
            <h3>Trigger Impact: {trigger}</h3>
            {chartData ? (
                <canvas id="triggerImpactChart"></canvas>
            ) : (
                <p>Loading data...</p>
            )}

            {chartData && (
                <script>
                    {`
                    const ctx = document.getElementById('triggerImpactChart').getContext('2d');
                    const triggerImpactChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ${chartData.map(item => item.symptom_name)},
                            datasets: [{
                                label: 'Symptom Severity',
                                data: ${chartData.map(item => item.severity)},
                                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                                borderColor: 'rgba(255, 159, 64, 1)',
                                borderWidth: 1
                            }]
                        }
                    });
                    `}
                </script>
            )}
        </div>
    );
}

export default TriggerImpact;

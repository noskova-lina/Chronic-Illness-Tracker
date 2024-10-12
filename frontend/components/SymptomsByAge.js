import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';

function SymptomsByAge({ startDate, endDate, ageGroup }) {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        fetch(`/api/filter_symptoms_by_age?startDate=${startDate}&endDate=${endDate}&ageGroup=${ageGroup}`)
            .then(response => response.json())
            .then(data => setChartData(data));
    }, [startDate, endDate, ageGroup]);

    return (
        <div>
            <h3>Average Symptom Severity and Triggers</h3>
            {chartData ? (
                <canvas id="symptomsChart"></canvas>
            ) : (
                <p>Loading data...</p>
            )}

            {chartData && (
                <script>
                    {`
                    const ctx = document.getElementById('symptomsChart').getContext('2d');
                    const symptomsChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: ${chartData.map(item => item.symptom_name)},
                            datasets: [{
                                label: 'Average Symptom Severity',
                                data: ${chartData.map(item => item.average_severity)},
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(75, 192, 192, 1)',
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

export default SymptomsByAge;

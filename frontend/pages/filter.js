import { useState } from 'react';
import SymptomsByAge from '../components/SymptomsByAge';
import TriggerImpact from '../components/TriggerImpact';

export default function FilterPage() {
    // Define state for start date, end date, and age group
    const [startDate, setStartDate] = useState("2016-06-01");
    const [endDate, setEndDate] = useState("2016-07-31");
    const [ageGroup, setAgeGroup] = useState("25-34");

    // Define state for trigger and period
    const [trigger, setTrigger] = useState("dairy consumption");
    const [period, setPeriod] = useState(6);

    return (
        <div>
            <h1>Data Filtering</h1>

            {/* Input fields to change the date range */}
            <div>
                <label>Start Date: </label>
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
                <label>End Date: </label>
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>

            {/* Input field to change the age group */}
            <div>
                <label>Age Group: </label>
                <input
                    type="text"
                    value={ageGroup}
                    onChange={(e) => setAgeGroup(e.target.value)}
                />
            </div>

            {/* Render SymptomsByAge component with updated values */}
            <SymptomsByAge startDate={startDate} endDate={endDate} ageGroup={ageGroup} />

            <hr />

            {/* Input field to change the trigger and period */}
            <div>
                <label>Trigger: </label>
                <input
                    type="text"
                    value={trigger}
                    onChange={(e) => setTrigger(e.target.value)}
                />
                <label>Period (months): </label>
                <input
                    type="number"
                    value={period}
                    onChange={(e) => setPeriod(e.target.value)}
                />
            </div>

            {/* Render TriggerImpact component with updated values */}
            <TriggerImpact trigger={trigger} period={period} />
        </div>
    );
}

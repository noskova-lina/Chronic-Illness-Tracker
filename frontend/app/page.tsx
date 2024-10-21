import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <h1>Health Tracker Dashboard</h1>
      <nav>
        <ul>
          <li>
            <Link href="/average_severity">Average Symptom Severity</Link>
          </li>
          <li>
            <Link href="/treatment_frequency">Treatment Frequency</Link>
          </li>
          <li>
            <Link href="/trigger_impact">Trigger Impact</Link>
          </li>
          <li>
            <Link href="/symptom_filter">Symptom Filter</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}

import Link from 'next/link';
import styles from '../styles/Home.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Health Tracker Dashboard</h1>
      <nav className={styles.nav}>
        <ul className={styles.navList}>
          <li className={styles.navItem}>
            <Link href="/average_severity" className={styles.navLink}>Average Symptom Severity</Link>
          </li>
          <li className={styles.navItem}>
            <Link href="/treatment_frequency" className={styles.navLink}>Treatment Frequency</Link>
          </li>
          <li className={styles.navItem}>
            <Link href="/trigger_impact" className={styles.navLink}>Trigger Impact</Link>
          </li>
          <li className={styles.navItem}>
            <Link href="/symptom_filter" className={styles.navLink}>Symptom Filter</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}

export default async function handler(req, res) {
    const { startDate, endDate, ageGroup } = req.query;
    const response = await fetch(`${process.env.BACKEND_URL}/filter_symptoms_by_age?start_date=${startDate}&end_date=${endDate}&age_group=${ageGroup}`);
    const data = await response.json();
    res.status(200).json(data);
}

export default async function handler(req, res) {
    const { trigger, period } = req.query;
    const response = await fetch(`${process.env.BACKEND_URL}/trigger_impact?trigger=${trigger}&period=${period}`);
    const data = await response.json();
    res.status(200).json(data);
}

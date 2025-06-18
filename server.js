const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

// Временное хранилище статистики
let statsStorage = {};

app.post('/save-stats', (req, res) => {
  const { date, chat_id } = req.body;

  if (!statsStorage[chat_id]) {
    statsStorage[chat_id] = {};
  }

  if (!statsStorage[chat_id][date]) {
    statsStorage[chat_id][date] = 0;
  }

  statsStorage[chat_id][date] += 1;

  res.json({ success: true, stats: statsStorage[chat_id] });
});

app.get('/get-stats', (req, res) => {
  const { chat_id } = req.query;

  const stats = statsStorage[chat_id] || {};
  res.json(stats);
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

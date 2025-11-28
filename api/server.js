const express = require('express');
const enforcePolicy = require('./middleware/enforcePolicyMiddleware');

const app = express();
app.use(express.json());

app.get('/', (req, res) => {
  res.status(200).send('API is healthy');
});

app.post('/templates', enforcePolicy, (req, res) => {
  res.status(200).send('Template registration allowed by policy');
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`API server listening on port ${port}`);
});

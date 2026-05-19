const express = require('express');

const app = express();
app.use(express.json());

app.get('/healthz', (req, res) => res.json({ ok: true }));

module.exports = app;

if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => console.log(`server on ${port}`));
}

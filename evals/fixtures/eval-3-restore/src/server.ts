import express from "express";

export const app = express();
app.use(express.json());

app.post("/login", (_req, res) => {
  res.json({ token: "stub" });
});

if (require.main === module) {
  const port = Number(process.env.PORT ?? 3000);
  app.listen(port, () => console.log(`server on ${port}`));
}

const express = require("express");
const http = require("http");
const axios = require("axios");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(express.json());

// =============================================
// CHANGE THIS to your main Backend server URL
// If backend runs on same Pi, use http://localhost:5001
// If backend runs on a separate PC/server, use that IP
// =============================================
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5001";
const PORT = 5002;

// =============================================
// Store latest sensor reading in memory
// =============================================
let latestSensorData = {
  temperature: 0,
  humidity: 0,
  soil: 0,
  solar_output: 0,
  light_raw: 0,
  timestamp: null
};

let sensorHistory = [];

// =============================================
// ESP32 sends data here every 10 seconds
// =============================================
app.post("/api/sensor-data", async (req, res) => {
  const { temperature, humidity, soil, solar_output, light_raw } = req.body;

  if (temperature == null || humidity == null || soil == null) {
    return res.status(400).json({ error: "Missing sensor fields" });
  }

  latestSensorData = {
    temperature,
    humidity,
    soil,
    solar_output: solar_output || 0,
    light_raw: light_raw || 0,
    timestamp: new Date().toISOString()
  };

  // Keep last 100 readings
  sensorHistory.push({ ...latestSensorData });
  if (sensorHistory.length > 100) sensorHistory.shift();

  console.log(`[SENSOR] T:${temperature}°C | H:${humidity}% | Soil:${soil}% | Solar:${solar_output}W`);

  // Emit to any connected Socket.IO clients
  io.emit("sensor-update", latestSensorData);

  // Forward to main backend
  try {
    await axios.post(`${BACKEND_URL}/api/sensor-ingest`, latestSensorData);
    console.log("[FORWARDED] → Backend OK");
  } catch (err) {
    console.error("[FORWARD FAIL]", err.message);
  }

  res.json({ success: true, received: latestSensorData });
});

// Debug endpoint — check latest reading in browser
app.get("/api/latest", (req, res) => {
  res.json(latestSensorData);
});

// History endpoint
app.get("/api/history", (req, res) => {
  res.json(sensorHistory);
});

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    lastReading: latestSensorData.timestamp,
    totalReadings: sensorHistory.length
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`🍓 Raspberry Pi gateway running on port ${PORT}`);
  console.log(`   Forwarding to backend: ${BACKEND_URL}`);
});
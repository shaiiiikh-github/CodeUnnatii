import { useEffect, useState, useRef } from "react";
import { io } from "socket.io-client";

const SOCKET_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export const useSensorSocket = () => {
  const [sensorData, setSensorData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = io(SOCKET_URL, {
      withCredentials: true,
      transports: ["websocket"]
    });

    socketRef.current = socket;

    socket.on("connect", () => {
      console.log("🔌 Socket connected:", socket.id);
      setIsConnected(true);
    });

    socket.on("disconnect", () => {
      console.log("❌ Socket disconnected");
      setIsConnected(false);
    });

    socket.on("sensor-update", (data) => {
      console.log("📡 Live sensor data:", data);
      setSensorData(data);
      setLastUpdated(new Date().toLocaleTimeString());
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return { sensorData, isConnected, lastUpdated };
};
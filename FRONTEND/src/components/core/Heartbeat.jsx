import { useEffect, useRef, useState } from "react";

export default function Heartbeat({ alert = false }) {
  const canvasRef = useRef(null);
  const offsetRef = useRef(0);
  const [bpm, setBpm] = useState(72);
  const bpmRef = useRef(72);
  const alertRef = useRef(alert);

  useEffect(() => { alertRef.current = alert; }, [alert]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animId;

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    function ecgY(x, W, bpm, isAlert) {
      const period = W / (bpm / 60 * 2.5);
      const t = ((x % period) / period);
      if (isAlert) {
        if (t < 0.02) return 0.5 - t * 8;
        if (t < 0.06) return 0.5 - 0.16 + (t - 0.02) * 20;
        if (t < 0.10) return 0.5 + 0.64 - (t - 0.06) * 24;
        if (t < 0.14) return 0.5 - 0.32 + (t - 0.10) * 16;
        if (t < 0.18) return 0.5 + 0.32 - (t - 0.14) * 8;
        return 0.5;
      }
      if (t < 0.05) return 0.5 + Math.sin(t / 0.05 * Math.PI) * 0.06;
      if (t < 0.08) return 0.5 - (t - 0.05) / 0.03 * 0.25;
      if (t < 0.12) return 0.5 - 0.25 + (t - 0.08) / 0.04 * 1.0;
      if (t < 0.16) return 0.5 + 0.75 - (t - 0.12) / 0.04 * 1.1;
      if (t < 0.20) return 0.5 - 0.35 + (t - 0.16) / 0.04 * 0.45;
      if (t < 0.28) return 0.5 + 0.10 + Math.sin((t - 0.20) / 0.08 * Math.PI) * 0.15;
      return 0.5;
    }

    function draw() {
      const W = canvas.width, H = canvas.height;
      const currentBpm = bpmRef.current;
      const isAlert = alertRef.current;

      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = "#020814";
      ctx.fillRect(0, 0, W, H);

      ctx.strokeStyle = "rgba(56,189,248,0.07)";
      ctx.lineWidth = 0.5;
      for (let gx = 0; gx < W; gx += 20) {
        ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke();
      }
      for (let gy = 0; gy < H; gy += 20) {
        ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke();
      }

      const color = isAlert ? "#ff4d4d" : "#22d3ee";
      const glow  = isAlert ? "rgba(255,77,77,0.5)" : "rgba(34,211,238,0.5)";

      ctx.shadowBlur = 10;
      ctx.shadowColor = glow;
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();

      for (let x = 0; x < W; x++) {
        const xPos = (x + offsetRef.current) % W;
        const y = ecgY(xPos, W, currentBpm, isAlert) * H;
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      const fadeW = 50;
      const grad = ctx.createLinearGradient(W - fadeW, 0, W, 0);
      grad.addColorStop(0, "rgba(2,8,20,0)");
      grad.addColorStop(1, "rgba(2,8,20,1)");
      ctx.fillStyle = grad;
      ctx.fillRect(W - fadeW, 0, fadeW, H);

      offsetRef.current = (offsetRef.current + currentBpm / 60 * 1.8) % W;
      animId = requestAnimationFrame(draw);
    }

    draw();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  const handleBpm = (e) => {
    const val = parseInt(e.target.value);
    setBpm(val);
    bpmRef.current = val;
  };

  return (
    <div className="heartbeat-monitor">
      <div className="ecg-canvas-wrap">
        <canvas ref={canvasRef} className="ecg-canvas" />
        <span className="ecg-label">ECG</span>
        <span className="ecg-bpm">{bpm} BPM</span>
      </div>
      <div className="ecg-controls">
        <span className="ecg-ctrl-label">BPM</span>
        <input
          type="range"
          min="40"
          max="180"
          value={bpm}
          step="1"
          onChange={handleBpm}
          className="ecg-slider"
        />
        <span className="ecg-ctrl-val">{bpm}</span>
      </div>
    </div>
  );
}

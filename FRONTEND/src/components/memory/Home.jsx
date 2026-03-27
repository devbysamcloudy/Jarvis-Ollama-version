import  { useState, useEffect } from "react";
import { getWeather } from "../../api";

function Home() {
  const hour = new Date().getHours();
  let greeting = "Good Evening";
  if (hour < 12) greeting = "Good Morning";
  else if (hour < 18) greeting = "Good Afternoon";

  const [weather, setWeather] = useState(null);
  const [weatherLoading, setWeatherLoading] = useState(true);
  const [city, setCity] = useState("Nairobi");
  const [cityInput, setCityInput] = useState("");

  useEffect(() => {
    fetchWeather(city);
  }, [city]);

  const fetchWeather = async (targetCity) => {
    setWeatherLoading(true);
    try {
      const data = await getWeather(targetCity);
      setWeather(data);
    } catch {
      setWeather({ error: "Could not load weather" });
    } finally {
      setWeatherLoading(false);
    }
  };

  const handleCityChange = (e) => {
    e.preventDefault();
    if (cityInput.trim()) {
      setCity(cityInput.trim());
      setCityInput("");
    }
  };

  const getWeatherIcon = (desc) => {
    if (!desc) return "◈";
    const d = desc.toLowerCase();
    if (d.includes("rain")) return "🌧";
    if (d.includes("cloud")) return "☁";
    if (d.includes("clear") || d.includes("sun")) return "☀";
    if (d.includes("storm") || d.includes("thunder")) return "⛈";
    if (d.includes("snow")) return "❄";
    if (d.includes("mist") || d.includes("fog")) return "🌫";
    return "🌤";
  };

  return (
    <div className="page-container">
      <h1 className="home-greeting">{greeting}!</h1>
      <p className="home-welcome">Welcome to JARVIS</p>

      {/* Weather Widget */}
      <section className="home-section weather-section">
        <h2 className="section-title">Weather</h2>
        <div className="weather-widget">
          {weatherLoading ? (
            <p className="weather-loading">Loading weather...</p>
          ) : weather?.error ? (
            <p className="weather-error">{weather.error}</p>
          ) : (
            <div className="weather-card">
              <div className="weather-icon">{getWeatherIcon(weather.description)}</div>
              <div className="weather-info">
                <p className="weather-city">{weather.city}</p>
                <p className="weather-temp">{weather.temp}°C</p>
                <p className="weather-desc">{weather.description}</p>
                <p className="weather-extra">
                  Humidity: {weather.humidity}% · Wind: {weather.wind} m/s
                </p>
              </div>
            </div>
          )}

          {/* City Search */}
          <form onSubmit={handleCityChange} className="weather-form">
            <input
              type="text"
              value={cityInput}
              onChange={(e) => setCityInput(e.target.value)}
              placeholder="Search city..."
              className="weather-input"
            />
            <button type="submit" className="weather-btn">Search</button>
          </form>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="home-section">
        <h2 className="section-title">Quick Stats</h2>
        <ul className="stats-grid">
          <li className="stat-item">Emails: 5</li>
          <li className="stat-item">Tasks: 3</li>
          <li className="stat-item">Reminders: 2</li>
        </ul>
      </section>

      {/* Capabilities */}
      <section className="home-section">
        <h2 className="section-title">What I can do for you</h2>
        <ul className="capabilities">
          <li className="capability-item">Check emails</li>
          <li className="capability-item">Organize files</li>
          <li className="capability-item">Set reminders</li>
          <li className="capability-item">Show system info</li>
          <li className="capability-item">Live weather updates</li>
        </ul>
      </section>
    </div>
  );
}

export default Home;

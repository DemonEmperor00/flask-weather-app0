const API_KEY = 'ae9d892d339e5d9da64b19b7a4254bc7';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const cityInput = document.getElementById('city_input');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const city = cityInput.value.trim();
    if (!city) return;

    try {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`
      );
      const data = await response.json();

      if (data.cod !== 200) {
        alert(`Error: ${data.message}`);
        return;
      }

      // Store data and redirect
      localStorage.setItem('weatherData', JSON.stringify(data));
      window.location.href = 'results.html';
    } catch (error) {
      console.error('Fetch error:', error);
      alert('Unable to retrieve weather data.');
    }
  });
});
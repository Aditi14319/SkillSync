const sliderFields = [
  ['coding_interest', 'Coding interest'],
  ['writing_interest', 'Writing interest'],
  ['design_interest', 'Design interest'],
  ['law_interest', 'Law interest'],
  ['medical_interest', 'Medical interest'],
  ['math_comfort', 'Math comfort'],
  ['empathy', 'Empathy'],
  ['public_speaking', 'Public speaking'],
  ['problem_solving', 'Problem solving'],
  ['creativity', 'Creativity'],
  ['biology_interest', 'Biology interest'],
  ['portfolio_preference', 'Portfolio preference'],
  ['work_environment', 'Work environment']
];

const sliderGrid = document.getElementById('sliderGrid');
const resultsContainer = document.getElementById('resultsContainer');
const topResult = document.getElementById('topResult');
const statusText = document.getElementById('statusText');

sliderFields.forEach(([key, label]) => {
  const card = document.createElement('div');
  card.className = 'slider-card';
  card.innerHTML = `
    <div class="slider-head">
      <span>${label}</span>
      <strong id="${key}Value">5</strong>
    </div>
    <input type="range" id="${key}" min="0" max="10" value="5" />
  `;
  sliderGrid.appendChild(card);
  const range = card.querySelector('input');
  const valueNode = card.querySelector('strong');
  range.addEventListener('input', () => valueNode.textContent = range.value);
});

document.getElementById('recommendationForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  statusText.textContent = 'Generating recommendations...';
  const payload = {};
  sliderFields.forEach(([key]) => payload[key] = Number(document.getElementById(key).value));
  payload.subject_preference = document.getElementById('subject_preference').value;
  try {
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    renderResults(data.recommendations || []);
    statusText.textContent = '';
  } catch (error) {
    statusText.textContent = 'Could not connect to the recommendation engine.';
  }
});

function renderResults(items) {
  resultsContainer.innerHTML = '';
  topResult.innerHTML = '';
  if (!items.length) {
    resultsContainer.innerHTML = '<div class="empty-state">No recommendations found.</div>';
    return;
  }
  const first = items[0];
  topResult.innerHTML = `
    <div class="featured">
      <span class="badge">Top fit</span>
      <h3>${first.career}</h3>
      <p>${first.explanation}</p>
      <strong>Match score: ${first.score}</strong>
    </div>
  `;
  items.forEach(item => {
    const el = document.createElement('article');
    el.className = 'career-card';
    el.innerHTML = `
      <div class="career-top">
        <div>
          <h3>${item.career}</h3>
          <p>${item.explanation}</p>
        </div>
        <div class="score">${item.score}</div>
      </div>
      <h4>Suggested bachelor degrees</h4>
      <ul>${item.degrees.map(deg => `<li>${deg}</li>`).join('')}</ul>
    `;
    resultsContainer.appendChild(el);
  });
}

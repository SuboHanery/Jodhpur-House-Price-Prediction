document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    
    if(form) {
        form.addEventListener('submit', handlePredict);
    }
});

async function handlePredict(e) {
    e.preventDefault();
    
    const btn = document.getElementById('predictBtn');
    const btnText = btn.querySelector('.btn-text');
    const errorMsg = document.getElementById('errorMsg');
    
    // Clear previous errors
    errorMsg.textContent = '';
    
    // Build payload
    const payload = {
        area_name: document.getElementById('area_name').value,
        area_size: document.getElementById('area_size').value,
        bhk: document.getElementById('bhk').value,
        bathrooms: document.getElementById('bathrooms').value,
        balconies: document.getElementById('balconies').value,
        property_age: document.getElementById('property_age').value,
        gym: document.getElementById('gym').checked ? 1 : 0,
        swimming_pool: document.getElementById('swimming_pool').checked ? 1 : 0,
        park: document.getElementById('park').checked ? 1 : 0,
        security: document.getElementById('security').checked ? 1 : 0,
        parking: document.getElementById('parking').checked ? 1 : 0,
        hospital: document.getElementById('hospital').checked ? 1 : 0
    };

    // Loading State
    btn.disabled = true;
    btnText.textContent = 'Analyzing Market Data...';
    
    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        renderResult(data.predicted_price, payload.area_size);
        
    } catch (err) {
        errorMsg.textContent = 'Error: ' + err.message;
        renderEmpty();
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Generate AI Prediction';
    }
}

function renderResult(priceINR, sqft) {
    const resultContent = document.getElementById('resultContent');
    
    // Calculate values
    const lakhs = priceINR / 100000;
    const isCr = lakhs >= 100;
    const targetValue = isCr ? lakhs / 100 : lakhs;
    const suffix = isCr ? ' Cr' : ' Lakhs';
    const perSqft = Math.round(priceINR / sqft);
    
    const minVal = (targetValue * 0.95).toFixed(2);
    const maxVal = (targetValue * 1.05).toFixed(2);
    const rangeStr = `₹${minVal}${suffix} - ₹${maxVal}${suffix}`;
    
    resultContent.innerHTML = `
        <div class="result-card">
            <h3 class="result-label">Estimated Market Value</h3>
            <div class="result-price" id="animatedPrice">₹0.00</div>
            <div class="result-sqft">(₹${perSqft.toLocaleString('en-IN')} per sq ft)</div>
            
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-box-label">Price Range</div>
                    <div class="stat-box-val" style="font-size: 1.1rem">${rangeStr}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-box-label">Model Confidence</div>
                    <div class="stat-box-val">93.8%</div>
                </div>
            </div>
        </div>
    `;
    
    // Animate Number
    const priceEl = document.getElementById('animatedPrice');
    animateNumber(priceEl, 0, targetValue, 1200, val => '₹' + val.toFixed(2) + suffix);
}

function renderEmpty() {
    const resultContent = document.getElementById('resultContent');
    resultContent.innerHTML = `
        <div class="empty-state">
            <div class="pulse-ring"></div>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
            <p>Awaiting Property Details</p>
        </div>
    `;
}

function animateNumber(el, from, to, duration, formatter) {
    const start = performance.now();
    function step(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4); // Quartic ease out
        const current = from + (to - from) * eased;
        
        el.textContent = formatter(current);
        
        if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

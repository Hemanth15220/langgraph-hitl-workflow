let currentPostIndex = 0;
let allCryptos = [];
let currentPosts = [];

document.getElementById('startBtn').addEventListener('click', startWorkflow);
document.getElementById('searchInput').addEventListener('input', filterCryptos);

async function startWorkflow() {
    const btn = document.getElementById('startBtn');
    const status = document.getElementById('status');
    btn.disabled = true;
    status.textContent = '⏳ Fetching live data...';
    try {
        const response = await fetch('/api/start', {method: 'POST', headers: {'Content-Type': 'application/json'}});
        const data = await response.json();
        if (data.success) {
            status.textContent = '✅ Data loaded! Select a crypto';
            displayCryptos(data.trends.trending_films);
            allCryptos = data.trends.trending_films;
        } else {
            status.textContent = 'Error: ' + data.error;
        }
    } catch (error) {
        status.textContent = 'Error: ' + error.message;
    } finally {
        btn.disabled = false;
    }
}

function displayCryptos(cryptos) {
    const container = document.getElementById('cryptoGrid');
    if (!cryptos || cryptos.length === 0) {
        container.innerHTML = '<p class="placeholder">No cryptos found</p>';
        return;
    }
    let html = '';
    cryptos.forEach((crypto, index) => {
        const changeClass = crypto.change_24h >= 0 ? 'positive' : 'negative';
        const changeSymbol = crypto.change_24h >= 0 ? '📈' : '📉';
        html += '<div class="crypto-card" onclick="selectCrypto(\'' + crypto.id + '\', ' + index + ')"><img src="' + (crypto.image || '') + '" class="crypto-image" onerror="this.style.display=\'none\'"><div class="crypto-info"><div class="crypto-name">' + crypto.title + '</div><div class="crypto-symbol">' + crypto.symbol + '</div><div class="crypto-price">$' + (crypto.price || 0).toLocaleString() + '</div><div class="crypto-change ' + changeClass + '">' + changeSymbol + ' ' + (crypto.change_24h || 0).toFixed(2) + '%</div></div></div>';
    });
    container.innerHTML = html;
}

function filterCryptos() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allCryptos.filter(c => c.title.toLowerCase().includes(searchTerm) || c.symbol.toLowerCase().includes(searchTerm));
    displayCryptos(filtered);
}

async function selectCrypto(cryptoId, index) {
    const detailsSection = document.getElementById('detailsSection');
    const detailsContainer = document.getElementById('detailsContainer');
    try {
        const response = await fetch('/api/crypto/' + cryptoId);
        const details = await response.json();
        if (details.error) {
            detailsContainer.innerHTML = '<p class="placeholder">Error loading details</p>';
            return;
        }
        let html = '<div style="margin-bottom: 20px;"><h3>' + details.name + ' (' + details.symbol + ')</h3><p>' + (details.description || 'N/A').substring(0, 200) + '...</p></div>';
        html += '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">';
        html += '<div class="detail-item"><div class="detail-label">Price</div><div class="detail-value">$' + (details.price || 0).toLocaleString() + '</div></div>';
        html += '<div class="detail-item"><div class="detail-label">Market Cap</div><div class="detail-value">$' + (details.market_cap || 0).toLocaleString() + '</div></div>';
        html += '<div class="detail-item"><div class="detail-label">24h Volume</div><div class="detail-value">$' + (details.volume_24h || 0).toLocaleString() + '</div></div>';
        html += '<div class="detail-item"><div class="detail-label">ATH</div><div class="detail-value">$' + (details.ath || 0).toLocaleString() + '</div></div></div>';
        detailsContainer.innerHTML = html;
        detailsSection.style.display = 'block';
        generatePostsForCrypto(allCryptos[index]);
    } catch (error) {
        detailsContainer.innerHTML = '<p class="placeholder">Error: ' + error.message + '</p>';
    }
}

function generatePostsForCrypto(crypto) {
    currentPosts = [
        crypto.symbol + ' at $' + crypto.price + ' | Change: ' + crypto.change_24h.toFixed(2) + '% | Market Cap: $' + (crypto.market_cap || 0).toLocaleString() + '\n\nWhat\'s your take on the current price?',
        'Comparing ' + crypto.symbol + ' across the market - Current price $' + crypto.price + ' vs ATH. Do you think we\'ll recover?',
        crypto.symbol + ' Trading Analysis: ' + (crypto.change_24h >= 0 ? 'UP' : 'DOWN') + ' ' + Math.abs(crypto.change_24h).toFixed(2) + '%\n\nWhat\'s driving this movement? Share your thoughts!'
    ];
    let html = '';
    currentPosts.forEach((post, i) => {
        html += '<div class="post-item" onclick="selectPost(' + i + ')"><p>' + post + '</p></div>';
    });
    document.getElementById('contentContainer').innerHTML = html;
    document.getElementById('actionButtons').style.display = 'none';
}

function selectPost(index) {
    currentPostIndex = index;
    document.querySelectorAll('.post-item').forEach(el => el.classList.remove('selected'));
    document.querySelectorAll('.post-item')[index].classList.add('selected');
    document.getElementById('actionButtons').style.display = 'flex';
}

async function approvePost() {
    const selectedPost = document.querySelector('.post-item.selected');
    if (!selectedPost) {
        document.getElementById('status').textContent = 'Select a post first';
        return;
    }
    const postContent = selectedPost.textContent;
    document.getElementById('status').textContent = 'Publishing...';
    try {
        const response = await fetch('/api/approve', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({post_index: currentPostIndex, post_content: postContent})});
        const data = await response.json();
        if (data.success) {
            document.getElementById('status').textContent = 'Published!';
            document.getElementById('publicationContainer').innerHTML = '<div style="background: #f0fff4; border: 2px solid #48bb78; padding: 20px; border-radius: 8px;"><h3 style="color: #48bb78;">Published to r/CryptoTrends!</h3><p>' + postContent + '</p><p>' + new Date().toLocaleString() + '</p></div>';
        }
    } catch (error) {
        document.getElementById('status').textContent = 'Error: ' + error.message;
    }
}

function rejectPost() {
    document.getElementById('status').textContent = 'Skipped';
    document.getElementById('actionButtons').style.display = 'none';
}

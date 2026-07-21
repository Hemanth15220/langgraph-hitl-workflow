let allCryptos = [];
let selectedCrypto = null;
let comparisonCryptos = [];
let watchlist = [];

document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const searchInput = document.getElementById('searchInput');
    
    loadWatchlist();
    
    if (startBtn) startBtn.addEventListener('click', loadCryptos);
    if (searchInput) searchInput.addEventListener('input', filterCryptos);
});

function loadWatchlist() {
    const saved = localStorage.getItem('cryptoWatchlist');
    watchlist = saved ? JSON.parse(saved) : [];
    updateWatchlistCount();
}

function saveWatchlist() {
    localStorage.setItem('cryptoWatchlist', JSON.stringify(watchlist));
    updateWatchlistCount();
}

function updateWatchlistCount() {
    const count = document.getElementById('watchlistCount');
    if (count) count.textContent = watchlist.length;
}

function toggleWatchlist() {
    if (!selectedCrypto) return;
    
    const index = watchlist.findIndex(c => c.id === selectedCrypto.id);
    if (index > -1) {
        watchlist.splice(index, 1);
    } else {
        watchlist.push({id: selectedCrypto.id, name: selectedCrypto.title, symbol: selectedCrypto.symbol});
    }
    
    saveWatchlist();
    updateWatchlistButton();
    displayCryptoList(allCryptos);
}

function updateWatchlistButton() {
    const btn = document.getElementById('watchlistBtn');
    if (!btn || !selectedCrypto) return;
    
    const isWatched = watchlist.some(c => c.id === selectedCrypto.id);
    btn.textContent = isWatched ? '⭐ In Watchlist' : '☆ Add to Watchlist';
    btn.style.background = isWatched ? '#48bb78' : '#667eea';
}

async function loadCryptos() {
    const btn = document.getElementById('startBtn');
    const status = document.getElementById('status');
    
    btn.disabled = true;
    status.textContent = 'Loading cryptos...';
    
    try {
        const response = await fetch('/api/start', {method: 'POST', headers: {'Content-Type': 'application/json'}});
        const data = await response.json();
        
        if (data.success && data.cryptos) {
            allCryptos = data.cryptos;
            displayCryptoList(allCryptos);
            fetchBestTrades();
            status.textContent = 'Loaded ' + allCryptos.length + ' cryptos. Select one →';
        } else {
            status.textContent = 'Error loading data';
        }
    } catch (error) {
        status.textContent = 'Error: ' + error.message;
    } finally {
        btn.disabled = false;
    }
}

async function fetchBestTrades() {
    try {
        const response = await fetch('/api/best-trades');
        const data = await response.json();
        
        if (data.success) {
            displayBestTrades(data.trades);
        }
    } catch (error) {
        console.error('Error fetching best trades:', error);
    }
}

function displayBestTrades(trades) {
    const card = document.getElementById('bestTradesCard');
    if (!card) return;
    
    let buyHtml = '';
    if (trades.best_buys && trades.best_buys.length > 0) {
        trades.best_buys.forEach((buy, i) => {
            buyHtml += '<div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #c6f6d5;">';
            buyHtml += '<div style="font-weight: 700; color: #22543d;">#' + (i+1) + ' ' + buy.symbol + '</div>';
            buyHtml += '<p style="font-size: 0.85em; color: #22543d; margin: 5px 0;">' + buy.reason + '</p>';
            buyHtml += '<div style="font-size: 0.8em; color: #48bb78; font-weight: 600;">Target: ' + buy.price_target + '</div>';
            buyHtml += '</div>';
        });
    }
    document.getElementById('bestBuysContent').innerHTML = buyHtml;
    
    let sellHtml = '';
    if (trades.best_sells && trades.best_sells.length > 0) {
        trades.best_sells.forEach((sell, i) => {
            sellHtml += '<div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #fed7d7;">';
            sellHtml += '<div style="font-weight: 700; color: #742a2a;">#' + (i+1) + ' ' + sell.symbol + '</div>';
            sellHtml += '<p style="font-size: 0.85em; color: #742a2a; margin: 5px 0;">' + sell.reason + '</p>';
            sellHtml += '<div style="font-size: 0.8em; color: #f56565; font-weight: 600;">Profit Target: ' + sell.target_profit + '</div>';
            sellHtml += '</div>';
        });
    }
    document.getElementById('bestSellsContent').innerHTML = sellHtml;
    
    document.getElementById('marketOutlook').textContent = trades.market_outlook || 'Market analysis in progress...';
    
    card.style.display = 'block';
}

function displayCryptoList(cryptos) {
    const container = document.getElementById('cryptoList');
    if (!container) return;
    
    if (!cryptos || cryptos.length === 0) {
        container.innerHTML = '<p class="empty-state">No cryptos found</p>';
        return;
    }
    
    let html = '';
    cryptos.forEach((crypto, index) => {
        const changeClass = crypto.change_24h >= 0 ? 'positive' : 'negative';
        const changeSymbol = crypto.change_24h >= 0 ? '📈' : '📉';
        const isWatched = watchlist.some(c => c.id === crypto.id);
        
        html += '<div class="crypto-item' + (selectedCrypto && selectedCrypto.id === crypto.id ? ' selected' : '') + '" onclick="selectCrypto(\'' + crypto.id + '\', ' + index + ')">';
        html += '<div class="crypto-item-name">' + crypto.title + '</div>';
        html += '<div class="crypto-item-symbol">' + crypto.symbol + '</div>';
        html += '<div class="crypto-item-price">$' + (crypto.price || 0).toLocaleString('en-US', {maximumFractionDigits: 2}) + '</div>';
        html += '<div class="crypto-item-change ' + changeClass + '">' + changeSymbol + ' ' + (crypto.change_24h || 0).toFixed(2) + '%</div>';
        if (isWatched) html += '<div class="crypto-item-watchlist">⭐</div>';
        html += '</div>';
    });
    
    container.innerHTML = html;
}

function filterCryptos() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allCryptos.filter(c => 
        c.title.toLowerCase().includes(searchTerm) || 
        c.symbol.toLowerCase().includes(searchTerm)
    );
    displayCryptoList(filtered);
}

async function selectCrypto(cryptoId, index) {
    selectedCrypto = allCryptos[index];
    displayCryptoList(allCryptos);
    
    const header = document.getElementById('cryptoHeader');
    if (header) {
        document.getElementById('cryptoImage').src = selectedCrypto.image;
        document.getElementById('cryptoName').textContent = selectedCrypto.title;
        document.getElementById('cryptoSymbol').textContent = selectedCrypto.symbol;
        document.getElementById('cryptoPrice').textContent = '$' + (selectedCrypto.price || 0).toLocaleString('en-US', {maximumFractionDigits: 2});
        const changeSpan = document.getElementById('cryptoChange');
        changeSpan.textContent = (selectedCrypto.change_24h >= 0 ? '📈 ' : '📉 ') + (selectedCrypto.change_24h || 0).toFixed(2) + '%';
        changeSpan.className = 'change ' + (selectedCrypto.change_24h >= 0 ? 'positive' : 'negative');
        header.style.display = 'flex';
    }
    
    updateWatchlistButton();
    
    const loading = document.getElementById('loadingIndicator');
    if (loading) loading.style.display = 'flex';
    
    try {
        const detailsResponse = await fetch('/api/crypto/' + cryptoId);
        const details = await detailsResponse.json();
        
        const researchResponse = await fetch('/api/research/' + cryptoId);
        const research = await researchResponse.json();
        
        if (loading) loading.style.display = 'none';
        
        if (research.success) {
            displayRiskAnalysis(research.risk_analysis);
            displayOpportunityAnalysis(research.opportunity_analysis);
            displayResearchSynthesis(research.research_synthesis);
        }
        
        displayMarketDetails(details);
        showComparisonSection();
    } catch (error) {
        if (loading) loading.style.display = 'none';
        document.getElementById('status').textContent = 'Error: ' + error.message;
    }
}

function displayRiskAnalysis(data) {
    const card = document.getElementById('riskCard');
    const content = document.getElementById('riskContent');
    
    if (!card || !content) return;
    
    const riskScore = data.risk_score || 5;
    const scoreClass = riskScore <= 3 ? 'low' : riskScore <= 7 ? 'medium' : 'high';
    
    let html = '<p><strong>Main Concern:</strong> ' + (data.main_concern || 'N/A') + '</p>';
    html += '<p><strong>Severity:</strong> ' + (data.severity || 'N/A') + '</p>';
    html += '<strong>Risk Factors:</strong><ul class="risk-list">';
    
    if (data.risks && Array.isArray(data.risks)) {
        data.risks.forEach(risk => {
            html += '<li>' + risk + '</li>';
        });
    }
    
    html += '</ul>';
    
    content.innerHTML = html;
    card.style.display = 'block';
    document.querySelector('#riskCard .score-badge').textContent = riskScore + '/10';
    document.querySelector('#riskCard .score-badge').className = 'score-badge ' + scoreClass;
}

function displayOpportunityAnalysis(data) {
    const card = document.getElementById('opportunityCard');
    const content = document.getElementById('opportunityContent');
    
    if (!card || !content) return;
    
    const oppScore = data.opportunity_score || 5;
    const scoreClass = oppScore <= 3 ? 'low' : oppScore <= 7 ? 'medium' : 'high';
    
    let html = '<p><strong>Upside Potential:</strong> ' + (data.upside_potential || 'N/A') + '</p>';
    html += '<p><strong>Entry Point:</strong> ' + (data.entry_point || 'N/A') + '</p>';
    html += '<p><strong>Target Price Range:</strong> ' + (data.target_price_range || 'N/A') + '</p>';
    html += '<strong>Catalysts:</strong><ul class="opportunity-list">';
    
    if (data.catalysts && Array.isArray(data.catalysts)) {
        data.catalysts.forEach(catalyst => {
            html += '<li>' + catalyst + '</li>';
        });
    }
    
    html += '</ul>';
    
    content.innerHTML = html;
    card.style.display = 'block';
    document.querySelector('#opportunityCard .score-badge').textContent = oppScore + '/10';
    document.querySelector('#opportunityCard .score-badge').className = 'score-badge ' + scoreClass;
}

function displayResearchSynthesis(data) {
    const card = document.getElementById('synthesisCard');
    const content = document.getElementById('synthesisContent');
    
    if (!card || !content) return;
    
    const verdict = (data.verdict || 'HOLD').toUpperCase();
    const verdictClass = 'verdict-' + verdict.toLowerCase();
    
    let html = '<div class="thesis-box"><strong>Investment Thesis:</strong><p>' + (data.investment_thesis || 'N/A') + '</p></div>';
    html += '<p><strong>Key Metrics:</strong><ul class="risk-list">';
    
    if (data.key_metrics && Array.isArray(data.key_metrics)) {
        data.key_metrics.forEach(metric => {
            html += '<li>' + metric + '</li>';
        });
    }
    
    html += '</ul></p>';
    html += '<p><strong>Timeline:</strong> ' + (data.timeline || 'N/A') + '</p>';
    html += '<div class="verdict-badge ' + verdictClass + '">' + verdict + '</div>';
    
    content.innerHTML = html;
    card.style.display = 'block';
}

function displayMarketDetails(details) {
    const card = document.getElementById('detailsCard');
    const content = document.getElementById('detailsContent');
    
    if (!card || !content) return;
    
    let html = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">';
    html += '<div><strong>Market Cap Rank:</strong><br/>#' + (details.market_cap_rank || 'N/A') + '</div>';
    html += '<div><strong>Market Cap:</strong><br/>$' + (details.market_cap || 0).toLocaleString('en-US', {notation: 'compact'}) + '</div>';
    html += '<div><strong>Volume (24h):</strong><br/>$' + (details.volume_24h || 0).toLocaleString('en-US', {notation: 'compact'}) + '</div>';
    html += '<div><strong>Circulating Supply:</strong><br/>' + (details.circulating_supply || 0).toLocaleString('en-US', {notation: 'compact'}) + '</div>';
    html += '<div><strong>ATH:</strong><br/>$' + (details.ath || 0).toLocaleString('en-US', {maximumFractionDigits: 2}) + '</div>';
    html += '<div><strong>ATL:</strong><br/>$' + (details.atl || 0).toLocaleString('en-US', {maximumFractionDigits: 2}) + '</div>';
    html += '</div>';
    html += '<p style="margin-top: 15px; color: #718096;">' + (details.description || 'No description available') + '</p>';
    
    if (details.website) {
        html += '<p style="margin-top: 10px;"><a href="' + details.website + '" target="_blank" style="color: #667eea;">🔗 Visit Website</a></p>';
    }
    
    content.innerHTML = html;
    card.style.display = 'block';
}

function showComparisonSection() {
    const section = document.getElementById('comparisonSection');
    if (section) section.style.display = 'block';
}

function addToComparison() {
    const input = document.getElementById('compareInput');
    if (!input || !input.value.trim()) {
        return;
    }
    
    const searchTerm = input.value.trim().toUpperCase();
    
    const crypto = allCryptos.find(c => 
        c.symbol === searchTerm || 
        c.title.toUpperCase() === searchTerm
    );
    
    if (!crypto) {
        alert('Crypto not found. Try: BTC, ETH, SOL, ADA, etc.');
        return;
    }
    
    if (comparisonCryptos.some(c => c.id === crypto.id)) {
        alert(crypto.symbol + ' already added');
        return;
    }
    
    if (comparisonCryptos.length >= 5) {
        alert('Max 5 cryptos');
        return;
    }
    
    comparisonCryptos.push(crypto);
    input.value = '';
    displayComparison();
}

function removeFromComparison(index) {
    comparisonCryptos.splice(index, 1);
    displayComparison();
}

function clearComparison() {
    comparisonCryptos = [];
    document.getElementById('comparisonContent').innerHTML = '<p class="empty-state">Add cryptos to compare</p>';
}

function displayComparison() {
    const content = document.getElementById('comparisonContent');
    if (!content) return;
    
    if (comparisonCryptos.length === 0) {
        content.innerHTML = '<p class="empty-state">Add cryptos to compare (try: BTC, ETH, SOL)</p>';
        return;
    }
    
    let html = '<table class="comparison-table"><thead><tr><th>Metric</th>';
    comparisonCryptos.forEach(c => {
        html += '<th>' + c.symbol + '</th>';
    });
    html += '</tr></thead><tbody>';
    
    html += '<tr><td><strong>Price</strong></td>';
    comparisonCryptos.forEach(c => {
        html += '<td>$' + (c.price || 0).toLocaleString('en-US', {maximumFractionDigits: 2}) + '</td>';
    });
    html += '</tr>';
    
    html += '<tr><td><strong>Market Cap</strong></td>';
    comparisonCryptos.forEach(c => {
        html += '<td>$' + (c.market_cap || 0).toLocaleString('en-US', {notation: 'compact'}) + '</td>';
    });
    html += '</tr>';
    
    html += '<tr><td><strong>24h Change</strong></td>';
    comparisonCryptos.forEach(c => {
        const changeClass = c.change_24h >= 0 ? 'positive' : 'negative';
        html += '<td class="' + changeClass + '">' + (c.change_24h || 0).toFixed(2) + '%</td>';
    });
    html += '</tr>';
    
    html += '<tr><td><strong>Volume (24h)</strong></td>';
    comparisonCryptos.forEach(c => {
        html += '<td>$' + (c.volume_24h || 0).toLocaleString('en-US', {notation: 'compact'}) + '</td>';
    });
    html += '</tr>';
    
    html += '<tr><td><strong>Market Cap Rank</strong></td>';
    comparisonCryptos.forEach(c => {
        html += '<td>#' + (c.market_cap_rank || 'N/A') + '</td>';
    });
    html += '</tr>';
    
    html += '</tbody></table>';
    
    html += '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">';
    comparisonCryptos.forEach((c, i) => {
        html += '<button class="btn btn-small btn-danger" onclick="removeFromComparison(' + i + ')">✕ ' + c.symbol + '</button>';
    });
    html += '</div>';
    
    content.innerHTML = html;
}

// ============ تحديث الوقت والتاريخ ============
function updateTimestamp() {
    const timestamp = document.getElementById('timestamp');
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    timestamp.textContent = now.toLocaleDateString('ar-SA', options);
}

setInterval(updateTimestamp, 1000);
updateTimestamp();

// ============ البيانات الوهمية للرسوم البيانية ============
const priceData = {
    labels: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
    datasets: [{
        label: 'سعر الذهب',
        data: [2048, 2050, 2047, 2052, 2055, 2053, 2058, 2061, 2059, 2050],
        borderColor: '#FFD700',
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#FFD700',
        pointBorderColor: '#1a1a1a',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
    }]
};

const equityData = {
    labels: ['يوم 1', 'يوم 2', 'يوم 3', 'يوم 4', 'يوم 5', 'يوم 6', 'يوم 7'],
    datasets: [{
        label: 'منحنى الإيكويتي',
        data: [10000, 10150, 10280, 10420, 10350, 10500, 10650],
        borderColor: '#00D4FF',
        backgroundColor: 'rgba(0, 212, 255, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#00D4FF',
        pointBorderColor: '#1a1a1a',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
    }]
};

const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            display: true,
            labels: {
                color: '#e0e0e0',
                font: {
                    size: 12,
                    weight: 'bold'
                },
                padding: 15
            }
        }
    },
    scales: {
        y: {
            beginAtZero: false,
            grid: {
                color: '#3a3a3a',
                drawBorder: false
            },
            ticks: {
                color: '#e0e0e0'
            }
        },
        x: {
            grid: {
                color: '#3a3a3a',
                drawBorder: false
            },
            ticks: {
                color: '#e0e0e0'
            }
        }
    }
};

// ============ إنشاء الرسوم البيانية ============
const priceChartCtx = document.getElementById('priceChart').getContext('2d');
const priceChart = new Chart(priceChartCtx, {
    type: 'line',
    data: priceData,
    options: chartOptions
});

const equityChartCtx = document.getElementById('equityChart').getContext('2d');
const equityChart = new Chart(equityChartCtx, {
    type: 'line',
    data: equityData,
    options: chartOptions
});

// ============ معالجة الأزرار ============
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const statusBadge = document.getElementById('statusBadge');
const statusText = document.getElementById('statusText');
const statusDot = document.querySelector('.status-dot');

let isRunning = false;

startBtn.addEventListener('click', () => {
    isRunning = true;
    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusBadge.classList.add('connected');
    statusDot.classList.add('connected');
    statusText.textContent = 'التداول قيد التشغيل';
    showNotification('تم بدء التداول بنجاح! 🚀', 'success');
});

stopBtn.addEventListener('click', () => {
    isRunning = false;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    statusBadge.classList.remove('connected');
    statusDot.classList.remove('connected');
    statusText.textContent = 'التداول متوقف';
    showNotification('تم إيقاف التداول بنجاح! ⛔', 'danger');
});

// ============ وظائف مساعدة ============
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // يمكن إضافة نظام إشعارات حقيقي هنا
}

function updatePrice(newPrice) {
    const priceElement = document.getElementById('currentPrice');
    priceElement.textContent = `$${newPrice.toFixed(2)}`;
}

function updateBalance(newBalance) {
    const balanceElement = document.getElementById('balance');
    balanceElement.textContent = `$${newBalance.toFixed(2)}`;
}

function updateEquity(newEquity) {
    const equityElement = document.getElementById('equity');
    equityElement.textContent = `$${newEquity.toFixed(2)}`;
}

function updateProfit(profitAmount) {
    const profitElement = document.getElementById('profit');
    profitElement.classList.remove('loss');
    profitElement.classList.add('profit');
    
    if (profitAmount < 0) {
        profitElement.classList.remove('profit');
        profitElement.classList.add('loss');
    }
    
    const symbol = profitAmount >= 0 ? '+' : '';
    profitElement.textContent = `${symbol}$${profitAmount.toFixed(2)}`;
}

// ============ تحديث البيانات كل 5 ثوان ============
function updateData() {
    if (isRunning) {
        // محاكاة تحديث الأسعار
        const randomPrice = 2050 + (Math.random() - 0.5) * 10;
        updatePrice(randomPrice);
        
        // محاكاة تحديث الرصيد
        const randomProfit = -500 + Math.random() * 3000;
        updateProfit(randomProfit);
    }
}

setInterval(updateData, 5000);

// ============ تحميل البيانات من الخادم ============
async function fetchData(endpoint) {
    try {
        const response = await fetch(`/api/${endpoint}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        return null;
    }
}

// ============ تحديث الإحصائيات ============
async function updateStatistics() {
    const stats = await fetchData('statistics');
    if (stats && stats.success) {
        // تحديث البيانات في الواجهة
        console.log('Statistics updated:', stats.data);
    }
}

// تحديث الإحصائيات كل دقيقة
setInterval(updateStatistics, 60000);
updateStatistics();

// ============ معالجة الصفقات ============
const tradesTableBody = document.getElementById('tradesTableBody');

function addTradeRow(trade) {
    const row = document.createElement('tr');
    const profitClass = trade.profit >= 0 ? 'profit' : 'loss';
    const symbol = trade.profit >= 0 ? '+' : '';
    
    row.innerHTML = `
        <td>${trade.ticket}</td>
        <td><span class="badge ${trade.type === 'BUY' ? 'buy-badge' : 'sell-badge'}">${trade.type === 'BUY' ? 'شراء' : 'بيع'}</span></td>
        <td>${trade.volume}</td>
        <td>$${trade.entry_price.toFixed(2)}</td>
        <td>$${trade.current_price.toFixed(2)}</td>
        <td class="${profitClass}">${symbol}$${Math.abs(trade.profit).toFixed(2)}</td>
        <td><button class="btn btn-sm btn-danger" onclick="closeTrade(${trade.ticket})">إغلاق</button></td>
    `;
    tradesTableBody.appendChild(row);
}

function closeTrade(ticket) {
    fetch(`/api/close-trade/${ticket}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`تم إغلاق الصفقة ${ticket} بنجاح!`, 'success');
                // إعادة تحميل الصفقات
                location.reload();
            } else {
                showNotification(`فشل إغلاق الصفقة: ${data.error}`, 'danger');
            }
        })
        .catch(error => console.error('Error:', error));
}

// ============ معالجات الأحداث ============
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Dashboard loaded successfully!');
    updateTimestamp();
});

// Prevent page reload on unintended clicks
window.addEventListener('beforeunload', (event) => {
    if (isRunning) {
        event.preventDefault();
        event.returnValue = 'هل أنت متأكد من رغبتك في المغادرة أثناء التداول؟';
    }
});

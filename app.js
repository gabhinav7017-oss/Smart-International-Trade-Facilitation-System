async function calculateRoute() {
    try {
        const start = document.getElementById('route-start').value;
        const end = document.getElementById('route-end').value;
        
        const res = await fetch(`/api/route?start=${start}&end=${end}`);
        const data = await res.json();
        const box = document.getElementById('route-result');
        const val = document.getElementById('route-val');
        
        if (data.path.length === 0) {
            val.innerHTML = `<div style="color: #ff6b6b;">${data.time}</div>`;
        } else {
            val.innerHTML = `
                <div style="font-size: 0.9rem; color: #a0a0a0; margin-bottom: 0.5rem;">Path: ${data.path.join(' ➔ ')}</div>
                <div style="color: #fff;">Estimated Transit: <span style="color: var(--primary-yellow);">${data.time} Days</span></div>
            `;
        }
        box.classList.add('show');
    } catch (err) {
        console.error("API Error", err);
    }
}

async function optimizeLoad() {
    try {
        const cap = document.getElementById('load-capacity').value || 20;
        const res = await fetch(`/api/optimize?capacity=${cap}`);
        const data = await res.json();
        const box = document.getElementById('load-result');
        const val = document.getElementById('load-val');
        
        const itemsList = data.items.map(i => i.name).join(', ');
        
        val.innerHTML = `
            <div style="font-size: 0.9rem; color: #a0a0a0; margin-bottom: 0.5rem;">Capacity utilized: ${cap} Tons</div>
            <div style="font-size: 0.9rem; color: #a0a0a0; margin-bottom: 0.5rem;">Selected: ${itemsList || 'None'}</div>
            <div style="color: #fff;">Maximum Profit Yield: <span style="color: var(--primary-yellow);">$${data.profit.toLocaleString()}</span></div>
        `;
        box.classList.add('show');
    } catch (err) {
        console.error("API Error", err);
    }
}

async function addCustoms() {
    try {
        const id = document.getElementById('customs-id').value || 'CONT-' + Math.floor(Math.random()*1000);
        const type = document.getElementById('customs-type').value;
        const res = await fetch(`/api/customs/add?id=${id}&type=${type}`);
        const data = await res.json();
        
        const box = document.getElementById('customs-result');
        const val = document.getElementById('customs-val');
        document.getElementById('customs-id').value = ''; // clear input
        
        val.innerHTML = `<div style="color: #81ff89;">Shipment ${data.id} added to the priority queue.</div>`;
        box.classList.add('show');
    } catch (err) {
        console.error("API Error", err);
    }
}

async function processCustoms() {
    try {
        const res = await fetch('/api/customs');
        const data = await res.json();
        const box = document.getElementById('customs-result');
        const val = document.getElementById('customs-val');
        
        if (data.status === 'empty') {
            val.innerHTML = `<div style="color: #a0a0a0;">No pending shipments in queue.</div>`;
        } else {
            val.innerHTML = `
                <div style="font-size: 0.9rem; color: #a0a0a0; margin-bottom: 0.5rem;">ID: ${data.shipment.id} — ${data.shipment.type}</div>
                <div style="color: #fff;">Priority Score: <span style="color: var(--primary-yellow);">${data.priority}</span></div>
            `;
        }
        box.classList.add('show');
    } catch (err) {
        console.error("API Error", err);
    }
}

async function allocateStorage() {
    try {
        const res = await fetch('/api/storage');
        const data = await res.json();
        const box = document.getElementById('storage-result');
        const val = document.getElementById('storage-val');
        
        let htmlContent = `<div style="font-size: 0.9rem; color: #a0a0a0; margin-bottom: 0.5rem;">Total Safe Zones Required: <span style="color: #fff; font-weight: bold;">${data.zones_needed}</span></div>`;
        
        for (const [zone, materials] of Object.entries(data.allocation)) {
            htmlContent += `<div style="color: #fff; margin-top: 5px;">${zone}: <span style="color: var(--primary-yellow);">${materials.join(', ')}</span></div>`;
        }
        
        val.innerHTML = htmlContent;
        box.classList.add('show');
    } catch (err) {
        console.error("API Error", err);
    }
}

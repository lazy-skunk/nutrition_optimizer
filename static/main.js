document.addEventListener("DOMContentLoaded", function() {
    fetch('static/nutrition_data.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('tableBody');
            data.forEach(row => {
                const tr = document.createElement('tr');
                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});

function filterTable() {
    const keyword = document.getElementById('search').value.toLowerCase();
    const table = document.getElementById('nutritionTable');
    const rows = table.getElementsByTagName('tr');
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let matched = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().includes(keyword)) {
                matched = true;
                break;
            }
        }
        rows[i].style.display = matched ? '' : 'none';
    }
}

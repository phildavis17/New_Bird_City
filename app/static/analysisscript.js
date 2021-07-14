// Change 0.0 to gray color
// Change text of values above 0.99 to ">99%"

function toggleActive() {
    const cbs = document.getElementsByClassName("includeCB");
    for (let cb of cbs) {
        let items = document.getElementsByClassName(cb.name);
        if (cb.checked == true) {
            for (let i of items) {
                i.classList.remove("inactive");
            };
        } else {
            for (let i of items) {
                i.classList.add("inactive");
            };
        };
    };
};


function sortSp() {
    //console.log("sp sort")
    const spTable = document.getElementById('sp-table');
    const tableBody = spTable.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    const newRows = Array.from(rows)
    newRows.sort(function(rowA, rowB) {
        let cellA = rowA.querySelector('.sp-index-num').innerHTML;
        let cellB = rowB.querySelector('.sp-index-num').innerHTML;

        cellA = cellA.replace(/[^\. \d]/g, '');
        cellB = cellB.replace(/[^\. \d]/g, '');
        const numA = Number(cellA)
        const numB = Number(cellB)

        return numA - numB
    });
    [].forEach.call(rows, function(row) {
        tableBody.removeChild(row);
    });

    newRows.forEach(function(newRow) {
        tableBody.appendChild(newRow)
    });
};

function sortCumulative() {
    const spTable = document.getElementById('sp-table');
    const tableBody = spTable.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    const newRows = Array.from(rows)
    newRows.sort(function(rowA, rowB) {
        let cellA = rowA.querySelector('.cumulativeObs').innerHTML;
        let cellB = rowB.querySelector('.cumulativeObs').innerHTML;

        cellA = cellA.replace(/[^\. \d]/g, '');
        cellB = cellB.replace(/[^\. \d]/g, '');
        const numA = Number(cellA)
        const numB = Number(cellB)

        return numA - numB
    });
    [].forEach.call(rows, function(row) {
        tableBody.removeChild(row);
    });

    newRows.forEach(function(newRow) {
        tableBody.appendChild(newRow)
    });

};

function sortHS(hs) {
    alert(hs);
};
//let chkBxs  = document.querySelectorAll('input[class=includeCB]');



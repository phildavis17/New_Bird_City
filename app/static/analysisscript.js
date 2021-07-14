// Change 0.0 to gray color

const headers = document.getElementsByTagName("th")
let directions = Array.from(headers).map(function(header) {
    return 'asc';
});

let cumlativeDirection = 1;
let taxonDirection = 1;
let hsDirections = {};
//const hsHeaders = document.getElementsByClassName("header-hotspot");
//let hsDirections = Array.from(hsHeaders)

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

function numericalSortByIndex(index, multiplier) {
    const spTable = document.getElementById('sp-table');
    const tableBody = spTable.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    const newRows = Array.from(rows)
    newRows.sort(function(rowA, rowB) {
        let cellA = rowA.querySelector(index).innerHTML;
        let cellB = rowB.querySelector(index).innerHTML;

        cellA = cellA.replace(/[^\. \d]/g, '');
        cellB = cellB.replace(/[^\. \d]/g, '');
        const numA = Number(cellA) * multiplier;
        const numB = Number(cellB) * multiplier;

        return numA - numB;
    });
    [].forEach.call(rows, function(row) {
        tableBody.removeChild(row);
    });

    newRows.forEach(function(newRow) {
        tableBody.appendChild(newRow);
    });
};

function sortSp() {
    numericalSortByIndex('.sp-index-num', taxonDirection);
    taxonDirection *= -1;
};

function sortCumulative() {;
    numericalSortByIndex('.cumulativeObs', cumlativeDirection);
    cumlativeDirection *= -1;
};

function sortHS(hs) {
    //asc, desc
    if (hsDirections.hasOwnProperty(hs)) {
        hsDirections[hs] *= -1;
    } else {
        hsDirections[hs] = 1;
    };
    numericalSortByIndex('.' + hs, hsDirections[hs]);
};

// Some things to make the Analysis page more usable.

let cumlativeDirection = -1;
let taxonSortType = "alpha 1";
let hsDirections = {};

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

function alphaSortByIndex(index, multiplier) {
    const spTable = document.getElementById('sp-table');
    const tableBody = spTable.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    const newRows = Array.from(rows)
    newRows.sort(function(rowA, rowB) {
        let cellA = rowA.querySelector(index).innerHTML;
        let cellB = rowB.querySelector(index).innerHTML;

        switch (true) {
            case cellA > cellB: return 1 * multiplier;
            case cellA < cellB: return -1 * multiplier;
            case cellA === cellB: return 0;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        }
    });
    [].forEach.call(rows, function(row) {
        tableBody.removeChild(row);
    });

    newRows.forEach(function(newRow) {
        tableBody.appendChild(newRow);
    });
};

function sortSp() {
    // Sorts by positive Taxonomic, then positive alpha, then reverse alpha
    switch (taxonSortType) {
        case "alpha 1": 
            alphaSortByIndex('.spName', 1);
            taxonSortType = "alpha -1"
            break;
        case "alpha -1":
            alphaSortByIndex('.spName', -1);
            taxonSortType = "taxon";
            break;
        case "taxon":
            numericalSortByIndex('.sp-index-num', 1);
            taxonSortType = "alpha 1";
            break;
    }
    
    //reset other sort types
    cumlativeDirection = -1;
    hsDirections = {};
};

function sortCumulative() {;
    numericalSortByIndex('.cumulativeObs', cumlativeDirection);
    cumlativeDirection *= -1;
    
    // reset other sort types
    taxonSortType = "taxon";
    hsDirections = {};

};

function sortHS(hs) {
    if (hsDirections.hasOwnProperty(hs)) {
        hsDirections[hs] *= -1;
    } else {
        hsDirections[hs] = -1;
    };
    numericalSortByIndex('.' + hs, hsDirections[hs]);

    // reset other sort types
    cumlativeDirection = -1;
    taxonSortType = "taxon";
};

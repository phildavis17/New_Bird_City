// Change 0.0 to gray color
// Change text of values above 0.99 to ">99%"

function toggleActive() {
    const cbs = document.getElementsByClassName("includeCB");
    for (let cb of cbs) {
        let items = document.getElementsByClassName(cb.name);
        if (cb.checked == true) {
            for (let i of items) {
                i.classList.remove("inactive")
            }
        } else {
            for (let i of items) {
                i.classList.add("inactive")
            }
        }
    }
}


//let chkBxs  = document.querySelectorAll('input[class=includeCB]');



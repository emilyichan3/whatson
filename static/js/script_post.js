function init(){
    let action = document.getElementById('action').innerText;

    if (action === "add"){
        let default_formattedDate = document.getElementById('default_date').innerText;
        let date_from = document.getElementById('date_fm');
        let date_to = document.getElementById('date_to');
        date_from.value = formattedDate(default_formattedDate);
        date_to.value = formattedDate(default_formattedDate);
    } else {
        let edit_date_from = document.getElementById('edit_date_fm').innerText;
        let edit_date_to = document.getElementById('edit_date_to').innerText;
        let target_date_fm = document.getElementById('target_date_fm');
        let target_date_to = document.getElementById('target_date_to');
        target_date_fm.value = formattedDate(edit_date_from);
        target_date_to.value = formattedDate(edit_date_to);
    }
}

function formattedDate(targetDate){
    // Convert the date string to a JavaScript Date object
    let jsDate = new Date(targetDate);
    // Format jsDate to "yyyy-MM-dd"
    let year = jsDate.getFullYear();
    let month = String(jsDate.getMonth() + 1).padStart(2, '0');  // Months are zero-indexed
    let day = String(jsDate.getDate()).padStart(2, '0');

    let formattedDate =  `${year}-${month}-${day}`;
    return formattedDate;

}
addEventListener('load', init);

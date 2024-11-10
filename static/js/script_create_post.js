function init(){
    let default_formattedDate = document.getElementById('default_date').innerText;
    let date_from = document.getElementById('date_fm');
    let date_to = document.getElementById('date_to');

    // Convert the date string to a JavaScript Date object
    let jsDate = new Date(default_formattedDate);
    
    // Format jsDate to "yyyy-MM-dd"
    let year = jsDate.getFullYear();
    let month = String(jsDate.getMonth() + 1).padStart(2, '0');  // Months are zero-indexed
    let day = String(jsDate.getDate()).padStart(2, '0');

    let formattedDate = `${year}-${month}-${day}`;
    date_from.value = formattedDate;
    date_to.value = formattedDate;
}


addEventListener('load', init);

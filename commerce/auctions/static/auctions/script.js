window.addEventListener('DOMContedLoaded', (event) => {
	document.querySelector('.datapicker').datepicker();
});

function datePicker() {
	document.querySelector('#endDate').min = new Date().toISOString(0, 19);
}

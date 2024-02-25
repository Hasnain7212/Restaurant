document.addEventListener('DOMContentLoaded', function () {
    var payWithCard = document.getElementById('payWithCard');
    var cardDetailsForm = document.querySelector('.card-details');

    payWithCard.addEventListener('change', function () {
        if (this.checked) {
            cardDetailsForm.style.display = 'block';
        } else {
            cardDetailsForm.style.display = 'none';
        }
    });

    var payWithCash = document.getElementById('payWithCash');
    payWithCash.addEventListener('change', function () {
        if (this.checked) {
            cardDetailsForm.style.display = 'none';
        }
    });
});

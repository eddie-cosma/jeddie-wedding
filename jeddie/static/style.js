function contains_number(t) {
    var regex = /\d/g;
    return regex.test(t);
}

function toggle_menu_visibility() {
    var navbar = document.getElementsByTagName('nav')[0];
    if (navbar.className === '') {
        navbar.className = 'responsive';
    } else {
        navbar.className = '';
    }
}

function show_payment_modal(item_id) {
    let cash_check_form = document.getElementById('pay_by_cash_check')
    cash_check_form.action = 'promise/' + item_id
    let credit_card_form = document.getElementById('pay_by_credit_card')
    credit_card_form.action = 'pay/' + item_id

    let modal = document.getElementById('modal-overlay');
    modal.style.display = 'flex';
}

function hide_payment_modal() {
    if (event.target === event.currentTarget) {
        let modal = document.getElementById('modal-overlay');
        modal.style.display = 'none';
    }
}

function update_reservation_submit() {
    let any_coming = false
    let rsvps = document.querySelectorAll("input[type=radio][id$='_no'], input[type=radio][id$='_yes']")
    for (let i = 0; i < rsvps.length; i++) {
        if (rsvps[i].checked === true && rsvps[i].value === "1") {
            any_coming = true
        }
    }

    let submit_button = document.getElementById("next_submit")
    if (any_coming === true) {
        submit_button.value = 'Next'
    }
    else {
        submit_button.value = 'Submit'
    }
}
function toggle_menu_visibility() {
    var navbar = document.getElementsByTagName('nav')[0];
    if (navbar.className === '') {
        navbar.className = 'responsive';
    }
    else {
        navbar.className = '';
    }
}

function add_guests(new_guests) {
    let guest_box = document.getElementById('guests');

    for (let i = 0; i < new_guests; i++) {

        let first_name_label = document.createElement('label');
        first_name_label.innerText = 'First Name';
        first_name_label.htmlFor = 'first_name_add' + i;

        let first_name = document.createElement('input');
        first_name.type = 'text';
        first_name.name = 'first_name';
        first_name.id = 'first_name_add' + i;
        first_name.required = 'required';

        let last_name_label = document.createElement('label');
        last_name_label.innerText = 'Last Name';
        last_name_label.htmlFor = 'last_name_add' + i;

        let last_name = document.createElement('input');
        last_name.type = 'text';
        last_name.name = 'last_name';
        last_name.id = 'last_name_add' + i;
        last_name.required = 'required';

        guest_box.append(first_name_label);
        guest_box.append(first_name);
        guest_box.append(last_name_label);
        guest_box.append(last_name);
    }

    document.getElementById('add_guests_button').remove();
    document.getElementById('add_guests_notice').remove();
}
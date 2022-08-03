function toggle_menu_visibility() {
    var navbar = document.getElementsByTagName('nav')[0];
    if (navbar.className === '') {
        navbar.className = 'responsive';
    }
    else {
        navbar.className = '';
    }
}
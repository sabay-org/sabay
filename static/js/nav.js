/*
 * This file contains the js logic for the
 * mobile friendly nav bar
 */
const menuButton = document.querySelector('.hamburger-btn');
const navMenu = document.getElementById('nav-menu');

function setMenu(open) {
  navMenu.classList.toggle('active', open);
  menuButton.classList.toggle('active', open);
  menuButton.setAttribute('aria-expanded', String(open));
}

// Clicking the hamburger opens or closes the menu
menuButton.addEventListener('click', () => {
  setMenu(!navMenu.classList.contains('active'));
});

// Clicking anywhere outside the menu and button closes it
document.addEventListener('click', (event) => {
  const isMenuOpen = navMenu.classList.contains('active');
  const clickedOutsideMenu = !navMenu.contains(event.target);
  const clickedOutsideButton = !menuButton.contains(event.target);

  if (isMenuOpen && clickedOutsideMenu && clickedOutsideButton) {
    setMenu(false);
  }
});

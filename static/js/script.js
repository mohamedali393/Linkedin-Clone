const userProfileBtn = document.getElementById('user-profile');
const toggleMenu = document.querySelector('.toggle-menu');
const recent = document.querySelector('.recent-activities');
const showMoreBtn = document.getElementById('sidebarToggleBtn');
const alerts = document.querySelectorAll('.alert');

if(userProfileBtn){
    userProfileBtn.addEventListener('click',() => {
        toggleMenu.classList.toggle('toggle-menu-height');
    });
}

let isOpen = false;

if(showMoreBtn){
    showMoreBtn.addEventListener('click',() => {
        isOpen = isOpen === true ? false : true;
        showMoreBtn.textContent = isOpen ? 'Show Less -' : 'Show More +';
        recent.classList.toggle('open');
    });
}

console.log(alerts);


if(alerts){
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.parentElement.removeChild(alert);
        }, 3000);
    })
}
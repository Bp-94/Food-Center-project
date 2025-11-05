const menuBtn = document.querySelector('.menu-btn');
const dropdown = document.getElementById('dropdown')
const orderButtons = document.querySelectorAll(".special-button1");
const page_sung = document.getElementById("pop");
const orderButtons2 = document.querySelectorAll(".special-button2");
const page_sung2 = document.getElementById("pop2");
const orderButtons3 = document.querySelectorAll(".special-button3");
const page_sung3 = document.getElementById("pop3");
const orderButtons4 = document.querySelectorAll(".special-button4");
const page_sung4 = document.getElementById("pop4");
const quantitySelectors = document.querySelectorAll('.quantity-selector');

menuBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  dropdown.classList.toggle('show');
})

window.addEventListener('click', () => {
  dropdown.classList.remove('show');
})

orderButtons.forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    page_sung.style.display = 'flex';
  });
});

orderButtons2.forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    page_sung2.style.display = 'flex';
  });
});

orderButtons3.forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    page_sung3.style.display = 'flex';
  });
});

orderButtons4.forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    page_sung4.style.display = 'flex';
  });
});


  function goBack() {
    window.history.back();
  }

  function goBackPage() {
  window.location.href = "noodle.html";
}

function gotopage() {
  window.location.href = "pay.html";
}

quantitySelectors.forEach(selector => {
    const minusBtn = selector.querySelector('.minus');
    const plusBtn = selector.querySelector('.plus');
    const qtyInput = selector.querySelector('.qty');

    minusBtn.addEventListener('click', () => {
        let current = parseInt(qtyInput.value);
        if(current > 1) qtyInput.value = current - 1;
    });

    plusBtn.addEventListener('click', () => {
        let current = parseInt(qtyInput.value);
        qtyInput.value = current + 1;
    });
});
if (!localStorage.getItem('counter')) {
    let counter = localStorage.setItem('counter', 0)
}

function count() {
    let counter = localStorage.getItem('counter')
    counter++;
    document.querySelector('h1').innerHTML = counter;
    localStorage.setItem('counter', counter)
}

document.addEventListener('DOMContentLoaded', function(){
    // assign a variable a function also rememeber event listener methods
    var element = document.querySelector('button')
    element.onclick = count
    document.querySelector('h1').innerHTML = localStorage.getItem('counter')
})
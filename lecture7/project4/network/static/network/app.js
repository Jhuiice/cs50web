document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector('#profile-view').style.display = "none";
    document.querySelector('#post-view').style.display = "block";
    document.querySelector('#following-view').style.display = "none";
    document.querySelector('#post-form-container').style.display = "none";

    document.querySelector('#post-submit').addEventListener('click', submit_post)
    // document.querySelector('.profile-link').addEventListener('click',
    // load_profile)
})

// function load_profile() {
//     document.querySelector('#profile-view').style.display = "block";
// }

function load_post() {
    let post = document.querySelector('#post-form-container')
    post.value = "";
    post.style.display = "block";


}
function hide_post() {
    let post = document.querySelector('#post-form-container')
    post.value = "";
    post.style.display = "none";
}

function submit_post(event) {

    event.preventDefault()

    let content = document.querySelector('#post-content').value;
    const csrftoken = getCookie('csrftoken')

    fetch('/new_posts', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            content: content
        })
    })
    document.querySelector('.post-content').value = ""
    // .then(load_network())
    // call a function to hide the post and refresh the posts without reloading the page
    // .then()
}

// Got this code from the Django documents
// Grabs cookies based on names
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue
}
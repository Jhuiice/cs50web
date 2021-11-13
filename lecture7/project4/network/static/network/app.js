//? How do i get the js to reload on every page?
document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector('#profile-view').style.display = "none";
    document.querySelector('#post-view').style.display = "block";
    document.querySelector('#following-view').style.display = "none";
    document.querySelector('#post-form-container').style.display = "none";
    document.querySelector('.form-post-content').value = "";
    document.querySelectorAll('.edit-link').forEach(edit => {
        edit.addEventListener('click', edit_post)
    })

    // document.querySelector('#post-submit').addEventListener('click', submit_post)
    // document.querySelector('.profile-link').addEventListener('click',
    // load_profile)
})


// TODO figure out how to load the event listeners to the page on reload
function edit_post(event) {
    event.preventDefault();
    let post_id = event.target.dataset.post_id;
    let post_user = event.target.dataset.post_creator;
    let before_content = document.querySelector(`.post-container [data-post_id="${post_id}"]:nth-child(3) span`).innerHTML;

    let edit_form = document.createElement("form");
    edit_form.setAttribute('method', 'put')
    edit_form.setAttribute('class', 'edit-form')

    let textarea = document.createElement('textarea');
    textarea.className = 'form-control form-post-content';
    textarea.id = 'exampleFormControlTextarea4';
    textarea.setAttribute('rows', '3');
    textarea.setAttribute('name', 'content');
    textarea.innerHTML = before_content;

    let submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    submit.setAttribute('value', 'Save');

    edit_form.append(textarea)
    edit_form.append(submit)

    // hide preexisting content spot
    document.querySelector(`.post-container [data-post_id="${post_id}"]:nth-child(3) span`).innerHTML = '';
    document.querySelector('.edit-link').style.display = 'none';

    // append form to content upon clicking the edit button
    document.querySelector(`.post-container [data-post_id="${post_id}"]:nth-child(3)`).append(edit_form);

    document.querySelector('.edit-form input').addEventListener('click', (event) =>{
        event.preventDefault()
        // grab new content
        let new_content = document.querySelector('.edit-form textarea').value
        const csrftoken = getCookie('csrftoken')
        // fetch edit post and add content to db
        fetch('/edit_post/' + post_id, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                content: new_content
            })
        })
        // delete form
        .then(document.querySelector('.edit-form').remove())
        // unhide edit button
        .then(document.querySelector('.edit-link').style.display = 'block')
        // add content back to span
        .then(document.querySelector(`.post-container [data-post_id="${post_id}"]:nth-child(3) span`).innerHTML = new_content)
    });
}

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
    .then(document.querySelector('.post-content').value = "")
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
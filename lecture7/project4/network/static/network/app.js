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

// function load_profile() {
//     document.querySelector('#profile-view').style.display = "block";
// }
// all you needto do is add a text area that is edible and a save button
// TODO figure out how to load the event listeners to the page on reload
function edit_post(event) {
    event.preventDefault();
    let post_id = event.target.dataset.post_id
    let post_user = event.target.dataset.post_creator
    console.log(post_id)
    console.log(post_user)
    let post_container = document.querySelector(`.post-container [data-post_id="${post_id}"`)
    return event
    // get the post youre going to edit
    // let parent = element.parentNode
    // let content = document.querySelector('.post-content span');
    // console.log("Success");
    // function show_edit(edit) {
    //     if (edit){
    //         document.querySelector('.edit-view').style.display = "block"
    //     }
    //     else {
    //         document.querySelector('.edit-view').style.display = "none"
    //     }
    // }
    // fetch('/post/' + id, {
    //     method:"PUT",
    //     body: {
    //         content: document.querySelector('.edit-content')
    //     }
    // })
    // .then(response => response.json())
    // .then(post => {
    //     console.log(post)
    // })
    // fill out the data that has already been there
    // allow edit
    // resubmit edit as a put request

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
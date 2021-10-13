// Start with first post
let counter = 1;

// Load posts 20 at a time
const quantity = 15;

// When Dom loads, render the first 20 posts
document.addEventListener('DOMContentLoaded', load)

// If scrolled to bottom, load the next 20 posts
window.onscroll = () => {
    if (window.scrollY + window.innerHeight > document.body.offsetHeight){
        load();
    }
};


// load next set of posts
function load(){
    // set start and end post numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    // get new posts and add posts
    fetch(`posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post);
    })
}

// Add a new post with given contents on DOM
function add_post(contents) {
    // create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = contents;

    // Add posts to DOM
    document.querySelector('#posts').append(post);
};
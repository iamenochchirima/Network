document.addEventListener("DOMContentLoaded", function() {

    //Using nav_links to navigate between views
    document.querySelector('#all_post').addEventListener('click', posts);
    document.querySelector('#create').addEventListener('click', create_post);
    document.querySelector('#following').addEventListener('click', following);

    posts();
});

function posts() {

  document.querySelector('#posts_page').style.display = 'block';
  document.querySelector('#following_page').style.display = 'none';
  document.querySelector('#create_post').style.display = 'none';

    fetch(`all_posts`)
    .then(response => response.json())
    .then(posts => {
    
        console.log(posts);
    
    })

}

function create_post(event) {
    event.preventDefault()

    document.querySelector('#posts_page').style.display = 'none';
    document.querySelector('#following_page').style.display = 'none';
    document.querySelector('#create_post').style.display = 'block';

}

function following(event) {

    event.preventDefault()

    document.querySelector('#posts_page').style.display = 'none';
    document.querySelector('#following_page').style.display = 'block';
    document.querySelector('#create_post').style.display = 'none';
    
}
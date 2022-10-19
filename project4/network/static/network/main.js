document.addEventListener('DOMContentLoaded', function() {
    
    const followButton = document.querySelector('.toggle-btn');
    const followerCount = document.querySelector('.following_count');

    if (followButton) {
        followButton.addEventListener("click", (e) => {
            console.log('This element has been clicked!')
            let username = e.currentTarget.getAttribute("value");
            fetch(`${username}/follow_unfollow`)
            .then((response) => response.json())
            .then((data) => {
            console.log(data);
            followerCount.textContent = data.followers;
            });

            if (followButton.innerHTML == "Unfollow") {
                followButton.innerHTML = "Follow";
            }
            else {
                followButton.innerHTML = "Unfollow";
            }
        });

    }
     

    let edit_buttons = document.querySelectorAll('.edit-btn');

    edit_buttons.forEach(edit_button => {
        edit_button.addEventListener('click', (event) => {

           let post_id = event.currentTarget.dataset.id;
           let post_body = document.querySelector(`div[data-id="${post_id}"]`);
           console.log(post_body);
           let original_post = post_body.querySelector(".original");
           let post_edit = post_body.querySelector(".post-edit");
           let saveBtn = post_edit.querySelector("button");
           let cancelBtn = post_edit.querySelector(".cancel")
           let time = post_body.querySelector(".time")
           console.log(time);

           post_edit.style.display = 'block';
           original_post.style.display = 'none';
           edit_button.style.display = 'none';
           time.style.display = 'none';

            cancelBtn.addEventListener('click', (event) => {
                event.preventDefault();

                post_edit.style.display = 'none';
                original_post.style.display = 'block';
                edit_button.style.display = 'block';
                time.style.display = 'block';

            })

           saveBtn.addEventListener('click', (event) => {

            event.preventDefault();

            fetch(`edit_post/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: post_body.querySelector("textarea").value,
                })
              })
              .then(response => response.json())
              .then(result => {
                
                original_post.textContent = result.content;
                console.log(original_post);

                post_edit.style.display = 'none';
                original_post.style.display = 'block';
                edit_button.style.display = 'block';
                time.style.display = 'block';

                })
            });
            
        })    
       

    }) 
       
})

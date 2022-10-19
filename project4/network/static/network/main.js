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
     

    var edit_buttons = document.querySelectorAll('#edit-btn');
    console.log(edit_buttons);

    edit_buttons.forEach(edit_button => {
        edit_button.addEventListener('click', () => {
            document.querySelector('.post-edit').style.display = 'block';
            document.querySelector('.original').style.display = 'none';

            console.log("Finished this function");
        });
    }) 
       
})






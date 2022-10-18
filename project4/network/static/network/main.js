document.addEventListener('DOMContentLoaded', function() {

    const followButton = document.querySelector('.toggle-btn');
    console.log(followButton)
    const followerCount = document.querySelector('.following_count');
    console.log(followerCount)

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
       
})






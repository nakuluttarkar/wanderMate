//SIDEBAR
const menuItems = document.querySelectorAll('.menu-item');
//Messages
const messagesNotification = document.getElementById('messages-notification');
const messages = document.getElementById('messages');

//message-search
const message = messages.getElementsByClassName('message');
const messageSearch= document.querySelector('#message-search');

//remove active class fucntion
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

menuItems.forEach(item => {
    item.addEventListener('click',() => {
        changeActiveItem();
        item.classList.add('active');
        if(item.id != 'notifications'){
            document.querySelector('.notifications-popup').style.display = 'none';
        }else{
            document.querySelector('.notifications-popup').style.display = 'block';
            document.querySelector('#notifications .notification-count').style.display = 'none';
        }
    })
})

//Messages

//searching messages

const searchMessage = () => {
    const val = messageSearch.value.toLowerCase();
    console.log(val);
    message.forEach(user => {
        let name = user.querySelectorAll('h5').textContent.toLowerCase();
        if(name.indexOf(val) != -1){
            user.style.display = 'flex';
        }else{
            user.style.display = 'none'
        }
    })
}

// messageSearch.addEventListener('keyup', searchMessage);

// messagesNotification.addEventListener('click',() => {
//     messages.style.boxShadow = '0 0 1rem var(--color-primary)';
//     messagesNotification.querySelector('.notification-count').style.display = 'none';
//     setTimeout(() => {
//         messages.style.boxShadow = 'none';
//     }, 2000);
// })

console.log("hello")
document.addEventListener('DOMContentLoaded', function() {
    // Handle like button click
    document.querySelectorAll('.like-button').forEach(function(button) {
        button.addEventListener('click', function(event) {
            // Prevent the default form submission
            event.preventDefault();
    
            // Get the post ID from the button's data attribute
            var postId = button.dataset.postId;
            console.log('Post ID:', postId); // Debugging output
    
            // Send an AJAX request to like the post
            fetch(`/like-post/?post_id=${postId}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Server response:', data); // Debugging output
                    // Update the UI based on the response
                })
                .catch(error => console.error('Error:', error)); // Handle errors
        });
    });
});
console.log("hello1")
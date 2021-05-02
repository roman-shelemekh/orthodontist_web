export function likeQuestion() {
    const button = document.getElementsByClassName('like-btn')
    Array.from(button).forEach(element => {
        element.addEventListener('click', () => {
            const url = element.dataset.url
            const request = new XMLHttpRequest()
            request.responseType = 'json'
            request.open('GET', url)
            request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
            request.send()
            request.onload = function () {
                if (this.status >= 200 && this.status < 400) {
                    if (this.response.auth) {
                        window.location = this.response.auth
                    } else {
                        element.querySelector('.like_count').textContent = this.response.like_count
                        if (this.response.add) {
                            element.classList.add('active')
                        } else {
                            element.classList.remove('active')
                        }
                    }
                } else {
                    console.log('Did not get anything')
                }
            }
            request.onerror = function () {
                console.log('Connection error');
            }
        })
    })
}

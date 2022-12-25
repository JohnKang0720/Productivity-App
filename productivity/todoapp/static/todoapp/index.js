document.addEventListener('DOMContentLoaded', () => {
    const div = document.querySelector("#edit-div");
    div.style.display = "none";
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function search(){
//     console.log("searched")
//     const todos = document.querySelectorAll('#todo');
//     let searchValue = document.querySelector('#textfield').value;
//     todos.forEach((todo) => {
//         console.log(todo.children[0].textContent)
//         if(todo.children[0].textContent === searchValue){
//             todo.style.display = "block"
//         }else{
//             todo.style.display = "none"
//         }
//     })
// }
const textfield = document.querySelector("#textfield");
const titles = document.querySelectorAll("#todo");
textfield.addEventListener('keyup', e => {
    console.log(e.target.value)
    value = textfield.value
    titles.forEach((title) => {
        let name = title.getElementsByTagName('p')[0];

        if(!name.textContent.includes(e.target.value)){
            title.style.display = "none";
        }else{
            title.style.display = "block";
        }
    })
})

function addToFolder(todo_id, title){
    const selected = document.querySelector("#folders");
    fetch(`/folder/${selected.options[selected.selectedIndex].value}`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            folder: selected.options[selected.selectedIndex].value,
            title: title
        })
    }).then(response => response.json())
    .then(result => {
        alert("Added!")
    })
}

const todos = document.querySelectorAll("#todo")
const containers = document.querySelectorAll("#container")
//drag and drop
todos.forEach((todo) => {
    todo.addEventListener('dragstart', () => {
        console.log("dragstart")
        todo.classList.add("dragging")
    })

    todo.addEventListener('dragend', () => {
        console.log("dragend")
        todo.classList.remove("dragging")
        const finished = document.querySelector(".finished")
        if (finished.children.length != 1) {
            //take the elements inside the container, add it to new model and delete it form old model
            add(todo)
        }
    })
})

containers.forEach((container) => {
    csrftoken = getCookie('csrftoken')
    container.addEventListener('dragover', (e) => {
        e.preventDefault()
        const todo = document.querySelector('.dragging')
        container.appendChild(todo)
    })
})

function add(todo) {
    title = todo.children[0].textContent
    notes = todo.children[1].textContent
    due = todo.children[2].textContent

    todo_id = todo.children[3].textContent
    fetch('/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            todoid: todo_id,
            title: title,
            notes: notes,
            due: due
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
}

function sendTodo() {
    const task = document.querySelector('#task').value;
    const note = document.querySelector('#note').value;
    const date = document.querySelector('#date').value;
    const username = document.querySelector('#username').value;
    csrftoken = getCookie('csrftoken')
    fetch('/send', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            task: task,
            note: note,
            date: date,
            username: username
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
}

function editTodo(user_id) {
    const div = document.querySelector("#edit-div");
    div.style.display = "block";
    //create elements
    const form = document.createElement('form');
    const input = document.createElement('input');
    const submitBtn = document.createElement('button');

    //Bootstrap stuff
    input.classList.add("form-control")
    input.style.marginTop = "10px"
    input.style.marginBottom = "10px"
    submitBtn.classList.add("btn")
    submitBtn.classList.add("btn-primary")

    div.append(form);
    form.append(input);
    form.append(submitBtn);
    submitBtn.innerHTML = "Submit";

    submitBtn.addEventListener('click', () => {
        edit(user_id, input)
    })
}

function edit(user_id, input) {
    //csrf token cookie to prevent serverside attacks
    csrftoken = getCookie('csrftoken')

    if (input.value != "") {
        fetch(`/edit/${user_id}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                msg: input.value
            })
        })
            .then(response => response.json())
            .then(result => {
                alert("Edited!")
                console.log(result)
            })
    }
}

fetch('/api/members/', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access'),
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data));
function getCookie(cName) {
  const name = cName + "=";
  const cDecoded = decodeURIComponent(document.cookie); //to be careful
  const cArr = cDecoded.split('; ');
  let res;
  cArr.forEach(val => {
    if (val.indexOf(name) === 0) res = val.substring(name.length);
  })
  return res
}


const darkModeToggle = document.querySelector('#dark-mode-toggle');

const enableDarkMode = () => {
  document.body.classList.add("dark");
  document.cookie = "darkMode=enabled; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
  //localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
  document.body.classList.remove("dark");

  document.cookie = "darkMode=disabled; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
  //localStorage.setItem('darkMode', null);
}

//callback in case of absence of backed logic
//{
//let darkMode = localStorage.getItem('darkMode');

darkMode = getCookie('darkMode'); 
if (darkMode === 'enabled' && !document.body.classList.contains('dark')) {
  enableDarkMode();
}
//}

darkModeToggle.addEventListener('click', () => {
  darkMode = getCookie('darkMode'); 

  if (darkMode !== 'enabled') {
    enableDarkMode(); 
  } else {  
    disableDarkMode(); 
  }
  var url = "/";

  var req = new XMLHttpRequest();
  req.open("GET", url);

  req.send();
});
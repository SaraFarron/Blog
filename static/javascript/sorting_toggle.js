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

const sortingToggle = document.querySelector('#sorting-toggle');

const enableSortingByPopularity = () => {
    document.cookie = "sorting=popularity; expires=Tue, 19 Jan 9999 03:14:07 GMT";
  }
  
  const enableSortingByNovelty = () => {
    document.cookie = "sorting=novelty; expires=Tue, 19 Jan 9999 03:14:07 GMT";
  }
   
  // When someone clicks the button
  sortingToggle.addEventListener('click', () => {
  
    sorting = getCookie('sorting'); 
    
    // if it not current enabled, enable it
    if (sorting !== 'popularity') {
        enableSortingByPopularity();
    // if it has been enabled, turn it off  
    } else {  
        enableSortingByNovelty(); 
    }
    document.location.reload();
  });
// check for saved 'darkMode' in localStorage
let sorting = localStorage.getItem('sorting'); 

const sortingToggle = document.querySelector('#sorting-toggle');

const enableSortingByPopularity = () => {
    document.cookie = "sorting=popularity; expires=Tue, 19 Jan 9999 03:14:07 GMT";
    localStorage.setItem('sorting', 'popularity');
  }
  
  const enableSortingByNovelty = () => {
    document.cookie = "sorting=novelty; expires=Tue, 19 Jan 9999 03:14:07 GMT";
    localStorage.setItem('sorting', 'novelty');
  }
   
  // When someone clicks the button
  sortingToggle.addEventListener('click', () => {
  
    sorting = localStorage.getItem('sorting'); 
    
    // if it not current enabled, enable it
    if (sorting !== 'popularity') {
        enableSortingByPopularity();
    // if it has been enabled, turn it off  
    } else {  
        enableSortingByNovelty(); 
    }
    document.location.reload();
  });
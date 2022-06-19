const sortingToggle = document.querySelector('#sorting-toggle');

const enableSortingByPopularity = () => {
    document.cookie = "sorting=popularity; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
  }
  
const enableSortingByNovelty = () => {
  document.cookie = "sorting=novelty; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
}

sortingToggle.addEventListener('click', () => {

  sorting = getCookie('sorting'); 
  
  if (sorting !== 'popularity') {
      enableSortingByPopularity();
  } else {  
      enableSortingByNovelty(); 
  }
  document.location.reload();
});
const sortingToggle = document.querySelector('#sorting-toggle');

const sortingVariants = document.querySelectorAll('[data-sort-by]');

const enableSortingByPopularity = () => {
    document.cookie = "sorting=popularity; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
    document.location.reload();
  }
  
const enableSortingByNovelty = () => {
  document.cookie = "sorting=novelty; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
  document.location.reload();
}

const enableSortingByRating = () => {
  document.cookie = "sorting=rating; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/";
  document.location.reload();
}

//sortingToggle.addEventListener('click', () => {

  //sorting = getCookie('sorting');

  sortingVariants?.forEach((element) => {
    if (element.getAttribute('data-sort-by') === 'popularity') {
      element.addEventListener('click', () => enableSortingByPopularity());
    }
    else if (element.getAttribute('data-sort-by') === 'rating') {
      element.addEventListener('click', () => enableSortingByRating());
    }
    else {
      element.addEventListener('click', () => enableSortingByNovelty());
    }
  })
  
  // if (sorting == 'popularity') {
  //    enableSortingByRating();
  // } else if (sorting == 'rating') {  
  //     enableSortingByNovelty(); 
  // } else {
  //   enableSortingByPopularity();
  // }
//});
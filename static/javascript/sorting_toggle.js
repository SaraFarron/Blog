const sortingToggle = document.querySelector('#sorting-toggle');

const sortingVariants = document.querySelectorAll('[data-sort-by]');

const switchSorting = (target, cookieName) => {
  document.cookie = `sorting=${cookieName}; expires=Tue, 19 Jan 9999 03:14:07 GMT; path=/`;
  window.location.assign(target.getAttribute('data-url-to-sorted'));
}

//sortingToggle.addEventListener('click', () => {

  //sorting = getCookie('sorting');

  sortingVariants?.forEach((element) => {
    if (element.getAttribute('data-sort-by') === 'popularity') {
      element.addEventListener('click', (e) => {
        console.log(e.target)
        switchSorting(e.target, 'popularity')}
      );
    }
    else if (element.getAttribute('data-sort-by') === 'rating') {
      element.addEventListener('click', (e) => {
        switchSorting(e.target, 'rating')
      });
    }
    else {
      element.addEventListener('click', (e) => {
        switchSorting(e.target, 'novelty')
      });
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
import Blazy from '../../node_modules/blazy/blazy';

(function () {
	'use strict';

	// window.init_map = () => {
	// 	let map_el = document.getElementById('map');
	//
	// 	window.artwork_map = new google.maps.Map(map_el, {
	// 		center: {lat: -34.397, lng: 150.644},
	// 		zoom: 8
	// 	});
	//
	// 	 new google.maps.Marker({position: {lat: -34.397, lng: 150.644}, map: map});
	// };

	if (document.querySelector('.artwork-grid')) {
		let blazy = new Blazy();
	}


	let artwork_filters = document.querySelectorAll('.filter-artwork select');

	if (artwork_filters) {
		for (let filter of artwork_filters) {
			filter.addEventListener('change', () => {

				const selected = filter.options[filter.selectedIndex];
				const name = filter.name;

				if (filter.selectedIndex === 0) {
					window.location.pathname = '/';
				} else if (selected) {
					window.location.pathname = '/' + name + '/' + selected.value;
				}
			});
		}
	}

})();
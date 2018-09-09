(function () {
	'use strict';

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

	let render_large_map = function (start_lat, start_long) {
		const default_lat = -42.8838359, default_long = 147.3311996;

		let center = (start_lat === undefined || start_long === undefined) ?
			{lat: default_lat, lng: default_long} :
			{lat: start_lat, lng: start_long};

		let map = new google.maps.Map(document.getElementById('large-map'), {
			zoom: 17,
			center: center
		});

		if (window.artwork_locations) {
			for (let artwork of window.artwork_locations) {
				let marker = new google.maps.Marker({
					position: {lat: artwork.lat, lng: artwork.long},
					map: map,
					icon: '/static/images/thumb/' + artwork.image
				});

			    let infowindow = new google.maps.InfoWindow({
				    content: artwork.title + '<br><img src="/static/images/full/' + artwork.image + '" width="200px" style="display: block; margin: 5px auto 0">'
			    });

				marker.addListener('click', () => {
					window.location.pathname = '/artwork/' + artwork.uid
				});

				marker.addListener('mouseover', () => infowindow.open(map, marker));
				marker.addListener('mouseout', () => infowindow.close(map, marker));
			}
		}

		if (start_lat !== undefined && start_long !== undefined) {
			let marker = new google.maps.Marker({
				position: center,
				map: map,
				animation: google.maps.Animation.DROP,
				label: 'You are here'
			});
		}
	};

	window.load_large_map = function () {

		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => render_large_map(position.coords.latitude, position.coords.longitude),
				() => render_large_map()
			);
		} else {
			render_large_map()
		}
	}

})();
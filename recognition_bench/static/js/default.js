$(function() {
	$resultTemplate = $(
		'<div class="column">' +
			'<div class="ui fluid card">' +
				'<div class="medium image">' +
					'<img data-dz-thumbnail>' +
				'</div>' +
				'<div class="content">' +
					'<div class="header" data-dz-name></div>' +
					'<div class="meta" data-dz-size>' +
					'</div>' +
					'<div class="description" data-dz-errormessage>' +
						'<div class="ui indicating progress success">' +
							'<div class="bar" data-dz-uploadprogress></div>' +
						'</div>' +
						'<div class="ui active inverted dimmer">' +
							'<div class="ui text loader">Loading</div>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>'+
		'</div>'
	);

	var upload = new Dropzone('.upload', {
		url: '/classify',
		thumbnailHeight: null,
		thumbnailWidth: null,
		maxFileSize: 10,
		accept: function(file, done) {
			if (file.type === 'image/jpeg' || file.type === 'image/png') {
				done()
			}
		},
		previewsContainer: '.results',
		previewTemplate: $resultTemplate[0].outerHTML
	});

	upload.on('addedfile', function(file) {
		console.log(file);
	});

	upload.on('dragover', function(ev) {
		console.log(ev);
		$(ev.target).addClass('hover');
	});

	upload.on('dragleave', function(ev) {
		console.log(ev);
		$(ev.target).removeClass('hover');
	});

	generateLabels = function(labels) {
		var labelsHTML = "";

		labels.forEach(function(label) {
			labelsHTML += 
				'<div class="item">' +
					'<div class="header">' + label.name.toLowerCase() + '</div>' +
					_.round(parseFloat(label.confidence) * 100, 2) + '%' +
				'</div>';
		});

		return labelsHTML;
	}

	upload.on('success', function(file, response) {
		response.services.forEach(function(service) {
			var $result = $(
				'<h3 class="ui pink header">' + service.service_name + '</h5>' +
				'<div class="ui horizontal list">' +
					generateLabels(service.labels) +
				'</div>'
			);

			$(file.previewElement).find('.dimmer').removeClass('active'); // disable loader
			$(file.previewElement).find('.description').append($result);
		});
	});
});
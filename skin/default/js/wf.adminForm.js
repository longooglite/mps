// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function() {
	$.widget( "wfWidgets.wfAdminForm",  {
		options: {
			item: false,
			auth: false
		},

		_create: function(){
			var $this = this,
				$form = $this.element;

			$form.trigger('safeInitFormWidgets');

			cvApp._handleRepeatingFields({
                iCols: 'none',
                iOffset: 'none',
                sClass: 'wf-form-right'
            });
			// New: Author Etc Widget fields need Init:
			$body.find('.mps-json-enums-widget').each(function(){
				var $sel = $(this);
				console.log('Have a repeatingInputSelect:', $sel);
				// Init widget...
			});
		}
    });
});

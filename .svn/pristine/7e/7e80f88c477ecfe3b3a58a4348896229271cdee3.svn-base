// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function() {
	$.widget( "wfWidgets.serverSideAjaxForm", $.wfWidgets.itemWidget,  {
		options: {
			item: false,
			auth: false
		},

		_create: function(){
			var $this = this,
				$element = $this.element;

			// New: Common Config States for each Widget Instance (for non-selector based OO code later)
			$this.states = {};
			$this.states = $this.options.item.common;

			// Make HTML -> jQ obj:
			$this.$form = $($this._createForm());
			$this.$form.mpsForm();
			// RENDER:s
			$this.element.append($this.$form);

			$this.setWidgetToAjaxFormInterfaces();
		},

		_createForm: function(){
			var $this = this,
				item = $this.options.item,
				auth = $this.options.auth,
				tplForm = $('#wf-workflow-serverside-ajax-form').html(),
				sGuid = wfApp._createUniqueID('GUID_'+wfApp._safeDomGuid(item.common.descr)),
				data = {
					descr: item.common.descr,
					domGuid: sGuid
				};
			return wfApp.wfTemplate(tplForm, data);

		}
	});
});

odoo.define('custom_item.action_button', function (require) {
	"use strict";
	var core = require('web.core');
	var ListController = require('web.ListController');
	var FormController = require('web.FormController');
    var FormView = require('web.FormView');
	var rpc = require('web.rpc');
	var session = require('web.session');
	var _t = core._t;

    FormController.include({
        /**
         * Main method used when saving the record hitting the "Save" button.
         * We check if the stage_id field was altered and if we need to display a rainbowman
         * message.
         *
         * @override
         */
        renderButtons: function ($node) {
			this._super.apply(this, arguments);
			if (this.$buttons) {

			    this.$buttons.find("#button_click").click(this.proxy('action_def'))
				//this.$buttons.find('.oe_action_button').click(this.proxy('action_def'));
			}
		},
		action_def: function (ev) {
		    env.stopPropagation();
		    var self = this;
		    var parent = self;
		    var ciclos = 0;

		    while (ciclos <= 100 || !jQuery(parent.el).hasClass('o_action o_view_controller')) {
                parent = parent.getParent();
		    }

		    if (jQuery(parent.el).hasClass('o_action o_view_controller')) {
		        parent.saveRecord();
		        parent._setMode("edit");
		    }

		    //this._updateControlPanel();
            //this._setMode('edit');
		    //self.saveRecord();
		}
        });

	/*
	 saveRecord: function () {
            var self = this;
            return this._super(...arguments).then((modifiedFields) => {
                console.log(modifiedFields);
                if (modifiedFields.indexOf('stage_id') !== -1) {
                    this._checkRainbowmanMessage(this.renderer.state.res_id)
                }
            });
        }
	ListController.include({
	    custom_events: {
	        open_record: _.extend({} function ($node) {
	            //this._super.apply(this, arguments);
	            console.log(this);
	            console.log($node);
	        }
	    },
	     custom_events: _.extend({}, ListController.prototype.custom_events, {
           open_record: '_openRecord',
         }),
         _openRecord: function(event) {
            event.stopPropagation();

            var self = this;
            this.handle = event.data.id;
            // console.log(this);
            //console.log(event);
            event.target.do_action({ views: [[false, 'form']],
             view_type: 'form',
             view_mode: 'form',
             res_model: self.modelName,
             type: 'ir.actions.act_window',
             target: 'current',
             res_id: self.model.__id });
            //self.trigger_up('open_record', { id: event.data.id, mode: "edit" });
            //this.model.duplicateRecord(this.handle);
         },
		renderButtons: function ($node) {
			this._super.apply(this, arguments);
			if (this.$buttons) {
				this.$buttons.find('.oe_action_button').click(this.proxy('action_def'));
			}
		},
		action_def: function(){
		    var self = this
		    var user = session.uid;
		    rpc.query(
		        {
		        model: 'odoo_view_advanced.custom_item',
		        method: 'removeItems',
		        args: [
		            [user], {
		                'id': user
		            }
		        ]
		        }
		    ).then(function (e) {
                self.do_action({
                    name: _t('action_custom_item'),
                    type: 'ir.actions.act_window',
                    res_model: 'odoo_view_advanced.custom_item',
                    views: [[false, 'form']],
                    view_mode: 'form',
                    target: 'new',
                });
                window.location
            });
		}
	})*/
});
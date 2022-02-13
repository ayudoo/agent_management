odoo.define('agent_management.commissionable', function(require) {
  "use strict";

  var field_registry = require('web.field_registry');
  var basic_fields = require('web.basic_fields');

  var CommissionToggle = basic_fields.FieldBoolean.extend({
    className: 'o_field_commission o_field_boolean o_field_widget o_checkbox',
    _render: function() {
      this._super.apply(this, arguments);
      if (this.value === true) {
        // fix slightly to small Odoo checkbox padding
        var $container = $('<span style="margin-left: 0.75rem;"/>');
        var monetaryField = new basic_fields.FieldMonetary(
          this, 'amount_commission', this.record, {
            'mode': 'readonly'
          }
        );
        monetaryField.$el = $container;
        monetaryField._render();
        this.$el.append(monetaryField.$el);
      }
    },
  });

  field_registry.add('commission', CommissionToggle);
  return {
    CommissionToggle: CommissionToggle,
  };
});

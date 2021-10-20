# -*- coding: utf-8 -*-

from odoo import models
from odoo.execeptions import UserError

KEY_PARAM_SHOULD_CHECK_ADJUSTMENT = 'stock_picking_cacelation_should_check_adjustment'

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_cancel_doned_picking(self):
        def _cancel_stock_move(record):
            moves = record.move_lines
            move_lines = moves.mapped('move_line_ids')
            move_lines.write(dict(qty_done=0))
            moves.write(dict(state='cancel'))

        def _cancel_account_move(record):
            moves = record.move_lines
            account_moves = self.env['account.move'].search([
                ('stock_move_id', 'in', moves.ids)
            ])
            account_moves.button_cancel()
        
        def _check_adjustment(record):
            # by default always check existing adjustment
            if not _should_check_adjustment(record):
                return

            inv_model = self.env['stock.quant']
            for move in record.move_lines:
                exist_adjustment = inv_model.search([
                    ('state', '=', 'done'),
                    ('date', '>', move.date),
                    ('product_id', '=', move.product_id.id),
                    '|', 
                        ('location_id.usage', '=', 'inventory'),
                        ('location_dest_id.usage', '=', 'inventory'),
                ], order='date desc', limit=1)

                if not exist_adjustment:
                    continue
                raise UserError('Already contain adjustment above date transfer!.')
        
        def _should_check_adjustment(record):
            params = record.env['ir.config_parameter'].sudo()
            should_check = int(params.get(KEY_PARAM_SHOULD_CHECK_ADJUSTMENT, 0)) == 1
            return should_check

        records = self.filtered(lambda e: e.state != 'cancel')
        for record in records:
            _check_adjustment(record)
            _cancel_stock_move(record)
            _cancel_account_move(record)

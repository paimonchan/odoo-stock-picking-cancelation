# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_cancel(self):
        def _cancel_stock_move(record):
            moves = record.move_lines
            move_lines = moves.mapped('move_line_ids')
            move_lines.write(dict(qty_done=0))
            moves.write(dict(state='cancel'))
        records = self.filtered(lambda e: e.state != 'cancel')
        for record in records:
            _cancel_stock_move(record)
